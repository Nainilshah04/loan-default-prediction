import pandas as pd
import sqlite3
import os

print("="*70)
print("🗄️  CREATING SQLITE DATABASE FROM LOAN DATA")
print("="*70)

# Paths
csv_path = 'data/loan_data.csv'
db_path = 'data/loan_database.db'

# Check if CSV exists
if not os.path.exists(csv_path):
    print(f"\n❌ Error: CSV file not found at {csv_path}")
    print("Please ensure loan_data.csv is in the data/ folder")
    exit()

# Load CSV
print(f"\n📂 Loading data from: {csv_path}")
df = pd.read_csv(csv_path)
print(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")

# Display columns
print(f"\n📋 Columns in dataset:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:2d}. {col:25s} - {df[col].dtype}")

# Create SQLite database
print(f"\n🗄️  Creating SQLite database: {db_path}")

# Connect to SQLite (creates file if doesn't exist)
conn = sqlite3.connect(db_path)

# Write DataFrame to SQLite
df.to_sql('loans', conn, if_exists='replace', index=False)

print(f"✅ Data successfully loaded into 'loans' table")

# Verify data
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM loans")
count = cursor.fetchone()[0]
print(f"✅ Verified: {count:,} rows in database")

# Show sample data
print(f"\n🔍 First 3 rows from database:")
sample = pd.read_sql("SELECT * FROM loans LIMIT 3", conn)
print(sample)

# Get table info
print(f"\n📊 Table Schema:")
cursor.execute("PRAGMA table_info(loans)")
schema = cursor.fetchall()
for col in schema:
    print(f"   {col[1]:25s} - {col[2]}")

# Close connection
conn.close()

print(f"\n✅ Database created successfully!")
print(f"📍 Location: {os.path.abspath(db_path)}")
print("="*70)