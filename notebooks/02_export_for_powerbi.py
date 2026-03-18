# ========================================
# EXPORT DATA FOR POWER BI DASHBOARD
# ========================================

import pandas as pd
import numpy as np
import os
import sys

# Get correct paths
if os.path.basename(os.getcwd()) == 'notebooks':
    # Running from notebooks folder
    os.chdir('..')
    
print("="*70)
print("📊 EXPORTING DATA FOR POWER BI DASHBOARD")
print("="*70)
print(f"\n📂 Working directory: {os.getcwd()}")

# Load original data
data_file = 'data/loan_data.csv'

if not os.path.exists(data_file):
    print(f"\n❌ Error: File not found at {os.path.abspath(data_file)}")
    print(f"\n📂 Current directory: {os.getcwd()}")
    print(f"📋 Files in current directory:")
    print(os.listdir('.'))
    sys.exit(1)

df = pd.read_csv(data_file)
print(f"\n✅ Loaded original data: {df.shape[0]} rows × {df.shape[1]} columns")

# ========================================
# 1. CLEAN AND PREPARE DATA
# ========================================

print("\n🧹 Cleaning data...")

# Create a copy
df_powerbi = df.copy()

# Fill missing values
categorical_cols = ['Gender', 'Married', 'Dependents', 'Self_Employed', 'Credit_History', 'Loan_Amount_Term']
for col in categorical_cols:
    if col in df_powerbi.columns and df_powerbi[col].isnull().sum() > 0:
        df_powerbi[col].fillna(df_powerbi[col].mode()[0], inplace=True)

if 'LoanAmount' in df_powerbi.columns:
    df_powerbi['LoanAmount'].fillna(df_powerbi['LoanAmount'].median(), inplace=True)

print("✅ Missing values filled")

# ========================================
# 2. CREATE CALCULATED COLUMNS FOR DASHBOARD
# ========================================

print("\n⚙️ Creating calculated columns...")

# Total Income
df_powerbi['Total_Income'] = df_powerbi['ApplicantIncome'] + df_powerbi['CoapplicantIncome']

# Income Category
df_powerbi['Income_Category'] = pd.cut(
    df_powerbi['Total_Income'],
    bins=[0, 3000, 6000, 10000, float('inf')],
    labels=['Low (<3K)', 'Medium (3K-6K)', 'High (6K-10K)', 'Very High (>10K)']
)

# Loan Amount Category
df_powerbi['Loan_Category'] = pd.cut(
    df_powerbi['LoanAmount'],
    bins=[0, 100, 200, 300, float('inf')],
    labels=['Small (<100K)', 'Medium (100-200K)', 'Large (200-300K)', 'Very Large (>300K)']
)

# Loan to Income Ratio
df_powerbi['Loan_to_Income_Ratio'] = df_powerbi['LoanAmount'] / df_powerbi['Total_Income']
df_powerbi['Loan_to_Income_Ratio'] = df_powerbi['Loan_to_Income_Ratio'].replace([np.inf, -np.inf], 0)

# Risk Score (simple calculation based on key factors)
df_powerbi['Risk_Score'] = 0

# Credit History impact (most important)
df_powerbi.loc[df_powerbi['Credit_History'] == 0, 'Risk_Score'] += 40
df_powerbi.loc[df_powerbi['Credit_History'] == 1, 'Risk_Score'] += 0

# Self-employed risk
df_powerbi.loc[df_powerbi['Self_Employed'] == 'Yes', 'Risk_Score'] += 15

# High loan to income ratio
df_powerbi.loc[df_powerbi['Loan_to_Income_Ratio'] > 0.05, 'Risk_Score'] += 20

# Low income risk
df_powerbi.loc[df_powerbi['Total_Income'] < 3000, 'Risk_Score'] += 15

# Dependents risk
df_powerbi.loc[df_powerbi['Dependents'].isin(['3+', '2']), 'Risk_Score'] += 10

# Risk Category
df_powerbi['Risk_Category'] = pd.cut(
    df_powerbi['Risk_Score'],
    bins=[-1, 20, 40, 60, 100],
    labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
)

# Loan Status Clean (for easier understanding)
df_powerbi['Loan_Approved'] = df_powerbi['Loan_Status'].map({'Y': 'Approved', 'N': 'Rejected'})

# Numeric Loan Status
df_powerbi['Loan_Status_Numeric'] = df_powerbi['Loan_Status'].map({'Y': 1, 'N': 0})

# Estimated Loss (if loan defaults) - assume 30% of loan amount is lost
df_powerbi['Estimated_Loss_If_Default'] = df_powerbi['LoanAmount'] * 0.30 * 1000  # in actual currency

print("✅ Calculated columns created")

# ========================================
# 3. CREATE SUMMARY TABLES
# ========================================

print("\n📊 Creating summary tables...")

# Summary by Gender
summary_gender = df_powerbi.groupby('Gender').agg({
    'Loan_ID': 'count',
    'Loan_Status_Numeric': 'mean',
    'LoanAmount': 'mean',
    'Total_Income': 'mean'
}).reset_index()
summary_gender.columns = ['Gender', 'Total_Applications', 'Approval_Rate', 'Avg_Loan_Amount', 'Avg_Income']
summary_gender['Approval_Rate'] = (summary_gender['Approval_Rate'] * 100).round(2)

