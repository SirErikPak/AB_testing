import numpy as np
from scipy import stats
from scipy.stats import t # Use the t-distribution for better accuracy with small samples


def perform_t_test(A, B, alpha = 0.05, equal_var=True):
    # Use pooled t-test only if variances are equal and sample sizes are similar.
    # Perform two-sample t-test (equal_var=True or False based on Levene's test)
    t_stat, p_value = stats.ttest_ind(A, B, equal_var=equal_var)
    print(f"Pooled t-test t-statistic: {t_stat:.3f}")
    print(f"Pooled t-test p-value: {p_value:.3f}")

    # Interpretation
    # --- Conclusion ---
    if p_value < alpha:
        if p_value < alpha:
            print(f"\nConclusion: Reject the Null Hypothesis (p < {alpha}).")
            print(f"The mean of Group B ({np.mean(B):.2f}) is statistically significantly different from Group A ({np.mean(A):.2f}).")
        else:
            print(f"\nConclusion: Fail to Reject the Null Hypothesis (p >= {alpha}).")
            print(f"There is not enough evidence to say the mean of Group B is different from Group A.")



def bayesian_t_test_equivalent(A, B, N_SAMPLES=100_000):
    # --- 1. Calculate Standard Errors (The Uncertainty) ---
    # Standard error is the standard deviation of the sampling distribution of the mean.
    A_mean = np.mean(A)
    B_mean = np.mean(B)

    A_std = np.std(A, ddof=1)  # Sample standard deviation
    B_std = np.std(B, ddof=1)  # Sample standard deviation

    se_A = A_std / np.sqrt(len(A))
    se_B = B_std / np.sqrt(len(B))

    # --- 2. Degrees of Freedom (dof) for the t-distribution
    # Using n-1 for a simpler approximation
    dof_A = len(A) - 1
    dof_B = len(B) - 1

    # Monte Carlo Simulation (Approximating the Posterior)
    # Approximate the Posterior Distribution of the Mean (mu) for each group
    # We sample from the t-distribution centered at the sample mean (mean_A/B) 
    # and scaled by the standard error (se_A/B).
    samples_A = t.rvs(df=dof_A, loc=A_mean, scale=se_A, size=N_SAMPLES)
    samples_B = t.rvs(df=dof_B, loc=B_mean, scale=se_B, size=N_SAMPLES)

    # --- 4. Parameter of Interest: Difference and Superiority ---
    diff_samples = samples_B - samples_A

    # Calculate the 95% Credible Interval (CrI)
    hdi_diff = np.percentile(diff_samples, [2.5, 97.5])

    # Calculate the Probability of Superiority (P(mu_B > mu_A))
    # This is the proportion of times the difference is positive.
    prob_b_better = (diff_samples > 0).mean()

    # --- 5. Analysis and Interpretation ---
    print("\n--- Bayesian T-Test Equivalent Results (Monte Carlo) ---")
    print("Ratio of stds (B/A):", B_std / A_std)
    print(f"Mean Difference (B - A): {np.mean(diff_samples):.2f}")
    print(f"95% Credible Interval (CrI) for Difference: [{hdi_diff[0]:.2f}, {hdi_diff[1]:.2f}]")
    print(f"Probability B > A (P(mu_B > mu_A)): {prob_b_better:.4f} ({prob_b_better:.2%})")

    # --- Conclusion ---
    # Interpret the CrI, which is the key to Bayesian hypothesis testing.
    if hdi_diff[0] > 0:
        print("\n✅ Conclusion: The entire 95% CrI is positive. Variant B is highly likely to be superior to A.")
    elif hdi_diff[0] < 0 and hdi_diff[1] > 0:
        print("\n⚠️ Conclusion: The 95% CrI crosses zero. The evidence is not conclusive; more data is needed.")
    else:
        print("\n❌ Conclusion: The 95% CrI is entirely negative. Variant A is likely superior to B (or B is inferior).")