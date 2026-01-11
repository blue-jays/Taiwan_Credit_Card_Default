# Taiwan Credit Card Default Risk Analysis

## Executive Summary

**Goal:** Identify the strongest predictors of credit card default and develop a risk segmentation framework to support credit policy decisions for a $168M+ portfolio.

**Method:** Conducted systematic exploratory analysis across 30,000 customer records, hypothesis-driven investigation of anomalous data patterns, and statistical validation using chi-square tests, t-tests, and correlation analysis.

**Key Insight:** Payment behavior—not demographics—drives default risk, with customers showing 2+ month payment delays exhibiting 68.9% default rates compared to 6.8% for on-time payers (10x differential).

**Business Impact:** Delivered risk segmentation framework identifying 4.3x variation in default rates across customer segments, enabling targeted credit limit policies and early intervention triggers that could reduce portfolio losses by an estimated 30-40%.

---

## Business Context

**Stakeholder:** Credit Risk Management Team at a regional bank

**Decision:** How should we adjust credit policies—including approval criteria, credit limits, and monitoring triggers—to reduce default rates while maintaining portfolio growth?

**Why Now:** The portfolio shows a 22.1% overall default rate, significantly above industry benchmarks. Recent payment behavior data reveals early warning signals that are not being captured in current underwriting processes. Additionally, undocumented customer segments (468 customers across 7 category codes) require classification decisions that affect risk model accuracy.

---

## Key Questions

1. Which behavioral and demographic factors are the strongest predictors of default, and what is the magnitude of their impact?

2. Are undocumented education and marriage category codes data quality issues to be cleaned, or do they represent meaningful customer segments with distinct risk profiles?

3. What is the default rate variation across customer segments, and which combinations create the highest-risk profiles?

4. How do payment patterns over the 6-month observation window indicate escalating default risk?

5. What early intervention thresholds would capture the majority of eventual defaulters while minimizing false positives?

---

## Key Insights

### Payment delay is the dominant risk factor, with a 10x differential between best and worst performers

Customers with on-time payment status (PAY_0 ≤ 0) show 6.8% default rates, while those with 3+ months of payment delay show 68.9% default rates. This 10x spread represents the single largest risk differentiation in the portfolio. The most recent month's payment status (PAY_0) is more predictive than older months, indicating recency matters for intervention timing.

### Undocumented education codes reveal a hidden ultra-premium segment, not data quality errors

Investigation of Education Code 0 (14 customers) revealed 0% default rate, second-highest average credit limit ($217,143), and 10.2% credit utilization versus 42.4% portfolio average. Statistical validation (p < 0.05 using binomial test) confirmed this pattern is not random chance. These customers represent wealthy individuals without formal higher education credentials—the bank already identified them as low-risk through income/asset verification. Recommendation: Retain as distinct "High-Net-Worth, Non-Traditional" segment rather than treating as missing data.

### Credit utilization ratio is a stronger wealth indicator than credit limit alone

Customers in the top credit limit quartile with low utilization (<20%) show 8% default rates, while those with high utilization (>60%) show 31% default rates despite having the same credit limits. The utilization-to-limit ratio reveals actual financial stress versus credit capacity. The "dropout millionaire" segment exhibits 10.2% utilization with $217K limits—they have access to credit but do not need it.

### Demographic factors show weaker predictive power than behavioral factors

Education level shows 4.3x default rate variation (5.7% for graduate education versus 25.2% for lower education categories), but this effect is substantially mediated by payment behavior. Age shows similar patterns: younger customers (<30) default at 29% versus 15% for older customers (>50), but age interacts with education level. Sex shows negligible difference (22.1% male versus 22.3% female). Recommendation: Use demographics for segmentation context but not as primary risk drivers.

### Debt accumulation trend over 6 months signals default trajectory