# Summary by Property Area
summary_area = df_powerbi.groupby('Property_Area').agg({
    'Loan_ID': 'count',
    'Loan_Status_Numeric': 'mean',
    'LoanAmount': 'mean',
    'Total_Income': 'mean'
}).reset_index()
summary_area.columns = ['Property_Area', 'Total_Applications', 'Approval_Rate', 'Avg_Loan_Amount', 'Avg_Income']
summary_area['Approval_Rate'] = (summary_area['Approval_Rate'] * 100).round(2)

# Summary by Education
summary_education = df_powerbi.groupby('Education').agg({
    'Loan_ID': 'count',
    'Loan_Status_Numeric': 'mean',
    'LoanAmount': 'mean',
    'Total_Income': 'mean'
}).reset_index()
summary_education.columns = ['Education', 'Total_Applications', 'Approval_Rate', 'Avg_Loan_Amount', 'Avg_Income']
summary_education['Approval_Rate'] = (summary_education['Approval_Rate'] * 100).round(2)

# Summary by Risk Category
summary_risk = df_powerbi.groupby('Risk_Category').agg({
    'Loan_ID': 'count',
    'Loan_Status_Numeric': 'mean',
    'Estimated_Loss_If_Default': 'sum'
}).reset_index()
summary_risk.columns = ['Risk_Category', 'Total_Applications', 'Approval_Rate', 'Total_Estimated_Loss']
summary_risk['Approval_Rate'] = (summary_risk['Approval_Rate'] * 100).round(2)

# Summary by Income Category
summary_income = df_powerbi.groupby('Income_Category').agg({
    'Loan_ID': 'count',
    'Loan_Status_Numeric': 'mean',
    'LoanAmount': 'mean'
}).reset_index()
summary_income.columns = ['Income_Category', 'Total_Applications', 'Approval_Rate', 'Avg_Loan_Amount']
summary_income['Approval_Rate'] = (summary_income['Approval_Rate'] * 100).round(2)

# Overall KPIs
kpis = pd.DataFrame({
    'Metric': [
        'Total Applications',
        'Total Approved',
        'Total Rejected',
        'Approval Rate (%)',
        'Rejection Rate (%)',
        'Average Loan Amount',
        'Total Loan Value',
        'High Risk Applications',
        'Estimated Loss from High Risk'
    ],
    'Value': [
        len(df_powerbi),
        (df_powerbi['Loan_Status'] == 'Y').sum(),
        (df_powerbi['Loan_Status'] == 'N').sum(),
        round((df_powerbi['Loan_Status'] == 'Y').sum() / len(df_powerbi) * 100, 2),
        round((df_powerbi['Loan_Status'] == 'N').sum() / len(df_powerbi) * 100, 2),
        round(df_powerbi['LoanAmount'].mean(), 2),
        round(df_powerbi['LoanAmount'].sum(), 2),
        (df_powerbi['Risk_Category'].isin(['High Risk', 'Very High Risk'])).sum(),
        round(df_powerbi[df_powerbi['Risk_Category'].isin(['High Risk', 'Very High Risk'])]['Estimated_Loss_If_Default'].sum(), 2)
    ]
})

print("✅ Summary tables created")

# ========================================
# 4. EXPORT TO CSV FILES
# ========================================

print("\n💾 Exporting files...")

# Create powerbi folder if not exists
os.makedirs('powerbi', exist_ok=True)

# Export main data
df_powerbi.to_csv('powerbi/loan_data_for_powerbi.csv', index=False)
print(f"   ✅ Main data: powerbi/loan_data_for_powerbi.csv ({len(df_powerbi)} rows)")

# Export summary tables
summary_gender.to_csv('powerbi/summary_by_gender.csv', index=False)
print(f"   ✅ Gender summary: powerbi/summary_by_gender.csv")

summary_area.to_csv('powerbi/summary_by_area.csv', index=False)
print(f"   ✅ Area summary: powerbi/summary_by_area.csv")

summary_education.to_csv('powerbi/summary_by_education.csv', index=False)
print(f"   ✅ Education summary: powerbi/summary_by_education.csv")

summary_risk.to_csv('powerbi/summary_by_risk.csv', index=False)
print(f"   ✅ Risk summary: powerbi/summary_by_risk.csv")

summary_income.to_csv('powerbi/summary_by_income.csv', index=False)
print(f"   ✅ Income summary: powerbi/summary_by_income.csv")

kpis.to_csv('powerbi/kpi_metrics.csv', index=False)
print(f"   ✅ KPI metrics: powerbi/kpi_metrics.csv")

# ========================================
# 5. DISPLAY SUMMARY
# ========================================

print("\n" + "="*70)
print("📊 DATA EXPORT SUMMARY")
print("="*70)

print("\n📋 KPI Metrics:")
print(kpis.to_string(index=False))

print("\n📋 Risk Category Summary:")
print(summary_risk.to_string(index=False))

print("\n📋 Files exported to 'powerbi/' folder:")
print("   1. loan_data_for_powerbi.csv (Main dataset)")
print("   2. summary_by_gender.csv")
print("   3. summary_by_area.csv")
print("   4. summary_by_education.csv")
print("   5. summary_by_risk.csv")
print("   6. summary_by_income.csv")
print("   7. kpi_metrics.csv")

print("\n" + "="*70)
print("✅ DATA EXPORT COMPLETE! Ready for Power BI")
print("="*70)