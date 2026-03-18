import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Loan Default Predictor",
    page_icon="🏦",
    layout="wide"
)

# Load model and preprocessing tools
import os

@st.cache_resource
def load_model():
    # Get the directory where app.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build full paths
    model_path = os.path.join(base_dir, 'models', 'best_loan_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    features_path = os.path.join(base_dir, 'models', 'feature_names.pkl')
    
    # Load
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(features_path)
    
    return model, scaler, feature_names

try:
    model, scaler, feature_names = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Error loading model: {e}")

# App Title
st.title("🏦 Loan Default Prediction System")
st.markdown("### Predict loan approval in real-time using Machine Learning")
st.markdown("---")

if not model_loaded:
    st.stop()

# Sidebar
st.sidebar.header("ℹ️ About")
st.sidebar.info(
    """
    **Loan Default Predictor**
    
    ML model predicts loan approval.
    
    **Accuracy:** 81.3%
    **Model:** Random Forest
    
    Built by: Nainil Shah
    """
)

st.sidebar.markdown("---")
st.sidebar.header("📊 Model Info")
st.sidebar.metric("Accuracy", "81.3%")
st.sidebar.metric("Features", len(feature_names))

# Debug toggle
show_debug = st.sidebar.checkbox("Show Debug Info", value=False)

# Main form
st.header("📝 Enter Customer Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Personal Information")
    customer_name = st.text_input("Customer Name", "John Doe")
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Marital Status", ["Yes", "No"])
    dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])

with col2:
    st.subheader("Financial Information")
    applicant_income = st.number_input(
        "Monthly Income (₹)", 
        min_value=0, 
        max_value=1000000, 
        value=50000,
        step=1000
    )
    coapplicant_income = st.number_input(
        "Co-applicant Income (₹)", 
        min_value=0, 
        max_value=1000000, 
        value=0,
        step=1000
    )
    loan_amount = st.number_input(
        "Loan Amount (₹ in thousands)", 
        min_value=10, 
        max_value=10000, 
        value=200,
        step=10,
        help="Enter in thousands (e.g., 200 for 2 Lakhs)"
    )
    loan_term = st.selectbox(
        "Loan Term (months)", 
        [360, 180, 120, 60, 36],
        index=0
    )

with col3:
    st.subheader("Additional Details")
    self_employed = st.selectbox("Self Employed?", ["No", "Yes"])
    credit_history = st.selectbox(
        "Credit History", 
        ["1 - Good", "0 - Poor/None"]
    )
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

st.markdown("---")

