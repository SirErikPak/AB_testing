"""
Sample size calculator example.

This example demonstrates how to calculate the required sample size
for an A/B test given baseline metrics and desired effect size.
"""

from ab_testing import calculate_sample_size


def main():
    print("=" * 60)
    print("Sample Size Calculator Example")
    print("=" * 60)
    print()
    
    # Scenario 1: E-commerce conversion rate test
    print("Scenario 1: E-commerce Conversion Rate Test")
    print("-" * 60)
    print("Current conversion rate: 5%")
    print("Minimum detectable effect: 20% (relative increase)")
    print("Significance level (alpha): 5%")
    print("Statistical power: 80%")
    print()
    
    n1 = calculate_sample_size(
        baseline_rate=0.05,
        minimum_detectable_effect=0.20,
        alpha=0.05,
        power=0.8
    )
    
    print(f"Required sample size per variant: {n1:,}")
    print(f"Total sample size needed: {n1 * 2:,}")
    print()
    
    # Scenario 2: Email click-through rate test
    print("Scenario 2: Email Click-Through Rate Test")
    print("-" * 60)
    print("Current click-through rate: 2%")
    print("Minimum detectable effect: 50% (relative increase)")
    print("Significance level (alpha): 5%")
    print("Statistical power: 80%")
    print()
    
    n2 = calculate_sample_size(
        baseline_rate=0.02,
        minimum_detectable_effect=0.50,
        alpha=0.05,
        power=0.8
    )
    
    print(f"Required sample size per variant: {n2:,}")
    print(f"Total sample size needed: {n2 * 2:,}")
    print()
    
    # Scenario 3: High-traffic website
    print("Scenario 3: High-Traffic Website Test")
    print("-" * 60)
    print("Current conversion rate: 10%")
    print("Minimum detectable effect: 10% (relative increase)")
    print("Significance level (alpha): 5%")
    print("Statistical power: 80%")
    print()
    
    n3 = calculate_sample_size(
        baseline_rate=0.10,
        minimum_detectable_effect=0.10,
        alpha=0.05,
        power=0.8
    )
    
    print(f"Required sample size per variant: {n3:,}")
    print(f"Total sample size needed: {n3 * 2:,}")
    print()
    
    # Effect of power on sample size
    print("Effect of Statistical Power on Sample Size")
    print("-" * 60)
    print("Baseline rate: 5%, MDE: 20%")
    print()
    
    for power in [0.7, 0.8, 0.9]:
        n = calculate_sample_size(
            baseline_rate=0.05,
            minimum_detectable_effect=0.20,
            alpha=0.05,
            power=power
        )
        print(f"Power {power:.0%}: {n:,} samples per variant")
    
    print()
    print("Note: Higher power requires larger sample sizes")
    print("      but reduces the risk of false negatives (Type II error)")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
