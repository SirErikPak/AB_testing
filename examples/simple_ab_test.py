"""
Simple A/B test example.

This example demonstrates how to set up a basic A/B test,
assign users to variants, record conversions, and analyze results.
"""

from ab_testing import Experiment, Variant, z_test_proportions


def main():
    print("=" * 60)
    print("Simple A/B Test Example")
    print("=" * 60)
    print()
    
    # Create an experiment with two variants
    variants = [
        Variant(name="control", weight=1.0),
        Variant(name="treatment", weight=1.0)
    ]
    
    experiment = Experiment(
        name="button_color_test",
        variants=variants,
        seed=42  # For reproducibility
    )
    
    print("Experiment created: button_color_test")
    print(f"Variants: {[v.name for v in variants]}")
    print()
    
    # Simulate user assignments
    print("Simulating user assignments...")
    num_users = 1000
    
    for i in range(num_users):
        user_id = f"user_{i}"
        
        # Assign user to a variant
        variant = experiment.assign_variant(user_id=user_id)
        
        # Simulate conversion (control: 10%, treatment: 12%)
        import random
        random.seed(i)
        
        if variant.name == "control":
            if random.random() < 0.10:
                experiment.record_conversion("control")
        else:  # treatment
            if random.random() < 0.12:
                experiment.record_conversion("treatment")
    
    print(f"Assigned {num_users} users to variants")
    print()
    
    # Get results
    results = experiment.get_results()
    
    print("Results:")
    print("-" * 60)
    for variant_name, stats in results.items():
        print(f"{variant_name.upper()}:")
        print(f"  Exposures: {stats['exposures']}")
        print(f"  Conversions: {stats['conversions']}")
        print(f"  Conversion Rate: {stats['conversion_rate']:.2%}")
        print()
    
    # Perform statistical test
    control = experiment.get_variant("control")
    treatment = experiment.get_variant("treatment")
    
    z_score, p_value, se = z_test_proportions(
        conversions_a=control.conversions,
        exposures_a=control.exposures,
        conversions_b=treatment.conversions,
        exposures_b=treatment.exposures
    )
    
    print("Statistical Analysis:")
    print("-" * 60)
    print(f"Z-score: {z_score:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Standard Error: {se:.4f}")
    print()
    
    if p_value < 0.05:
        print("✓ Result is STATISTICALLY SIGNIFICANT (p < 0.05)")
        uplift = ((treatment.conversion_rate - control.conversion_rate) / 
                  control.conversion_rate * 100)
        print(f"  Treatment variant shows a {uplift:.1f}% uplift over control")
    else:
        print("✗ Result is NOT statistically significant (p >= 0.05)")
        print("  Continue the test or increase sample size")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
