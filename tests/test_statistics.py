"""Tests for the statistics module."""

import pytest
import math
from ab_testing.statistics import (
    z_test_proportions,
    t_test_means,
    chi_square_test,
    calculate_sample_size,
    calculate_confidence_interval,
    calculate_relative_uplift,
    is_statistically_significant,
)


class TestZTestProportions:
    """Test cases for z_test_proportions."""
    
    def test_z_test_proportions_basic(self):
        """Test basic z-test for proportions."""
        z_score, p_value, se = z_test_proportions(
            conversions_a=50,
            exposures_a=1000,
            conversions_b=60,
            exposures_b=1000
        )
        
        assert isinstance(z_score, float)
        assert isinstance(p_value, float)
        assert isinstance(se, float)
        assert 0 <= p_value <= 1
    
    def test_z_test_identical_rates(self):
        """Test z-test with identical conversion rates."""
        z_score, p_value, se = z_test_proportions(
            conversions_a=50,
            exposures_a=1000,
            conversions_b=50,
            exposures_b=1000
        )
        
        assert abs(z_score) < 0.01  # Should be close to 0
        assert p_value > 0.9  # Should be high (not significant)
    
    def test_z_test_zero_exposures(self):
        """Test that zero exposures raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            z_test_proportions(
                conversions_a=0,
                exposures_a=0,
                conversions_b=50,
                exposures_b=1000
            )
    
    def test_z_test_significant_difference(self):
        """Test z-test with significant difference."""
        z_score, p_value, se = z_test_proportions(
            conversions_a=100,
            exposures_a=1000,
            conversions_b=200,
            exposures_b=1000
        )
        
        assert p_value < 0.05  # Should be significant


class TestTTestMeans:
    """Test cases for t_test_means."""
    
    def test_t_test_means_basic(self):
        """Test basic t-test for means."""
        values_a = [1, 2, 3, 4, 5]
        values_b = [2, 3, 4, 5, 6]
        
        t_stat, p_value = t_test_means(values_a, values_b)
        
        assert isinstance(t_stat, float)
        assert isinstance(p_value, float)
        assert 0 <= p_value <= 1
    
    def test_t_test_identical_samples(self):
        """Test t-test with identical samples."""
        values_a = [1, 2, 3, 4, 5]
        values_b = [1, 2, 3, 4, 5]
        
        t_stat, p_value = t_test_means(values_a, values_b)
        
        assert abs(t_stat) < 0.01  # Should be close to 0
        assert p_value > 0.9  # Should be high (not significant)
    
    def test_t_test_small_samples(self):
        """Test that small samples raise ValueError."""
        values_a = [1]
        values_b = [2, 3]
        
        with pytest.raises(ValueError, match="at least 2 values"):
            t_test_means(values_a, values_b)
    
    def test_t_test_significant_difference(self):
        """Test t-test with significant difference."""
        values_a = [1, 2, 3, 4, 5] * 20
        values_b = [10, 11, 12, 13, 14] * 20
        
        t_stat, p_value = t_test_means(values_a, values_b)
        
        assert p_value < 0.05  # Should be significant


class TestChiSquareTest:
    """Test cases for chi_square_test."""
    
    def test_chi_square_basic(self):
        """Test basic chi-square test."""
        contingency_table = [
            [50, 950],
            [60, 940]
        ]
        
        chi2, p_value, dof = chi_square_test(contingency_table)
        
        assert isinstance(chi2, float)
        assert isinstance(p_value, float)
        assert isinstance(dof, int)
        assert 0 <= p_value <= 1
        assert dof == 1
    
    def test_chi_square_invalid_table(self):
        """Test that invalid table raises ValueError."""
        with pytest.raises(ValueError, match="at least 2x2"):
            chi_square_test([[1]])


class TestCalculateSampleSize:
    """Test cases for calculate_sample_size."""
    
    def test_sample_size_basic(self):
        """Test basic sample size calculation."""
        n = calculate_sample_size(
            baseline_rate=0.1,
            minimum_detectable_effect=0.2
        )
        
        assert isinstance(n, int)
        assert n > 0
    
    def test_sample_size_invalid_baseline(self):
        """Test that invalid baseline rate raises ValueError."""
        with pytest.raises(ValueError, match="between 0 and 1"):
            calculate_sample_size(
                baseline_rate=1.5,
                minimum_detectable_effect=0.2
            )
    
    def test_sample_size_negative_effect(self):
        """Test that negative effect raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            calculate_sample_size(
                baseline_rate=0.1,
                minimum_detectable_effect=-0.1
            )
    
    def test_sample_size_larger_effect_smaller_sample(self):
        """Test that larger effect requires smaller sample size."""
        n1 = calculate_sample_size(
            baseline_rate=0.1,
            minimum_detectable_effect=0.1
        )
        n2 = calculate_sample_size(
            baseline_rate=0.1,
            minimum_detectable_effect=0.3
        )
        
        assert n2 < n1


