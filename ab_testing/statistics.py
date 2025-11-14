"""
Statistical analysis module for A/B testing.

This module provides functions for statistical hypothesis testing and
power analysis for A/B tests.
"""

import math
from typing import Tuple, Optional
from scipy import stats
import numpy as np


def z_test_proportions(
    conversions_a: int,
    exposures_a: int,
    conversions_b: int,
    exposures_b: int,
    two_tailed: bool = True
) -> Tuple[float, float, float]:
    """Perform a Z-test for proportions.
    
    Tests whether the conversion rates of two variants are significantly different.
    
    Args:
        conversions_a: Number of conversions in variant A
        exposures_a: Number of exposures in variant A
        conversions_b: Number of conversions in variant B
        exposures_b: Number of exposures in variant B
        two_tailed: Whether to perform a two-tailed test
    
    Returns:
        Tuple of (z_score, p_value, pooled_std_error)
    
    Raises:
        ValueError: If exposures are zero or negative
    """
    if exposures_a <= 0 or exposures_b <= 0:
        raise ValueError("Exposures must be positive")
    
    # Calculate conversion rates
    p_a = conversions_a / exposures_a
    p_b = conversions_b / exposures_b
    
    # Calculate pooled proportion
    p_pooled = (conversions_a + conversions_b) / (exposures_a + exposures_b)
    
    # Calculate standard error
    se = math.sqrt(p_pooled * (1 - p_pooled) * (1/exposures_a + 1/exposures_b))
    
    if se == 0:
        return (0.0, 1.0, 0.0)
    
    # Calculate z-score
    z_score = (p_a - p_b) / se
    
    # Calculate p-value
    if two_tailed:
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    else:
        p_value = 1 - stats.norm.cdf(z_score)
    
    return (z_score, p_value, se)


def t_test_means(
    values_a: list,
    values_b: list,
    equal_var: bool = True
) -> Tuple[float, float]:
    """Perform a t-test for means.
    
    Tests whether the means of two samples are significantly different.
    Useful for comparing continuous metrics like revenue or time spent.
    
    Args:
        values_a: List of values from variant A
        values_b: List of values from variant B
        equal_var: Whether to assume equal variance (default: True)
    
    Returns:
        Tuple of (t_statistic, p_value)
    
    Raises:
        ValueError: If samples are too small
    """
    if len(values_a) < 2 or len(values_b) < 2:
        raise ValueError("Each sample must have at least 2 values")
    
    t_statistic, p_value = stats.ttest_ind(values_a, values_b, equal_var=equal_var)
    
    return (float(t_statistic), float(p_value))


def chi_square_test(
    contingency_table: list
) -> Tuple[float, float, int]:
    """Perform a chi-square test for independence.
    
    Tests whether there is a significant relationship between categorical variables.
    
    Args:
        contingency_table: 2D list representing the contingency table
                          Example: [[conversions_a, non_conversions_a],
                                   [conversions_b, non_conversions_b]]
    
    Returns:
        Tuple of (chi2_statistic, p_value, degrees_of_freedom)
    
    Raises:
        ValueError: If table is not properly formatted
    """
    if len(contingency_table) < 2 or len(contingency_table[0]) < 2:
        raise ValueError("Contingency table must be at least 2x2")
    
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    return (float(chi2), float(p_value), int(dof))


def calculate_sample_size(
    baseline_rate: float,
    minimum_detectable_effect: float,
    alpha: float = 0.05,
    power: float = 0.8,
    two_tailed: bool = True
) -> int:
    """Calculate required sample size per variant for an A/B test.
    
    Args:
        baseline_rate: Expected conversion rate of control group (0 to 1)
        minimum_detectable_effect: Minimum relative effect to detect (e.g., 0.1 for 10%)
        alpha: Significance level (default: 0.05)
        power: Statistical power (default: 0.8)
        two_tailed: Whether test is two-tailed (default: True)
    
    Returns:
        Required sample size per variant
    
    Raises:
        ValueError: If parameters are out of valid range
    """
    if not 0 < baseline_rate < 1:
        raise ValueError("Baseline rate must be between 0 and 1")
    if minimum_detectable_effect <= 0:
        raise ValueError("Minimum detectable effect must be positive")
    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between 0 and 1")
    if not 0 < power < 1:
        raise ValueError("Power must be between 0 and 1")
    
    # Calculate treatment rate
    treatment_rate = baseline_rate * (1 + minimum_detectable_effect)
    
    if treatment_rate >= 1:
        raise ValueError("Treatment rate would exceed 1")
    
    # Z-scores
    if two_tailed:
        z_alpha = stats.norm.ppf(1 - alpha / 2)
    else:
        z_alpha = stats.norm.ppf(1 - alpha)
    
    z_beta = stats.norm.ppf(power)
    
    # Calculate sample size using standard formula
    p1 = baseline_rate
    p2 = treatment_rate
    p_avg = (p1 + p2) / 2
    
    numerator = (z_alpha * math.sqrt(2 * p_avg * (1 - p_avg)) +
                z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2
    
    n = numerator / denominator
    
    return int(math.ceil(n))


def calculate_confidence_interval(
    conversions: int,
    exposures: int,
    confidence_level: float = 0.95
) -> Tuple[float, float]:
    """Calculate confidence interval for a proportion.
    
    Uses the Wilson score interval method for better accuracy with small samples.
    
    Args:
        conversions: Number of conversions
        exposures: Number of exposures
        confidence_level: Confidence level (default: 0.95)
    
    Returns:
        Tuple of (lower_bound, upper_bound)
    
    Raises:
        ValueError: If parameters are invalid
    """
    if exposures <= 0:
        raise ValueError("Exposures must be positive")
    if conversions < 0 or conversions > exposures:
        raise ValueError("Conversions must be between 0 and exposures")
    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1")
    
    p = conversions / exposures
    n = exposures
    
    # Wilson score interval
    z = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    z_squared = z ** 2
    
    denominator = 1 + z_squared / n
    center = (p + z_squared / (2 * n)) / denominator
    margin = z * math.sqrt(p * (1 - p) / n + z_squared / (4 * n ** 2)) / denominator
    
    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    
    return (lower, upper)


def calculate_relative_uplift(
    control_rate: float,
    treatment_rate: float
) -> float:
    """Calculate the relative uplift from control to treatment.
    
    Args:
        control_rate: Conversion rate of control variant
        treatment_rate: Conversion rate of treatment variant
    
    Returns:
        Relative uplift as a decimal (e.g., 0.15 for 15% uplift)
    
    Raises:
        ValueError: If control_rate is zero
    """
    if control_rate == 0:
        raise ValueError("Control rate cannot be zero")
    
    return (treatment_rate - control_rate) / control_rate


def is_statistically_significant(
    p_value: float,
    alpha: float = 0.05
) -> bool:
    """Check if a result is statistically significant.
    
    Args:
        p_value: The p-value from a statistical test
        alpha: The significance level (default: 0.05)
    
    Returns:
        True if result is statistically significant, False otherwise
    """
    return p_value < alpha
