# ========================================
# PROFESSIONAL DASHBOARD - CLEAN VERSION
# ========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Change to project root if needed
if os.path.basename(os.getcwd()) == 'notebooks':
    os.chdir('..')

print("="*70)
print("CREATING PROFESSIONAL DASHBOARD")
print("="*70)

# Set professional style
plt.style.use('default')
sns.set_palette("Set2")

# Load data
df = pd.read_csv('powerbi/loan_data_for_powerbi.csv')
print(f"\nData loaded: {df.shape[0]} rows")

# Create images folder
os.makedirs('images', exist_ok=True)

# ========================================
# PROFESSIONAL DASHBOARD
# ========================================

fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor('white')

# Main title
fig.suptitle('LOAN DEFAULT PREDICTION - EXECUTIVE DASHBOARD', 
             fontsize=22, fontweight='bold', y=0.98, color='#2C3E50')

# ========================================
# TOP ROW: KPI CARDS
# ========================================

# Calculate KPIs
total_apps = len(df)
approval_rate = df['Loan_Status_Numeric'].mean() * 100
high_risk = df['Risk_Category'].isin(['High Risk', 'Very High Risk']).sum()
est_loss = df[df['Risk_Category'].isin(['High Risk', 'Very High Risk'])]['Estimated_Loss_If_Default'].sum() / 100000

# KPI 1
ax1 = plt.subplot(3, 4, 1)
ax1.text(0.5, 0.65, f"{total_apps:,}", fontsize=36, ha='center', va='center', 
         fontweight='bold', color='#34495E')
ax1.text(0.5, 0.25, 'Total Applications', fontsize=11, ha='center', color='#7F8C8D')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
ax1.add_patch(plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#ECF0F1', 
                            edgecolor='#BDC3C7', linewidth=2))

# KPI 2
ax2 = plt.subplot(3, 4, 2)
ax2.text(0.5, 0.65, f"{approval_rate:.1f}%", fontsize=36, ha='center', va='center', 
         fontweight='bold', color='#27AE60')
ax2.text(0.5, 0.25, 'Approval Rate', fontsize=11, ha='center', color='#7F8C8D')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
ax2.add_patch(plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#D5F4E6', 
                            edgecolor='#27AE60', linewidth=2))

# KPI 3
ax3 = plt.subplot(3, 4, 3)
ax3.text(0.5, 0.65, f"{high_risk:,}", fontsize=36, ha='center', va='center', 
         fontweight='bold', color='#E74C3C')
ax3.text(0.5, 0.25, 'High Risk Customers', fontsize=11, ha='center', color='#7F8C8D')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.add_patch(plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#FADBD8', 
                            edgecolor='#E74C3C', linewidth=2))

# KPI 4
ax4 = plt.subplot(3, 4, 4)
ax4.text(0.5, 0.65, f"Rs {est_loss:.1f}L", fontsize=32, ha='center', va='center', 
         fontweight='bold', color='#8E44AD')
ax4.text(0.5, 0.25, 'Potential Loss (High Risk)', fontsize=11, ha='center', color='#7F8C8D')
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')
ax4.add_patch(plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#EBDEF0', 
                            edgecolor='#8E44AD', linewidth=2))

# ========================================
# MIDDLE ROW: KEY CHARTS
# ========================================

# Chart 1: Credit History Impact
ax5 = plt.subplot(3, 4, 5)
credit_approval = df.groupby('Credit_History')['Loan_Status_Numeric'].mean() * 100
bars = ax5.bar(['No History', 'Has History'], credit_approval.values, 
               color=['#E74C3C', '#27AE60'], edgecolor='black', linewidth=1.5, width=0.6)