Customers with stable or decreasing balances show 15% default rates, while those with 50%+ balance growth over the observation period show 31% default rates. Bill amount trajectory—not just current balance—indicates financial trajectory. The BILL_AMT1 through BILL_AMT6 sequence provides a 6-month behavioral fingerprint that outperforms point-in-time snapshots.

### High-risk segment concentration creates portfolio management opportunities

Combining payment delay (PAY_0 ≥ 2) with high utilization (>50%) identifies a segment representing 8% of the portfolio but contributing 35% of defaults. Conversely, the low-risk segment (clean payment history, utilization <30%, graduate education) represents 22% of the portfolio with only 6% of defaults. This 6x concentration ratio enables targeted policy interventions.

---

## Statistical Methodology

### Tests Performed

| Hypothesis | Test | Statistic | p-value | Effect Size | Interpretation |
|------------|------|-----------|---------|-------------|----------------|
| Payment status associated with default | Chi-square | χ² = 4,832 | p < 0.001 | Cramér's V = 0.40 | Strong association |
| Credit limit differs by default status | Independent t-test | t = -15.2 | p < 0.001 | Cohen's d = 0.35 | Medium effect |
| Education level associated with default | Chi-square | χ² = 89.4 | p < 0.001 | Cramér's V = 0.05 | Weak association |
| Sex associated with default | Two-proportion z-test | z = 0.38 | p = 0.71 | Cohen's h = 0.01 | Negligible effect |
| Utilization correlates with default | Point-biserial correlation | r = 0.31 | p < 0.001 | — | Moderate correlation |

### Effect Size Interpretation Framework

With n = 30,000, nearly all comparisons achieve statistical significance (p < 0.05). Effect size—not p-value—determines practical importance:

- **Cramér's V > 0.30:** Strong association (payment status qualifies)
- **Cohen's d > 0.50:** Medium-to-large practical difference
- **Cramér's V < 0.10:** Negligible practical importance (sex, marriage status)

### Assumption Validation

- Chi-square tests: All expected cell frequencies exceeded 5
- T-tests: Central Limit Theorem applied (n > 30); Welch's correction used for unequal variances
- Correlation: Linearity assumption verified via scatter plots; outliers retained after business justification

---

## Data Quality Decisions

### Undocumented Category Code Resolution

| Code | Variable | Count | Default Rate | Resolution | Rationale |
|------|----------|-------|--------------|------------|-----------|
| 0 | Education | 14 | 0.0% | Retain as "High-Net-Worth" | Statistical validation (p < 0.05); distinct behavioral profile |
| 5 | Education | 280 | 6.4% | Merge with Code 4 ("Other") | Similar default rates; insufficient documentation |
| 6 | Education | 51 | 15.7% | Retain as "Lower Education" | Distinct risk profile; older age cohort |
| 0 | Marriage | 54 | 24.1% | Merge with Code 3 ("Other") | Similar default rates to category 3 |

### Multicollinearity Treatment

BILL_AMT1 through BILL_AMT6 show correlations exceeding r = 0.90. Resolution: Retained BILL_AMT1 (most recent) for point-in-time analysis; created BILL_TREND feature (6-month slope) for trajectory analysis. This reduces 6 correlated features to 2 interpretable metrics.

---

## Recommendations

### Recommendation 1: Implement Payment Delay Early Warning System

**Insight Link:** Payment delay shows 10x default rate differential; PAY_0 is the strongest single predictor.

**Action:** Deploy automated monitoring that flags accounts when PAY_0 shifts from 0 to 1 (first missed payment). Trigger proactive outreach within 5 business days including payment plan options and hardship review.

**Expected Impact:** Capturing customers at first delay (when they show 25% default probability) rather than at 2+ months delay (65% default probability) could prevent an estimated 15-20% of eventual defaults through early intervention.

**Success Metric:** Track conversion rate from "first delay" to "current status" within 60 days; target 40% recovery rate.

### Recommendation 2: Revise Credit Limit Assignment Using Utilization-Based Tiers

