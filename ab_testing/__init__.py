"""
A/B Testing Library

A Python library for conducting A/B tests and analyzing statistical significance.
"""

from .experiment import Experiment, Variant
from .statistics import (
    z_test_proportions,
    t_test_means,
    chi_square_test,
    calculate_sample_size,
    calculate_confidence_interval,
    calculate_relative_uplift,
    is_statistically_significant,
)

__version__ = "0.1.0"
__all__ = [
    "Experiment",
    "Variant",
    "z_test_proportions",
    "t_test_means",
    "chi_square_test",
    "calculate_sample_size",
    "calculate_confidence_interval",
    "calculate_relative_uplift",
    "is_statistically_significant",
]
