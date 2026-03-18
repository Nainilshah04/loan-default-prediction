# 🔍 SQL Analysis - Key Findings

**Project:** Loan Default Prediction  
**Date:** 2024-03-17  
**Analyst:** [Your Name]

---

## 📊 Executive Summary

Analyzed 614 loan applications using SQL to identify risk patterns and approval drivers.

### Key Metrics:
- **Total Applications:** 614
- **Overall Approval Rate:** 68.73%
- **Rejection Rate:** 31.27%

---

## 🎯 Critical Findings

### 1. Credit History is the STRONGEST Predictor
- **With Credit History:** 79.6% approval rate
- **Without Credit History:** 7.9% approval rate
- **Impact:** 10x difference in approval likelihood

### 2. Income Segmentation Insights
- Low Income (<3K): 62% approval
- Medium Income (3K-6K): 72% approval  
- High Income (>10K): 75% approval
- **Finding:** Higher income → Higher approval rate

### 3. Geographic Variations
- Semiurban: Highest approval (71%)
- Urban: 68% approval
- Rural: 65% approval

### 4. Education Level Impact
- Graduates: 70% approval rate
- Non-Graduates: 65% approval rate
- **Finding:** Moderate impact (5% difference)

### 5. Self-Employment Risk
- Salaried: 70% approval
- Self-Employed: 64% approval
- **Finding:** Self-employed perceived as higher risk

### 6. Marital Status Effect
- Married Applicants: 71% approval
- Unmarried: 64% approval
- **Finding:** Married applicants preferred

---

## 🚨 High-Risk Segments Identified

1. **No Credit History + Self-Employed** → 92% rejection rate
2. **Low Income + Rural Area** → 45% rejection rate
3. **High Loan Amount (>300K) + Low Income** → 55% rejection rate

---

## 💡 Business Recommendations

1. **Implement Credit History Check** - Mandatory for all applicants
2. **Income Verification** - Stricter for self-employed segment
3. **Geographic Pricing** - Adjust interest rates by area
4. **Loan Amount Caps** - Based on income multiples (max 3x income)

---

## 📈 Next Steps

1. Build ML model using these insights
2. Create risk scoring system
3. Develop Power BI dashboard for business users

---

*Note: Detailed query results available in `sql/query_results/` folder*