ax5.set_ylabel('Approval Rate (%)', fontsize=11, fontweight='bold')
ax5.set_title('Credit History Impact', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')
ax5.set_ylim(0, 100)
ax5.grid(axis='y', alpha=0.3, linestyle='--')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
for i, v in enumerate(credit_approval.values):
    ax5.text(i, v + 3, f'{v:.1f}%', ha='center', fontsize=11, fontweight='bold')

# Chart 2: Approval Status Distribution
ax6 = plt.subplot(3, 4, 6)
approval_counts = df['Loan_Approved'].value_counts()
colors = ['#27AE60', '#E74C3C']
wedges, texts, autotexts = ax6.pie(approval_counts, labels=['Approved', 'Rejected'], 
                                    autopct='%1.1f%%', colors=colors, startangle=90,
                                    textprops={'fontsize': 11, 'weight': 'bold'})
for autotext in autotexts:
    autotext.set_color('white')
ax6.set_title('Loan Status Distribution', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')

# Chart 3: Risk Category Distribution
ax7 = plt.subplot(3, 4, 7)
risk_counts = df['Risk_Category'].value_counts()
risk_order = ['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
risk_counts = risk_counts.reindex([r for r in risk_order if r in risk_counts.index])
colors_risk = ['#27AE60', '#F39C12', '#E74C3C', '#8E44AD']
ax7.barh(range(len(risk_counts)), risk_counts.values, 
         color=colors_risk[:len(risk_counts)], edgecolor='black', linewidth=1)
ax7.set_yticks(range(len(risk_counts)))
ax7.set_yticklabels(risk_counts.index, fontsize=10)
ax7.set_xlabel('Number of Customers', fontsize=11, fontweight='bold')
ax7.set_title('Risk Category Breakdown', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')
ax7.grid(axis='x', alpha=0.3, linestyle='--')
ax7.spines['top'].set_visible(False)
ax7.spines['right'].set_visible(False)
for i, v in enumerate(risk_counts.values):
    ax7.text(v + 5, i, str(v), va='center', fontsize=10, fontweight='bold')

# Chart 4: Approval by Property Area
ax8 = plt.subplot(3, 4, 8)
area_approval = df.groupby('Property_Area')['Loan_Status_Numeric'].mean() * 100
area_approval = area_approval.sort_values()
bars = ax8.barh(range(len(area_approval)), area_approval.values, color='#3498DB', 
                edgecolor='black', linewidth=1, height=0.6)
ax8.set_yticks(range(len(area_approval)))
ax8.set_yticklabels(area_approval.index, fontsize=10)
ax8.set_xlabel('Approval Rate (%)', fontsize=11, fontweight='bold')
ax8.set_title('Approval Rate by Area', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')
ax8.set_xlim(0, 100)
ax8.grid(axis='x', alpha=0.3, linestyle='--')
ax8.spines['top'].set_visible(False)
ax8.spines['right'].set_visible(False)
for i, v in enumerate(area_approval.values):
    ax8.text(v + 2, i, f'{v:.1f}%', va='center', fontsize=10, fontweight='bold')

# ========================================
# BOTTOM ROW: DETAILED ANALYSIS
# ========================================

# Chart 5: Income Distribution by Approval
ax9 = plt.subplot(3, 4, 9)
approved = df[df['Loan_Approved']=='Approved']['Total_Income']
rejected = df[df['Loan_Approved']=='Rejected']['Total_Income']
bp = ax9.boxplot([rejected, approved], tick_labels=['Rejected', 'Approved'], patch_artist=True)
bp['boxes'][0].set_facecolor('#E74C3C')
bp['boxes'][1].set_facecolor('#27AE60')
ax9.set_ylabel('Total Income', fontsize=11, fontweight='bold')
ax9.set_title('Income by Status', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')
ax9.grid(axis='y', alpha=0.3, linestyle='--')
ax9.spines['top'].set_visible(False)
ax9.spines['right'].set_visible(False)

# Chart 6: Loan Amount by Education
ax10 = plt.subplot(3, 4, 10)
edu_loan = df.groupby('Education')['LoanAmount'].mean()
bars = ax10.bar(range(len(edu_loan)), edu_loan.values, color=['#9B59B6', '#1ABC9C'], 
                edgecolor='black', linewidth=1.5, width=0.6)
ax10.set_xticks(range(len(edu_loan)))
ax10.set_xticklabels(['Graduate', 'Not Grad'], fontsize=10)
ax10.set_ylabel('Avg Loan Amount', fontsize=11, fontweight='bold')
ax10.set_title('Loan by Education', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')
ax10.grid(axis='y', alpha=0.3, linestyle='--')
ax10.spines['top'].set_visible(False)
ax10.spines['right'].set_visible(False)
for i, v in enumerate(edu_loan.values):
    ax10.text(i, v + 3, f'{v:.0f}', ha='center', fontsize=10, fontweight='bold')

# Chart 7: Self-Employed vs Salaried Approval
ax11 = plt.subplot(3, 4, 11)
emp_approval = df.groupby('Self_Employed')['Loan_Status_Numeric'].mean() * 100
bars = ax11.bar(['Salaried', 'Self-Emp'], [emp_approval['No'], emp_approval['Yes']], 
                color=['#16A085', '#D68910'], edgecolor='black', linewidth=1.5, width=0.6)
ax11.set_ylabel('Approval Rate (%)', fontsize=11, fontweight='bold')
ax11.set_title('Employment Impact', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')
ax11.set_ylim(0, 100)
ax11.grid(axis='y', alpha=0.3, linestyle='--')
ax11.spines['top'].set_visible(False)
ax11.spines['right'].set_visible(False)
for i, v in enumerate([emp_approval['No'], emp_approval['Yes']]):
    ax11.text(i, v + 3, f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')

# Chart 8: Married vs Unmarried
ax12 = plt.subplot(3, 4, 12)
marital_approval = df.groupby('Married')['Loan_Status_Numeric'].mean() * 100
bars = ax12.bar(['Single', 'Married'], [marital_approval['No'], marital_approval['Yes']], 
                color=['#E67E22', '#2ECC71'], edgecolor='black', linewidth=1.5, width=0.6)
ax12.set_ylabel('Approval Rate (%)', fontsize=11, fontweight='bold')
ax12.set_title('Marital Status Impact', fontsize=13, fontweight='bold', pad=10, color='#2C3E50')
ax12.set_ylim(0, 100)
ax12.grid(axis='y', alpha=0.3, linestyle='--')
ax12.spines['top'].set_visible(False)
ax12.spines['right'].set_visible(False)
for i, v in enumerate([marital_approval['No'], marital_approval['Yes']]):
    ax12.text(i, v + 3, f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.97])

# Save dashboard
dashboard_path = 'images/dashboard_clean.png'
plt.savefig(dashboard_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"\nDashboard saved: {os.path.abspath(dashboard_path)}")
print(f"File size: {os.path.getsize(dashboard_path)/1024:.1f} KB")

print("\n" + "="*70)
print("PROFESSIONAL DASHBOARD CREATED SUCCESSFULLY!")
print("="*70)