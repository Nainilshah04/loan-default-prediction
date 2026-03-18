import sqlite3
import pandas as pd
import os

print("="*70)
print("🔍 RUNNING SQL ANALYSIS QUERIES")
print("="*70)

# Database path
db_path = 'data/loan_database.db'

# Check if database exists
if not os.path.exists(db_path):
    print(f"\n❌ Error: Database not found at {db_path}")
    print("Please run sql/01_create_database.py first")
    exit()

# Connect to database
conn = sqlite3.connect(db_path)

# Read SQL file
sql_file = 'sql/02_exploratory_queries.sql'
with open(sql_file, 'r') as f:
    sql_content = f.read()

# Split queries by separator
queries = sql_content.split('-- ========================================')

# Create results folder
os.makedirs('sql/query_results', exist_ok=True)

# Execute each query
query_num = 0
for query_block in queries:
    # Skip empty blocks or comments-only blocks
    if 'SELECT' not in query_block:
        continue
    
    query_num += 1
    
    # Extract query description
    lines = query_block.strip().split('\n')
    description = ""
    for line in lines:
        if '-- Business Question:' in line:
            description = line.replace('-- Business Question:', '').strip()
            break
    
    # Extract the actual SQL query
    sql_query = '\n'.join([line for line in lines if not line.strip().startswith('--')])
    
    if sql_query.strip():
        print(f"\n{'='*70}")
        print(f"📊 QUERY {query_num}: {description}")
        print(f"{'='*70}")
        
        try:
            # Execute query
            result = pd.read_sql(sql_query, conn)
            
            # Display result
            print(result.to_string(index=False))
            
            # Save to CSV
            output_file = f'sql/query_results/query_{query_num:02d}_result.csv'
            result.to_csv(output_file, index=False)
            print(f"\n💾 Saved to: {output_file}")
            
        except Exception as e:
            print(f"\n❌ Error executing query: {e}")

# Close connection
conn.close()

print(f"\n{'='*70}")
print("✅ All queries executed successfully!")
print(f"📂 Results saved in: sql/query_results/")
print(f"{'='*70}")