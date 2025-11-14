"""
Confidence intervals example.

This example demonstrates how to calculate and interpret confidence
intervals for conversion rates in A/B tests.
"""

from ab_testing import Experiment, Variant, calculate_confidence_interval


def main():
    print("=" * 60)
    print("Confidence Intervals Example")
    print("=" * 60)
    print()
    
    # Create an experiment
    variants = [
        Variant(name="control", weight=1.0),
        Variant(name="treatment", weight=1.0)
    ]
    
    experiment = Experiment(
        name="landing_page_test",
        variants=variants,
        seed=42
    )
    
    # Simulate data with different sample sizes
    import random
    
    # Small sample (100 users per variant)
    print("Scenario 1: Small Sample Size (100 users per variant)")
    print("-" * 60)
    
    exp_small = Experiment(
        name="small_test",
        variants=[Variant(name="A"), Variant(name="B")],
        seed=42
    )
    
    for i in range(200):
        variant = exp_small.assign_variant(user_id=f"user_{i}")
        random.seed(i)
        if random.random() < 0.10:
            exp_small.record_conversion(variant.name)
    
    for variant in exp_small.variants:
        lower, upper = calculate_confidence_interval(
            conversions=variant.conversions,
            exposures=variant.exposures,
            confidence_level=0.95
        )
        print(f"{variant.name}:")
        print(f"  Conversion Rate: {variant.conversion_rate:.2%}")
        print(f"  95% CI: [{lower:.2%}, {upper:.2%}]")
        print(f"  CI Width: {(upper - lower):.2%}")
        print()
    
    # Medium sample (1000 users per variant)
    print("Scenario 2: Medium Sample Size (1000 users per variant)")
    print("-" * 60)
    
    exp_medium = Experiment(
        name="medium_test",
        variants=[Variant(name="A"), Variant(name="B")],
        seed=42
    )
    
    for i in range(2000):
        variant = exp_medium.assign_variant(user_id=f"user_{i}")
        random.seed(i)
        if random.random() < 0.10:
            exp_medium.record_conversion(variant.name)
    
    for variant in exp_medium.variants:
        lower, upper = calculate_confidence_interval(
            conversions=variant.conversions,
            exposures=variant.exposures,
            confidence_level=0.95
        )
        print(f"{variant.name}:")
        print(f"  Conversion Rate: {variant.conversion_rate:.2%}")
        print(f"  95% CI: [{lower:.2%}, {upper:.2%}]")
        print(f"  CI Width: {(upper - lower):.2%}")
        print()
    
    # Large sample (10000 users per variant)
    print("Scenario 3: Large Sample Size (10000 users per variant)")
    print("-" * 60)
    
    exp_large = Experiment(
        name="large_test",
        variants=[Variant(name="A"), Variant(name="B")],
        seed=42
    )
    
    for i in range(20000):
        variant = exp_large.assign_variant(user_id=f"user_{i}")
        random.seed(i)
        if random.random() < 0.10:
            exp_large.record_conversion(variant.name)
    
    for variant in exp_large.variants:
        lower, upper = calculate_confidence_interval(
            conversions=variant.conversions,
            exposures=variant.exposures,
            confidence_level=0.95
        )
        print(f"{variant.name}:")
        print(f"  Conversion Rate: {variant.conversion_rate:.2%}")
        print(f"  95% CI: [{lower:.2%}, {upper:.2%}]")
        print(f"  CI Width: {(upper - lower):.2%}")
        print()
    
    print("Observation:")
    print("  As sample size increases, confidence intervals become narrower,")
    print("  providing more precise estimates of the true conversion rate.")
    print()
    
    # Different confidence levels
    print("Scenario 4: Different Confidence Levels")
    print("-" * 60)
    
    conversions = 100
    exposures = 1000
    rate = conversions / exposures
    
    print(f"Conversion Rate: {rate:.2%} ({conversions}/{exposures})")
    print()
    
    for conf_level in [0.90, 0.95, 0.99]:
        lower, upper = calculate_confidence_interval(
            conversions=conversions,
            exposures=exposures,
            confidence_level=conf_level
        )
        print(f"{conf_level:.0%} Confidence Interval: [{lower:.2%}, {upper:.2%}]")
    
    print()
    print("Observation:")
    print("  Higher confidence levels result in wider intervals,")
    print("  trading precision for increased certainty.")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
