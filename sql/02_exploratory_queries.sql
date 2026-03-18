-- ========================================
-- LOAN DEFAULT PREDICTION - SQL ANALYSIS
-- Author: [Your Name]
-- Date: 2024-03-17
-- ========================================

-- QUERY 1: Total number of loans
-- Business Question: What is the total volume of loan applications?
SELECT 
    COUNT(*) as total_loans,
    COUNT(DISTINCT Loan_ID) as unique_loans
FROM loans;

-- ========================================

-- QUERY 2: Loan approval rate
-- Business Question: What percentage of loans are approved vs rejected?
SELECT 
    Loan_Status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM loans), 2) as percentage
FROM loans
GROUP BY Loan_Status
ORDER BY count DESC;

-- ========================================

-- QUERY 3: Default rate by Gender
-- Business Question: Does gender impact loan approval rates?
SELECT 
    Gender,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    SUM(CASE WHEN Loan_Status = 'N' THEN 1 ELSE 0 END) as rejected,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE Gender IS NOT NULL
GROUP BY Gender
ORDER BY approval_rate DESC;

-- ========================================

-- QUERY 4: Default rate by Education Level
-- Business Question: Are graduates more likely to get loans approved?
SELECT 
    Education,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE Education IS NOT NULL
GROUP BY Education
ORDER BY approval_rate DESC;

-- ========================================

-- QUERY 5: Default rate by Marital Status
-- Business Question: Do married applicants have better approval rates?
SELECT 
    Married,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE Married IS NOT NULL
GROUP BY Married
ORDER BY approval_rate DESC;

-- ========================================

-- QUERY 6: Loan Amount Distribution
-- Business Question: What is the average loan amount requested?
SELECT 
    ROUND(AVG(LoanAmount), 2) as avg_loan_amount,
    ROUND(MIN(LoanAmount), 2) as min_loan_amount,
    ROUND(MAX(LoanAmount), 2) as max_loan_amount,
    ROUND(AVG(LoanAmount) - MIN(LoanAmount), 2) as range_amount
FROM loans
WHERE LoanAmount IS NOT NULL;

-- ========================================

-- QUERY 7: Income vs Loan Amount Analysis
-- Business Question: What is the relationship between income and loan amount?
SELECT 
    ROUND(AVG(ApplicantIncome), 2) as avg_applicant_income,
    ROUND(AVG(CoapplicantIncome), 2) as avg_coapplicant_income,
    ROUND(AVG(ApplicantIncome + CoapplicantIncome), 2) as avg_total_income,
    ROUND(AVG(LoanAmount), 2) as avg_loan_amount,
    ROUND(AVG(LoanAmount) * 100.0 / AVG(ApplicantIncome + CoapplicantIncome), 2) as loan_to_income_ratio
FROM loans
WHERE ApplicantIncome > 0 AND LoanAmount IS NOT NULL;

-- ========================================

-- QUERY 8: High-risk segments (Self-employed)
-- Business Question: Are self-employed applicants riskier?
SELECT 
    Self_Employed,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE Self_Employed IS NOT NULL
GROUP BY Self_Employed
ORDER BY approval_rate DESC;

-- ========================================

-- QUERY 9: Credit History Impact
-- Business Question: How critical is credit history for approval?
SELECT 
    Credit_History,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE Credit_History IS NOT NULL
GROUP BY Credit_History
ORDER BY Credit_History DESC;

-- ========================================

-- QUERY 10: Geographic Analysis
-- Business Question: Which property areas have highest approval rates?
SELECT 
    Property_Area,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate,
    ROUND(AVG(LoanAmount), 2) as avg_loan_amount
FROM loans
WHERE Property_Area IS NOT NULL
GROUP BY Property_Area
ORDER BY approval_rate DESC;

-- ========================================

-- QUERY 11: Income Segmentation
-- Business Question: How do approval rates vary across income brackets?
SELECT 
    CASE 
        WHEN ApplicantIncome < 3000 THEN '1. Low Income (<3K)'
        WHEN ApplicantIncome BETWEEN 3000 AND 6000 THEN '2. Medium Income (3K-6K)'
        WHEN ApplicantIncome BETWEEN 6000 AND 10000 THEN '3. High Income (6K-10K)'
        ELSE '4. Very High Income (>10K)'
    END as income_segment,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE ApplicantIncome > 0
GROUP BY income_segment
ORDER BY income_segment;

-- ========================================

-- QUERY 12: Loan Amount Segmentation
-- Business Question: Do larger loans have different approval rates?
SELECT 
    CASE 
        WHEN LoanAmount < 100 THEN '1. Small Loan (<100K)'
        WHEN LoanAmount BETWEEN 100 AND 200 THEN '2. Medium Loan (100K-200K)'
        WHEN LoanAmount BETWEEN 200 AND 300 THEN '3. Large Loan (200K-300K)'
        ELSE '4. Very Large Loan (>300K)'
    END as loan_segment,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE LoanAmount IS NOT NULL
GROUP BY loan_segment
ORDER BY loan_segment;

-- ========================================

-- QUERY 13: Dependents Analysis
-- Business Question: How do number of dependents affect loan approval?
SELECT 
    Dependents,
    COUNT(*) as total_applications,
    SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate
FROM loans
WHERE Dependents IS NOT NULL
GROUP BY Dependents
ORDER BY 
    CASE 
        WHEN Dependents = '0' THEN 0
        WHEN Dependents = '1' THEN 1
        WHEN Dependents = '2' THEN 2
        WHEN Dependents = '3+' THEN 3
    END;

-- ========================================

-- QUERY 14: Missing Data Analysis
-- Business Question: How much data is missing in critical fields?
SELECT 
    'Gender' as field_name,
    COUNT(*) as total_records,
    SUM(CASE WHEN Gender IS NULL OR Gender = '' THEN 1 ELSE 0 END) as missing_count,
    ROUND(SUM(CASE WHEN Gender IS NULL OR Gender = '' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as missing_percentage
FROM loans
UNION ALL
SELECT 
    'Married',
    COUNT(*),
    SUM(CASE WHEN Married IS NULL OR Married = '' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN Married IS NULL OR Married = '' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM loans
UNION ALL
SELECT 
    'Self_Employed',
    COUNT(*),
    SUM(CASE WHEN Self_Employed IS NULL OR Self_Employed = '' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN Self_Employed IS NULL OR Self_Employed = '' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM loans
UNION ALL
SELECT 
    'LoanAmount',
    COUNT(*),
    SUM(CASE WHEN LoanAmount IS NULL THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN LoanAmount IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM loans
UNION ALL
SELECT 
    'Credit_History',
    COUNT(*),
    SUM(CASE WHEN Credit_History IS NULL THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN Credit_History IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM loans
ORDER BY missing_percentage DESC;

-- ========================================

-- QUERY 15: High-Value Customer Profile
-- Business Question: What profile gets the highest loan amounts approved?
SELECT 
    Gender,
    Education,
    Married,
    Property_Area,
    COUNT(*) as count,
    ROUND(AVG(LoanAmount), 2) as avg_loan_amount,
    ROUND(AVG(ApplicantIncome), 2) as avg_income
FROM loans
WHERE Loan_Status = 'Y' 
    AND Gender IS NOT NULL 
    AND LoanAmount IS NOT NULL
GROUP BY Gender, Education, Married, Property_Area
HAVING COUNT(*) >= 5
ORDER BY avg_loan_amount DESC
LIMIT 10;

-- ========================================
-- END OF QUERIES
-- ========================================