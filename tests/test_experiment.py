"""Tests for the experiment module."""

import pytest
from ab_testing.experiment import Experiment, Variant


class TestVariant:
    """Test cases for the Variant class."""
    
    def test_variant_initialization(self):
        """Test that a variant can be initialized correctly."""
        variant = Variant(name="control", weight=1.0)
        assert variant.name == "control"
        assert variant.weight == 1.0
        assert variant.conversions == 0
        assert variant.exposures == 0
        assert variant.conversion_rate == 0.0
    
    def test_conversion_rate_calculation(self):
        """Test that conversion rate is calculated correctly."""
        variant = Variant(name="control")
        variant.exposures = 100
        variant.conversions = 25
        assert variant.conversion_rate == 0.25
    
    def test_conversion_rate_zero_exposures(self):
        """Test that conversion rate is 0 when there are no exposures."""
        variant = Variant(name="control")
        assert variant.conversion_rate == 0.0
    
    def test_record_exposure(self):
        """Test that exposures are recorded correctly."""
        variant = Variant(name="control")
        variant.record_exposure()
        variant.record_exposure()
        assert variant.exposures == 2
    
    def test_record_conversion(self):
        """Test that conversions are recorded correctly."""
        variant = Variant(name="control")
        variant.record_conversion()
        variant.record_conversion()
        assert variant.conversions == 2


class TestExperiment:
    """Test cases for the Experiment class."""
    
    def test_experiment_initialization(self):
        """Test that an experiment can be initialized correctly."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        assert exp.name == "test_exp"
        assert len(exp.variants) == 2
    
    def test_experiment_requires_two_variants(self):
        """Test that an experiment requires at least 2 variants."""
        variants = [Variant(name="control")]
        with pytest.raises(ValueError, match="at least 2 variants"):
            Experiment(name="test_exp", variants=variants)
    
    def test_weight_normalization(self):
        """Test that variant weights are normalized correctly."""
        variants = [
            Variant(name="control", weight=2.0),
            Variant(name="treatment", weight=2.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        assert exp.variants[0].weight == 0.5
        assert exp.variants[1].weight == 0.5
    
    def test_assign_variant(self):
        """Test that variants are assigned."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants, seed=42)
        
        assigned = exp.assign_variant()
        assert assigned.name in ["control", "treatment"]
        assert assigned.exposures == 1
    
    def test_deterministic_assignment(self):
        """Test that deterministic assignment works correctly."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        
        # Same user_id should get same variant
        variant1 = exp.assign_variant(user_id="user123")
        variant2 = exp.assign_variant(user_id="user123")
        assert variant1.name == variant2.name
    
    def test_record_conversion(self):
        """Test that conversions are recorded correctly."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        
        result = exp.record_conversion("control")
        assert result is True
        assert exp.get_variant("control").conversions == 1
    
    def test_record_conversion_invalid_variant(self):
        """Test that recording conversion for invalid variant returns False."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        
        result = exp.record_conversion("invalid")
        assert result is False
    
    def test_get_variant(self):
        """Test that variants can be retrieved by name."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        
        variant = exp.get_variant("control")
        assert variant is not None
        assert variant.name == "control"
        
        variant = exp.get_variant("invalid")
        assert variant is None
    
    def test_get_results(self):
        """Test that experiment results are returned correctly."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        
        exp.assign_variant()
        exp.record_conversion("control")
        
        results = exp.get_results()
        assert "control" in results
        assert "treatment" in results
        assert "exposures" in results["control"]
        assert "conversions" in results["control"]
        assert "conversion_rate" in results["control"]
    
    def test_get_summary(self):
        """Test that experiment summary is generated correctly."""
        variants = [
            Variant(name="control", weight=1.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants)
        
        summary = exp.get_summary()
        assert "test_exp" in summary
        assert "control" in summary
        assert "treatment" in summary
    
    def test_weighted_assignment_distribution(self):
        """Test that weighted assignment produces expected distribution."""
        variants = [
            Variant(name="control", weight=3.0),
            Variant(name="treatment", weight=1.0)
        ]
        exp = Experiment(name="test_exp", variants=variants, seed=42)
        
        # Assign many variants
        for _ in range(1000):
            exp.assign_variant()
        
        control = exp.get_variant("control")
        treatment = exp.get_variant("treatment")
        
        # Control should have roughly 75% of assignments
        control_ratio = control.exposures / (control.exposures + treatment.exposures)
        assert 0.7 <= control_ratio <= 0.8  # Allow some variance