# Predict button
if st.button("🔮 PREDICT LOAN APPROVAL", type="primary", use_container_width=True):
    
    with st.spinner("Analyzing..."):
        
        # Convert inputs
        gender_binary = 1 if gender == "Male" else 0
        married_binary = 1 if married == "Yes" else 0
        education_binary = 1 if education == "Graduate" else 0
        self_employed_binary = 1 if self_employed == "Yes" else 0
        credit_history_value = 1.0 if credit_history.startswith("1") else 0.0
        
        dependents_numeric = 3.0 if dependents == "3+" else float(dependents)
        
        # Property area
        property_area_semiurban = 1 if property_area == "Semiurban" else 0
        property_area_urban = 1 if property_area == "Urban" else 0
        
        # Derived features
        total_income = applicant_income + coapplicant_income
        loan_to_income = loan_amount / total_income if total_income > 0 else 0
        income_per_dependent = total_income / (dependents_numeric + 1)
        loan_amount_log = np.log(loan_amount + 1)
        total_income_log = np.log(total_income + 1)
        
        # Create input - EXACT order as trained model
        input_data = pd.DataFrame({
            'ApplicantIncome': [float(applicant_income)],
            'CoapplicantIncome': [float(coapplicant_income)],
            'LoanAmount': [float(loan_amount)],
            'Loan_Amount_Term': [float(loan_term)],
            'Credit_History': [credit_history_value],
            'TotalIncome': [float(total_income)],
            'LoanAmountToIncome': [loan_to_income],
            'IncomePerDependent': [income_per_dependent],
            'LoanAmount_log': [loan_amount_log],
            'TotalIncome_log': [total_income_log],
            'Gender_binary': [float(gender_binary)],
            'Married_binary': [float(married_binary)],
            'Education_binary': [float(education_binary)],
            'Self_Employed_binary': [float(self_employed_binary)],
            'Dependents_numeric': [dependents_numeric],
            'Property_Area_Semiurban': [float(property_area_semiurban)],
            'Property_Area_Urban': [float(property_area_urban)]
        })
        
        # Debug info
        if show_debug:
            st.write("**Debug: Feature Names Expected:**")
            st.write(feature_names)
            st.write("**Debug: Input Data Columns:**")
            st.write(input_data.columns.tolist())
            st.write("**Debug: Input Data Values:**")
            st.write(input_data)
        
        # Ensure correct order
        input_data = input_data[feature_names]
        
        # Scale
        input_scaled = scaler.transform(input_data)
        
        if show_debug:
            st.write("**Debug: Scaled Data:**")
            st.write(input_scaled)
        
        # Predict
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)
        
        approval_prob = probability[0][1] * 100
        rejection_prob = probability[0][0] * 100
    
    # Results
    st.markdown("---")
    st.header("📊 Prediction Results")
    
    st.subheader(f"Customer: {customer_name}")
    
    result_col1, result_col2 = st.columns(2)
    
    with result_col1:
        if prediction[0] == 1:
            st.success("### ✅ LOAN APPROVED")
            st.metric("Approval Confidence", f"{approval_prob:.1f}%")
            st.balloons()
        else:
            st.error("### ❌ LOAN REJECTED")
            st.metric("Rejection Confidence", f"{rejection_prob:.1f}%")
    
    with result_col2:
        st.info("**Probability Distribution**")
        st.metric("Approval Probability", f"{approval_prob:.1f}%")
        st.metric("Rejection Probability", f"{rejection_prob:.1f}%")
        st.progress(approval_prob / 100)
    
    # Analysis
    st.markdown("---")
    st.subheader("📋 Customer Profile")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric("Total Income", f"₹{total_income:,}")
        st.metric("Loan Amount", f"₹{loan_amount * 1000:,}")
    
    with col_b:
        st.metric("Credit History", "✅ Good" if credit_history_value == 1 else "❌ Poor")
        st.metric("Education", education)
    
    with col_c:
        st.metric("Marital Status", married)
        st.metric("Property Area", property_area)
    
    # Key factors
    st.markdown("---")
    st.subheader("🔍 Key Factors")
    
    if credit_history_value == 0:
        st.error("❌ **No Credit History** - Major negative factor")
    else:
        st.success("✅ **Good Credit History** - Strong positive factor")
    
    if loan_to_income > 0.05:
        st.warning(f"⚠️ **Loan-to-Income Ratio: {loan_to_income:.4f}** - High ratio")
    else:
        st.success(f"✅ **Loan-to-Income Ratio: {loan_to_income:.4f}** - Healthy")
    
    if total_income < 3000:
        st.warning("⚠️ **Low Income** - May affect approval")
    elif total_income > 10000:
        st.success("✅ **High Income** - Strong factor")
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
    if prediction[0] == 1:
        st.success(
            f"""
            **✅ RECOMMENDED FOR APPROVAL**
            - Approval confidence: {approval_prob:.1f}%
            - Customer shows good repayment capacity
            - Standard interest rate applicable
            """
        )
    else:
        st.warning(
            f"""
            **❌ NOT RECOMMENDED**
            - Rejection confidence: {rejection_prob:.1f}%
            - High risk of default
            - Consider: higher interest rate or additional collateral
            """
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built by Nainil Shah | Model Accuracy: 81.3% | 
        <a href='https://github.com/Nainilshah04/loan-default-prediction'>GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)