class TestCalculateConfidenceInterval:
    """Test cases for calculate_confidence_interval."""
    
    def test_confidence_interval_basic(self):
        """Test basic confidence interval calculation."""
        lower, upper = calculate_confidence_interval(
            conversions=50,
            exposures=1000
        )
        
        assert isinstance(lower, float)
        assert isinstance(upper, float)
        assert 0 <= lower <= 1
        assert 0 <= upper <= 1
        assert lower <= upper
    
    def test_confidence_interval_contains_rate(self):
        """Test that confidence interval contains the conversion rate."""
        conversions = 50
        exposures = 1000
        rate = conversions / exposures
        
        lower, upper = calculate_confidence_interval(conversions, exposures)
        
        assert lower <= rate <= upper
    
    def test_confidence_interval_zero_conversions(self):
        """Test confidence interval with zero conversions."""
        lower, upper = calculate_confidence_interval(
            conversions=0,
            exposures=1000
        )
        
        assert lower < 0.001  # Very close to 0
        assert upper > 0
    
    def test_confidence_interval_all_conversions(self):
        """Test confidence interval with all conversions."""
        lower, upper = calculate_confidence_interval(
            conversions=1000,
            exposures=1000
        )
        
        assert lower < 1
        assert upper == 1
    
    def test_confidence_interval_invalid_conversions(self):
        """Test that invalid conversions raise ValueError."""
        with pytest.raises(ValueError, match="between 0 and exposures"):
            calculate_confidence_interval(
                conversions=1100,
                exposures=1000
            )


class TestCalculateRelativeUplift:
    """Test cases for calculate_relative_uplift."""
    
    def test_relative_uplift_positive(self):
        """Test positive relative uplift."""
        uplift = calculate_relative_uplift(
            control_rate=0.1,
            treatment_rate=0.12
        )
        
        assert abs(uplift - 0.2) < 0.01  # 20% uplift
    
    def test_relative_uplift_negative(self):
        """Test negative relative uplift."""
        uplift = calculate_relative_uplift(
            control_rate=0.1,
            treatment_rate=0.08
        )
        
        assert uplift < 0  # Negative uplift
    
    def test_relative_uplift_zero_control(self):
        """Test that zero control rate raises ValueError."""
        with pytest.raises(ValueError, match="cannot be zero"):
            calculate_relative_uplift(
                control_rate=0.0,
                treatment_rate=0.1
            )


class TestIsStatisticallySignificant:
    """Test cases for is_statistically_significant."""
    
    def test_significant_result(self):
        """Test that p-value < alpha is significant."""
        assert is_statistically_significant(0.01, alpha=0.05) is True
    
    def test_not_significant_result(self):
        """Test that p-value >= alpha is not significant."""
        assert is_statistically_significant(0.1, alpha=0.05) is False
    
    def test_borderline_case(self):
        """Test borderline p-value."""
        assert is_statistically_significant(0.05, alpha=0.05) is False
