"""Integration tests for the A/B testing library."""

import pytest
from ab_testing import (
    Experiment, 
    Variant, 
    z_test_proportions,
    calculate_sample_size,
    calculate_confidence_interval,
    is_statistically_significant
)


class TestEndToEndWorkflow:
    """Test complete A/B testing workflow."""
    
    def test_complete_ab_test_workflow(self):
        """Test a complete A/B test from setup to analysis."""
        # Step 1: Calculate required sample size
        sample_size = calculate_sample_size(
            baseline_rate=0.10,
            minimum_detectable_effect=0.20,
            alpha=0.05,
            power=0.8
        )
        
        assert sample_size > 0
        
        # Step 2: Create experiment
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        
        experiment = Experiment(
            name="integration_test",
            variants=variants,
            seed=42
        )
        
        # Step 3: Simulate user assignments
        import random
        num_users = min(sample_size, 1000)  # Use smaller number for test speed
        
        for i in range(num_users):
            user_id = f"user_{i}"
            variant = experiment.assign_variant(user_id=user_id)
            
            # Simulate conversions
            random.seed(i)
            if variant.name == "control":
                if random.random() < 0.10:
                    experiment.record_conversion("control")
            else:
                if random.random() < 0.12:
                    experiment.record_conversion("treatment")
        
        # Step 4: Get results
        results = experiment.get_results()
        
        assert "control" in results
        assert "treatment" in results
        assert results["control"]["exposures"] > 0
        assert results["treatment"]["exposures"] > 0
        
        # Step 5: Calculate confidence intervals
        control = experiment.get_variant("control")
        treatment = experiment.get_variant("treatment")
        
        ci_control = calculate_confidence_interval(
            control.conversions,
            control.exposures
        )
        ci_treatment = calculate_confidence_interval(
            treatment.conversions,
            treatment.exposures
        )
        
        assert len(ci_control) == 2
        assert len(ci_treatment) == 2
        assert ci_control[0] <= control.conversion_rate <= ci_control[1]
        assert ci_treatment[0] <= treatment.conversion_rate <= ci_treatment[1]
        
        # Step 6: Perform statistical test
        z_score, p_value, se = z_test_proportions(
            control.conversions,
            control.exposures,
            treatment.conversions,
            treatment.exposures
        )
        
        assert isinstance(z_score, float)
        assert isinstance(p_value, float)
        assert 0 <= p_value <= 1
        
        # Step 7: Check significance
        is_significant = is_statistically_significant(p_value, alpha=0.05)
        # Just verify it returns something boolean-like (True or False)
        assert is_significant in [True, False]
        
        # Step 8: Verify summary works
        summary = experiment.get_summary()
        assert "integration_test" in summary
        assert "control" in summary
        assert "treatment" in summary
    
    def test_multi_variant_experiment(self):
        """Test experiment with more than 2 variants."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment_a", weight=1.0),
            Variant(name="treatment_b", weight=1.0),
            Variant(name="treatment_c", weight=1.0)
        ]
        
        experiment = Experiment(
            name="multi_variant_test",
            variants=variants,
            seed=123
        )
        
        # Assign many users
        for i in range(1000):
            variant = experiment.assign_variant(user_id=f"user_{i}")
            
            # Record some conversions
            if i % 10 == 0:
                experiment.record_conversion(variant.name)
        
        results = experiment.get_results()
        
        # Verify all variants got traffic
        assert len(results) == 4
        for variant_name in ["control", "treatment_a", "treatment_b", "treatment_c"]:
            assert variant_name in results
            assert results[variant_name]["exposures"] > 0
        
        # Check that traffic is roughly evenly distributed
        exposures = [results[v]["exposures"] for v in results]
        avg_exposure = sum(exposures) / len(exposures)
        
        for exposure in exposures:
            # Each variant should get roughly 25% (within 10% tolerance)
            assert 200 <= exposure <= 300
    
    def test_weighted_traffic_allocation(self):
        """Test that weighted traffic allocation works correctly."""
        variants = [
            Variant(name="control", weight=9.0),   # 90% traffic
            Variant(name="treatment", weight=1.0)  # 10% traffic
        ]
        
        experiment = Experiment(
            name="weighted_test",
            variants=variants,
            seed=456
        )
        
        # Assign many users
        for i in range(1000):
            experiment.assign_variant(user_id=f"user_{i}")
        
        results = experiment.get_results()
        
        control_exposures = results["control"]["exposures"]
        treatment_exposures = results["treatment"]["exposures"]
        
        # Control should get roughly 90% of traffic
        control_ratio = control_exposures / (control_exposures + treatment_exposures)
        
        assert 0.85 <= control_ratio <= 0.95  # Allow some variance
    
    def test_deterministic_assignment_consistency(self):
        """Test that deterministic assignment is consistent across experiments."""
        variants1 = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        
        variants2 = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        
        exp1 = Experiment("test1", variants1)
        exp2 = Experiment("test1", variants2)  # Same name
        
        # Same user_id and experiment name should give same variant
        user_ids = [f"user_{i}" for i in range(100)]
        
        for user_id in user_ids:
            v1 = exp1.assign_variant(user_id=user_id)
            v2 = exp2.assign_variant(user_id=user_id)
            assert v1.name == v2.name
