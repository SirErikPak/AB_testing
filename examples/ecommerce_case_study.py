"""
E-commerce A/B Test Case Study.

This example demonstrates a realistic A/B test scenario for an e-commerce website
testing a new checkout flow.
"""

from ab_testing import (
    Experiment, 
    Variant, 
    z_test_proportions,
    calculate_confidence_interval,
    calculate_relative_uplift
)


def main():
    print("=" * 70)
    print("E-commerce A/B Test: New Checkout Flow")
    print("=" * 70)
    print()
    
    print("Scenario:")
    print("  We want to test if a simplified checkout flow increases conversions")
    print("  compared to the current multi-step checkout process.")
    print()
    
    # Create experiment
    variants = [
        Variant(
            name="control",
            weight=1.0,
            metadata={"description": "Current multi-step checkout"}
        ),
        Variant(
            name="treatment",
            weight=1.0,
            metadata={"description": "New simplified single-page checkout"}
        )
    ]
    
    experiment = Experiment(
        name="checkout_simplification",
        variants=variants,
        seed=12345
    )
    
    print("Test Setup:")
    print("  Control: Current multi-step checkout")
    print("  Treatment: New simplified single-page checkout")
    print("  Traffic Split: 50/50")
    print()
    
    # Simulate 2 weeks of traffic
    import random
    
    # Realistic conversion rates
    # Control: 3.5% (typical e-commerce conversion)
    # Treatment: 4.2% (20% relative improvement)
    
    print("Simulating 2 weeks of traffic...")
    num_visitors = 5000  # Realistic weekly traffic per variant
    
    for i in range(num_visitors):
        user_id = f"visitor_{i}"
        variant = experiment.assign_variant(user_id=user_id)
        
        # Simulate checkout behavior
        random.seed(i)
        
        if variant.name == "control":
            # Current checkout: 3.5% conversion
            if random.random() < 0.035:
                experiment.record_conversion("control")
        else:
            # New checkout: 4.2% conversion
            if random.random() < 0.042:
                experiment.record_conversion("treatment")
    
    print(f"✓ Collected data from {num_visitors} visitors per variant")
    print()
    
    # Analyze results
    print("=" * 70)
    print("Results")
    print("=" * 70)
    print()
    
    control = experiment.get_variant("control")
    treatment = experiment.get_variant("treatment")
    
    # Display metrics for each variant
    for variant in [control, treatment]:
        print(f"{variant.name.upper()}: {variant.metadata['description']}")
        print(f"  Visitors: {variant.exposures:,}")
        print(f"  Conversions: {variant.conversions}")
        print(f"  Conversion Rate: {variant.conversion_rate:.2%}")
        
        # Calculate confidence interval
        ci_lower, ci_upper = calculate_confidence_interval(
            variant.conversions,
            variant.exposures,
            confidence_level=0.95
        )
        print(f"  95% CI: [{ci_lower:.2%}, {ci_upper:.2%}]")
        print()
    
    # Statistical test
    print("=" * 70)
    print("Statistical Analysis")
    print("=" * 70)
    print()
    
    z_score, p_value, se = z_test_proportions(
        control.conversions,
        control.exposures,
        treatment.conversions,
        treatment.exposures
    )
    
    print(f"Z-score: {z_score:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Standard Error: {se:.4f}")
    print()
    
    # Calculate uplift
    if control.conversion_rate > 0:
        relative_uplift = calculate_relative_uplift(
            control.conversion_rate,
            treatment.conversion_rate
        )
        print(f"Relative Uplift: {relative_uplift:+.1%}")
        
        if treatment.conversion_rate > control.conversion_rate:
            print(f"  → Treatment performs {abs(relative_uplift):.1%} better than control")
        else:
            print(f"  → Treatment performs {abs(relative_uplift):.1%} worse than control")
    print()
    
    # Decision
    print("=" * 70)
    print("Recommendation")
    print("=" * 70)
    print()
    
    if p_value < 0.05:
        print("✓ STATISTICALLY SIGNIFICANT (p < 0.05)")
        print()
        
        if treatment.conversion_rate > control.conversion_rate:
            print("RECOMMENDATION: Launch the new simplified checkout flow")
            print()
            print("Expected Impact:")
            
            # Calculate business impact
            avg_order_value = 85.00  # Example AOV
            monthly_visitors = num_visitors * 4  # 4 weeks
            
            control_revenue = monthly_visitors * control.conversion_rate * avg_order_value
            treatment_revenue = monthly_visitors * treatment.conversion_rate * avg_order_value
            additional_revenue = treatment_revenue - control_revenue
            
            print(f"  • Current monthly revenue (per variant): ${control_revenue:,.2f}")
            print(f"  • Projected monthly revenue: ${treatment_revenue:,.2f}")
            print(f"  • Additional monthly revenue: ${additional_revenue:,.2f}")
            print(f"  • Annual revenue increase: ${additional_revenue * 12:,.2f}")
        else:
            print("RECOMMENDATION: Keep the current checkout flow")
            print()
            print("The new checkout flow showed lower conversion rates.")
            print("Consider alternative improvements or testing different variations.")
    else:
        print("✗ NOT STATISTICALLY SIGNIFICANT (p >= 0.05)")
        print()
        print("RECOMMENDATION: Continue the test or increase sample size")
        print()
        print("Options:")
        print("  1. Run the test longer to collect more data")
        print("  2. Increase traffic allocation to the test")
        print("  3. Re-evaluate the hypothesis and test design")
        
        # Show how much more traffic is needed
        from ab_testing import calculate_sample_size
        
        if control.conversion_rate > 0:
            required_n = calculate_sample_size(
                baseline_rate=control.conversion_rate,
                minimum_detectable_effect=0.20,  # Want to detect 20% change
                alpha=0.05,
                power=0.8
            )
            
            print()
            print(f"To detect a 20% relative change with 80% power:")
            print(f"  Required sample size per variant: {required_n:,}")
            print(f"  Current sample size per variant: {control.exposures:,}")
            
            if required_n > control.exposures:
                additional_needed = required_n - control.exposures
                print(f"  Additional visitors needed: {additional_needed:,}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
