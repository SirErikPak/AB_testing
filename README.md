# A/B Testing Library

A comprehensive Python library for conducting A/B tests and analyzing statistical significance. This library provides tools for experiment management, variant assignment, and statistical analysis.

## Features

- **Experiment Management**: Easy setup and management of A/B tests with multiple variants
- **Variant Assignment**: Support for both random and deterministic user assignment
- **Statistical Analysis**: Built-in functions for:
  - Z-test for proportions (comparing conversion rates)
  - T-test for means (comparing continuous metrics)
  - Chi-square test (analyzing categorical data)
  - Confidence interval calculation (Wilson score method)
  - Sample size calculation
- **Flexible Weighting**: Support for unequal traffic allocation across variants
- **Comprehensive Testing**: Well-tested with 41+ unit tests

## Installation

```bash
pip install -e .
```

For development (includes testing tools):

```bash
pip install -r requirements-dev.txt
```

## Quick Start

### Basic A/B Test

```python
from ab_testing import Experiment, Variant, z_test_proportions

# Create an experiment with two variants
variants = [
    Variant(name="control", weight=1.0),
    Variant(name="treatment", weight=1.0)
]

experiment = Experiment(
    name="button_color_test",
    variants=variants,
    seed=42  # Optional: for reproducibility
)

# Assign users to variants
for user_id in user_ids:
    variant = experiment.assign_variant(user_id=user_id)
    
    # Show the variant to the user and track if they convert
    if user_converted:
        experiment.record_conversion(variant.name)

# Get results
results = experiment.get_results()
print(results)

# Perform statistical test
control = experiment.get_variant("control")
treatment = experiment.get_variant("treatment")

z_score, p_value, se = z_test_proportions(
    conversions_a=control.conversions,
    exposures_a=control.exposures,
    conversions_b=treatment.conversions,
    exposures_b=treatment.exposures
)

print(f"P-value: {p_value:.4f}")
if p_value < 0.05:
    print("Result is statistically significant!")
```

### Calculate Required Sample Size

```python
from ab_testing import calculate_sample_size

# Calculate how many users you need per variant
sample_size = calculate_sample_size(
    baseline_rate=0.10,        # Current conversion rate (10%)
    minimum_detectable_effect=0.20,  # Want to detect 20% relative change
    alpha=0.05,                # 5% significance level
    power=0.8                  # 80% statistical power
)

print(f"You need {sample_size} users per variant")
```

### Calculate Confidence Intervals

```python
from ab_testing import calculate_confidence_interval

lower, upper = calculate_confidence_interval(
    conversions=100,
    exposures=1000,
    confidence_level=0.95
)

print(f"95% CI: [{lower:.2%}, {upper:.2%}]")
```

## Core Classes

### Variant

Represents a single variant in an A/B test.

```python
from ab_testing import Variant

variant = Variant(
    name="treatment",
    weight=1.0,  # Relative weight for traffic allocation
    metadata={"color": "blue", "size": "large"}  # Optional metadata
)

# Properties
print(variant.conversion_rate)  # Calculated conversion rate
print(variant.exposures)        # Number of users shown this variant
print(variant.conversions)      # Number of users who converted
```

### Experiment

Main class for managing A/B tests.

```python
from ab_testing import Experiment, Variant

# Create experiment with multiple variants
variants = [
    Variant(name="control", weight=1.0),
    Variant(name="treatment_a", weight=1.0),
    Variant(name="treatment_b", weight=1.0)
]

experiment = Experiment(name="multi_variant_test", variants=variants)

# Assign variants
variant = experiment.assign_variant(user_id="user123")  # Deterministic
variant = experiment.assign_variant()  # Random

# Record conversions
experiment.record_conversion("treatment_a")

# Get results
results = experiment.get_results()
summary = experiment.get_summary()
```

## Statistical Functions

### Z-Test for Proportions

Compare conversion rates between two variants:

```python
from ab_testing import z_test_proportions

z_score, p_value, std_error = z_test_proportions(
    conversions_a=50,
    exposures_a=1000,
    conversions_b=60,
    exposures_b=1000,
    two_tailed=True
)
```

### T-Test for Means

Compare continuous metrics (e.g., revenue, time on site):

```python
from ab_testing import t_test_means

values_a = [10.5, 12.3, 9.8, ...]  # Control group values
values_b = [11.2, 13.1, 10.5, ...]  # Treatment group values

t_statistic, p_value = t_test_means(values_a, values_b)
```

### Chi-Square Test

Test independence between categorical variables:

```python
from ab_testing import chi_square_test

contingency_table = [
    [50, 950],   # Control: conversions, non-conversions
    [60, 940]    # Treatment: conversions, non-conversions
]

chi2, p_value, dof = chi_square_test(contingency_table)
```

### Calculate Relative Uplift

```python
from ab_testing import calculate_relative_uplift

uplift = calculate_relative_uplift(
    control_rate=0.10,
    treatment_rate=0.12
)
print(f"Uplift: {uplift:.1%}")  # 20.0% uplift
```

## Examples

The `examples/` directory contains several complete examples:

- **simple_ab_test.py**: Basic A/B test with variant assignment and analysis
- **sample_size_calculator.py**: Calculate required sample sizes for different scenarios
- **confidence_intervals.py**: Understanding confidence intervals with different sample sizes

Run an example:

```bash
python examples/simple_ab_test.py
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=ab_testing --cov-report=html
```

## Best Practices

1. **Pre-calculate sample size**: Use `calculate_sample_size()` to determine how long to run your test
2. **Use deterministic assignment**: Pass `user_id` to `assign_variant()` for consistent user experience
3. **Check statistical significance**: Don't stop tests early; wait for p < 0.05
4. **Consider practical significance**: A statistically significant result may not be practically meaningful
5. **Use confidence intervals**: They provide more information than just p-values
6. **Avoid peeking**: Don't repeatedly check results during the test (increases false positive rate)

## Statistical Concepts

### Statistical Significance

A result is statistically significant when p-value < α (typically 0.05). This means there's less than a 5% chance the observed difference occurred by random chance.

### Statistical Power

Power (typically 0.8 or 80%) is the probability of detecting a true effect. Higher power requires larger sample sizes.

### Confidence Intervals

A 95% confidence interval means we're 95% confident the true conversion rate falls within that range. Narrower intervals indicate more precise estimates.

### Minimum Detectable Effect (MDE)

The smallest relative change you want to be able to detect. Smaller MDEs require larger sample sizes.

## Requirements

- Python >= 3.7
- numpy >= 1.20.0
- scipy >= 1.7.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.