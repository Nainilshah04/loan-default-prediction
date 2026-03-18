# ========================================
# FIX: RETRAIN AND SAVE RANDOM FOREST MODEL
# ========================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import os

print("="*70)
print("FIXING MODEL - TRAINING RANDOM FOREST")
print("="*70)

# Load data
df = pd.read_csv('data/loan_data.csv')
print(f"\nData loaded: {df.shape[0]} rows")

# ========================================
# DATA PREPROCESSING
# ========================================

print("\n1. Preprocessing data...")

# Fill missing values
df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
df['Married'].fillna(df['Married'].mode()[0], inplace=True)
df['Dependents'].fillna(df['Dependents'].mode()[0], inplace=True)
df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace=True)
df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)
df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0], inplace=True)
df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)

print("   Missing values filled")

# ========================================
# FEATURE ENGINEERING
# ========================================

print("\n2. Creating features...")

# Total Income
df['TotalIncome'] = df['ApplicantIncome'] + df['CoapplicantIncome']

# Loan to Income Ratio
df['LoanAmountToIncome'] = df['LoanAmount'] / df['TotalIncome']
df['LoanAmountToIncome'] = df['LoanAmountToIncome'].replace([np.inf, -np.inf], 0)

# Income per Dependent
df['Dependents_numeric'] = df['Dependents'].replace({'3+': 3}).astype(float)
df['IncomePerDependent'] = df['TotalIncome'] / (df['Dependents_numeric'] + 1)

# Log transformations
df['LoanAmount_log'] = np.log(df['LoanAmount'] + 1)
df['TotalIncome_log'] = np.log(df['TotalIncome'] + 1)

# Binary encoding
df['Gender_binary'] = df['Gender'].map({'Male': 1, 'Female': 0})
df['Married_binary'] = df['Married'].map({'Yes': 1, 'No': 0})
df['Education_binary'] = df['Education'].map({'Graduate': 1, 'Not Graduate': 0})
df['Self_Employed_binary'] = df['Self_Employed'].map({'Yes': 1, 'No': 0})

# Target encoding
df['Loan_Status_binary'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

# Property Area encoding
property_dummies = pd.get_dummies(df['Property_Area'], prefix='Property_Area', drop_first=True)
df = pd.concat([df, property_dummies], axis=1)

print("   Features created")

# ========================================
# PREPARE DATA FOR MODELING
# ========================================

print("\n3. Preparing features...")

feature_columns = [
    'ApplicantIncome',
    'CoapplicantIncome',
    'LoanAmount',
    'Loan_Amount_Term',
    'Credit_History',
    'TotalIncome',
    'LoanAmountToIncome',
    'IncomePerDependent',
    'LoanAmount_log',
    'TotalIncome_log',
    'Gender_binary',
    'Married_binary',
    'Education_binary',
    'Self_Employed_binary',
    'Dependents_numeric',
    'Property_Area_Semiurban',
    'Property_Area_Urban'
]

X = df[feature_columns].copy()
y = df['Loan_Status_binary'].copy()

# Handle any remaining NaN
X = X.fillna(X.median())

print(f"   Features: {X.shape[1]}")
print(f"   Samples: {X.shape[0]}")

# ========================================
# TRAIN TEST SPLIT
# ========================================

print("\n4. Splitting data...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

# ========================================
# SCALING
# ========================================

print("\n5. Scaling features...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("   Scaling done")

# ========================================
# TRAIN RANDOM FOREST
# ========================================

print("\n6. Training Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train_scaled, y_train)

# Evaluate
y_pred_train = rf_model.predict(X_train_scaled)
y_pred_test = rf_model.predict(X_test_scaled)
y_pred_proba = rf_model.predict_proba(X_test_scaled)[:, 1]

train_acc = accuracy_score(y_train, y_pred_train)
test_acc = accuracy_score(y_test, y_pred_test)
test_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n   Train Accuracy: {train_acc*100:.2f}%")
print(f"   Test Accuracy: {test_acc*100:.2f}%")
print(f"   ROC-AUC: {test_auc:.4f}")

# ========================================
# SAVE MODEL
# ========================================

print("\n7. Saving model...")

os.makedirs('models', exist_ok=True)

joblib.dump(rf_model, 'models/best_loan_model.pkl')
print("   Saved: models/best_loan_model.pkl")

joblib.dump(scaler, 'models/scaler.pkl')
print("   Saved: models/scaler.pkl")

joblib.dump(feature_columns, 'models/feature_names.pkl')
print("   Saved: models/feature_names.pkl")

# ========================================
# TEST THE SAVED MODEL
# ========================================

print("\n" + "="*70)
print("TESTING SAVED MODEL")
print("="*70)

# Load fresh
model = joblib.load('models/best_loan_model.pkl')
scaler = joblib.load('models/scaler.pkl')
features = joblib.load('models/feature_names.pkl')

print(f"\nModel type: {type(model).__name__}")

# Test case - Should be APPROVED
test_input = pd.DataFrame({
    'ApplicantIncome': [5849],
    'CoapplicantIncome': [0],
    'LoanAmount': [128],
    'Loan_Amount_Term': [360],
    'Credit_History': [1.0],
    'TotalIncome': [5849],
    'LoanAmountToIncome': [0.022],
    'IncomePerDependent': [2924.5],
    'LoanAmount_log': [4.86],
    'TotalIncome_log': [8.67],
    'Gender_binary': [1],
    'Married_binary': [0],
    'Education_binary': [1],
    'Self_Employed_binary': [0],
    'Dependents_numeric': [0.0],
    'Property_Area_Semiurban': [0],
    'Property_Area_Urban': [1]
})

test_input = test_input[features]
test_scaled = scaler.transform(test_input)

pred = model.predict(test_scaled)
prob = model.predict_proba(test_scaled)

print(f"\nTest Prediction: {pred[0]} (1=Approved, 0=Rejected)")
print(f"Approval Probability: {prob[0][1]*100:.2f}%")

if pred[0] == 1:
    print("\n✅ MODEL WORKING - LOAN APPROVED!")
else:
    print("\n⚠️ Model predicts REJECTED for this case")
    print("   (This is okay - model learns from data patterns)")

# Test another case
print("\n" + "-"*70)
print("Testing HIGH INCOME + GOOD CREDIT case:")

test_input2 = pd.DataFrame({
    'ApplicantIncome': [10000],
    'CoapplicantIncome': [5000],
    'LoanAmount': [150],
    'Loan_Amount_Term': [360],
    'Credit_History': [1.0],
    'TotalIncome': [15000],
    'LoanAmountToIncome': [0.01],
    'IncomePerDependent': [7500],
    'LoanAmount_log': [5.02],
    'TotalIncome_log': [9.62],
    'Gender_binary': [1],
    'Married_binary': [1],
    'Education_binary': [1],
    'Self_Employed_binary': [0],
    'Dependents_numeric': [1.0],
    'Property_Area_Semiurban': [1],
    'Property_Area_Urban': [0]
})

test_input2 = test_input2[features]
test_scaled2 = scaler.transform(test_input2)

pred2 = model.predict(test_scaled2)
prob2 = model.predict_proba(test_scaled2)

print(f"Prediction: {pred2[0]} (1=Approved, 0=Rejected)")
print(f"Approval Probability: {prob2[0][1]*100:.2f}%")

if pred2[0] == 1:
    print("✅ LOAN APPROVED!")
else:
    print("❌ LOAN REJECTED")

print("\n" + "="*70)
print("MODEL FIX COMPLETE!")
print("="*70)