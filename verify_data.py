import pandas as pd
import numpy as np
import os

print("="*60)
print("🔍 LOAN DEFAULT PREDICTION - DATA VERIFICATION")
print("="*60)

# Dataset path
data_path = 'data/loan_data.csv'

# Check if file exists
if os.path.exists(data_path):
    print("\n✅ Dataset found!")
    print(f"📍 Location: {os.path.abspath(data_path)}")
    
    # Load dataset
    df = pd.read_csv(data_path)
    
    # Basic info
    print(f"\n📊 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    print(f"\n📋 Column Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n🔍 First 5 Rows:")
    print(df.head())
    
    print(f"\n📈 Data Types:")
    print(df.dtypes)
    
    print(f"\n🔢 Missing Values:")
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Missing %': missing_percent.values
    })
    print(missing_df[missing_df['Missing Count'] > 0])
    
    print(f"\n📊 Basic Statistics:")
    print(df.describe())
    
    print(f"\n✅ Data verification complete!")
    print("="*60)
    
else:
    print("\n❌ Dataset NOT found!")
    print(f"📍 Expected location: {os.path.abspath(data_path)}")
    print("\n📥 Please download dataset from Kaggle:")
    print("   1. Go to https://www.kaggle.com/datasets")
    print("   2. Search: 'loan prediction dataset'")
    print("   3. Download CSV file")
    print("   4. Place in 'data/' folder")
    print("   5. Rename to 'loan_data.csv'")
    print("="*60)