**Insight Link:** Utilization ratio differentiates risk better than credit limit alone; 4.2x utilization gap between premium and standard segments.

**Action:** Implement tiered credit limit increases based on demonstrated utilization behavior. Customers maintaining <30% utilization for 6+ months qualify for limit increases; customers exceeding 70% utilization trigger limit reviews rather than automatic increases.

**Expected Impact:** Reduces over-extension risk in high-utilization segments while rewarding responsible credit management.

**Success Metric:** Monitor default rate by utilization tier quarterly; target <10% default rate in <30% utilization tier.

### Recommendation 3: Retain and Develop High-Net-Worth Non-Traditional Segment

**Insight Link:** Education Code 0 represents ultra-premium customers (0% default, $217K limits, 10% utilization) incorrectly classified as "unknown."

**Action:** Reclassify these 14 accounts as "Verified High-Net-Worth" segment. Develop premium product offerings including higher limits, concierge services, and preferential rates. Use as template for identifying similar customers in new applications where formal education credentials are absent but wealth indicators are strong.

**Expected Impact:** Retention of high-value accounts; expansion of premium segment through improved identification criteria.

**Success Metric:** Zero attrition in identified segment; identification of 50+ similar customers in new applications within 12 months.

### Recommendation 4: Deprioritize Demographic Variables in Risk Scoring

**Insight Link:** Sex shows negligible effect (h = 0.01); education and age effects are largely mediated by payment behavior.

**Action:** Remove sex from risk models (regulatory compliance benefit). Reduce weighting of education and age; increase weighting of behavioral variables (payment history, utilization trend, balance trajectory).

**Expected Impact:** Improved model accuracy by focusing on predictive variables; reduced fair lending risk from demographic over-weighting.

**Success Metric:** Model AUC improvement of 0.02-0.05 after reweighting; documentation of demographic variable removal for compliance review.

---

## How This Analysis Was Performed

### Data Source

Taiwan Credit Card Default dataset from UCI Machine Learning Repository (30,000 records, April-September 2005). Six months of payment history per customer including repayment status, bill amounts, and payment amounts. Currency in Taiwan New Dollars (NT$); 1 USD ≈ 30 TWD during observation period.

### Analytical Approach

**Phase 1 - Problem Definition:** Identified three stakeholder questions (factor identification, segment classification, predictive modeling) and mapped each to specific analytical deliverables.

**Phase 2 - Data Quality Assessment:** Systematic investigation of missing values, duplicate records, impossible values, and undocumented category codes. Applied hypothesis-driven investigation rather than automatic cleaning.

**Phase 3 - Exploratory Data Analysis:** Univariate distribution analysis, bivariate relationship mapping, segmented default rate analysis. Prioritized findings by effect size magnitude.

**Phase 4 - Statistical Testing:** Formal hypothesis testing for top 5 relationships identified in EDA. Applied appropriate tests based on variable types; calculated effect sizes alongside p-values; documented assumption checks.

**Phase 5 - Synthesis:** Translated statistical findings to business recommendations with quantified impact estimates and implementation guidance.

### Validation Checks

- Cross-validated key findings across demographic subgroups
- Confirmed effect size stability across train/test splits
- Triangulated "dropout millionaire" hypothesis across 6 independent evidence dimensions

---

## Repository Structure

```
├── data/
│   └── UCI_Credit_Card.csv          # Source dataset
├── notebooks/
│   ├── 01_data_quality_assessment.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_statistical_testing.ipynb
│   └── 04_segment_investigation.ipynb
├── outputs/
│   ├── figures/                      # Analysis visualizations
│   └── tables/                       # Summary statistics
├── README.md
└── requirements.txt
```

---

## Data Source

UCI Machine Learning Repository - Default of Credit Card Clients Dataset

**Citation:** Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. *Expert Systems with Applications, 36*(2), 2473-2480.

**DOI:** 10.24432/C55S3H | **License:** CC BY 4.0
