import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
import time

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Loan Default Predictor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# MINIMAL CLEAN CSS
# ============================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        margin: 6px 0;
    }

    .card-val {
        font-size: 30px;
        font-weight: 700;
        color: #2563EB;
        margin: 4px 0;
    }

    .card-label {
        font-size: 13px;
        font-weight: 500;
        color: #334155;
        margin-top: 4px;
    }

    .score-big {
        font-size: 52px;
        font-weight: 700;
        line-height: 1;
        margin: 8px 0;
    }

    .clr-green { color: #10B981; }
    .clr-amber { color: #F59E0B; }
    .clr-red { color: #EF4444; }

    .badge-green {
        display: inline-block;
        padding: 5px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        background: #D1FAE5;
        color: #065F46;
    }

    .badge-red {
        display: inline-block;
        padding: 5px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        background: #FEE2E2;
        color: #991B1B;
    }

    .info {
        background: #EFF6FF;
        border-left: 4px solid #2563EB;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 10px 0;
        color: #1E40AF;
        font-size: 13px;
    }

    .res-green {
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 10px 0;
        color: #065F46;
        font-size: 14px;
        line-height: 1.7;
    }

    .res-red {
        background: #FFF1F2;
        border-left: 4px solid #EF4444;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 10px 0;
        color: #991B1B;
        font-size: 14px;
        line-height: 1.7;
    }

    .section-gap {
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD MODEL
# ============================================
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(base_dir, 'models', 'best_loan_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    features_path = os.path.join(base_dir, 'models', 'feature_names.pkl')

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(features_path)

    return model, scaler, feature_names

try:
    model, scaler, feature_names = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Model loading failed: {e}")

if not model_loaded:
    st.stop()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### Loan Default Predictor")
    st.caption("Machine Learning Based Credit Decision Support")
    st.markdown("---")

    st.metric("Model Accuracy", "81.3%")
    st.metric("Model Type", "Random Forest")
    st.metric("Features Used", len(feature_names))

    st.markdown("---")
    st.markdown("**Model Notes**")
    st.markdown("""
    - Trained on structured loan application data
    - Uses engineered income and repayment features
    - Supports real-time approval prediction
    """)

    st.markdown("---")
    show_debug = st.checkbox("Show Debug Information", value=False)

# ============================================
# HEADER
# ============================================
st.title("Loan Default Prediction System")
st.markdown("Generate a real-time loan approval assessment using machine learning")

st.markdown("""
<div class="info">
This application evaluates applicant profile, income strength, credit history, and repayment capacity to estimate loan approval probability.
</div>
""", unsafe_allow_html=True)

# ============================================
# TOP KPI CARDS
# ============================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-val">81.3%</div>
        <div class="card-label">Model Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-val">17</div>
        <div class="card-label">Engineered Features</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-val">Real-Time</div>
        <div class="card-label">Prediction Output</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# FORM
# ============================================
st.subheader("Applicant Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Personal Information")
    customer_name = st.text_input("Applicant Name", "John Doe")
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Marital Status", ["Yes", "No"])
    dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])

with col2:
    st.markdown("#### Financial Information")
    applicant_income = st.number_input(
        "Applicant Monthly Income (INR)",
        min_value=0,
        max_value=1000000,
        value=50000,
        step=1000
    )
    coapplicant_income = st.number_input(
        "Co-applicant Monthly Income (INR)",
        min_value=0,
        max_value=1000000,
        value=0,
        step=1000
    )
    loan_amount = st.number_input(
        "Loan Amount (INR in thousands)",
        min_value=10,
        max_value=10000,
        value=200,
        step=10,
        help="Example: Enter 200 for INR 2,00,000"
    )
    loan_term = st.selectbox(
        "Loan Term (Months)",
        [360, 180, 120, 60, 36],
        index=0
    )

with col3:
    st.markdown("#### Additional Details")
    self_employed = st.selectbox("Self Employed", ["No", "Yes"])
    credit_history = st.selectbox(
        "Credit History",
        ["1 - Good", "0 - Poor/None"]
    )
    property_area = st.selectbox(
        "Property Area",
        ["Urban", "Semiurban", "Rural"]
    )

st.markdown("---")

# ============================================
# PREDICTION
# ============================================
if st.button("Generate Loan Assessment", type="primary", use_container_width=True):

    with st.spinner("Processing application..."):
        progress = st.progress(0)
        for i, step in enumerate([
            "Reading applicant details",
            "Engineering derived features",
            "Scaling input data",
            "Running prediction model",
            "Generating assessment output"
        ]):
            progress.progress((i + 1) / 5, text=step)
            time.sleep(0.35)

        # Convert inputs
        gender_binary = 1 if gender == "Male" else 0
        married_binary = 1 if married == "Yes" else 0
        education_binary = 1 if education == "Graduate" else 0
        self_employed_binary = 1 if self_employed == "Yes" else 0
        credit_history_value = 1.0 if credit_history.startswith("1") else 0.0
        dependents_numeric = 3.0 if dependents == "3+" else float(dependents)

        property_area_semiurban = 1 if property_area == "Semiurban" else 0
        property_area_urban = 1 if property_area == "Urban" else 0

        # Derived features
        total_income = applicant_income + coapplicant_income
        loan_to_income = loan_amount / total_income if total_income > 0 else 0
        income_per_dependent = total_income / (dependents_numeric + 1)
        loan_amount_log = np.log(loan_amount + 1)
        total_income_log = np.log(total_income + 1)

        # Input DataFrame
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

        if show_debug:
            st.write("Expected Features:", feature_names)
            st.write("Input Data:", input_data)

        input_data = input_data[feature_names]
        input_scaled = scaler.transform(input_data)

        if show_debug:
            st.write("Scaled Input:", input_scaled)

        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)

        approval_prob = probability[0][1] * 100
        rejection_prob = probability[0][0] * 100

    # ============================================
    # RESULTS
    # ============================================
    st.markdown("---")
    st.subheader("Assessment Results")
    st.markdown(f"Evaluation generated for **{customer_name}**")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        if prediction[0] == 1:
            st.markdown("""
            <div class="card">
                <div class="card-label">DECISION</div>
                <div style="margin-top:14px;"><span class="badge-green">APPROVED</span></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <div class="card-label">DECISION</div>
                <div style="margin-top:14px;"><span class="badge-red">REJECTED</span></div>
            </div>
            """, unsafe_allow_html=True)

    with result_col2:
        if prediction[0] == 1:
            st.markdown(f"""
            <div class="card">
                <div class="card-label">APPROVAL CONFIDENCE</div>
                <div class="score-big clr-green">{approval_prob:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card">
                <div class="card-label">REJECTION CONFIDENCE</div>
                <div class="score-big clr-red">{rejection_prob:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

    with result_col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">LOAN AMOUNT REQUESTED</div>
            <div class="card-val">₹{loan_amount * 1000:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Probabilities
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Approval Probability", f"{approval_prob:.1f}%")
    with col2:
        st.metric("Rejection Probability", f"{rejection_prob:.1f}%")

    st.progress(approval_prob / 100)

    st.markdown("---")

    # ============================================
    # APPLICANT SUMMARY
    # ============================================
    st.subheader("Applicant Summary")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Total Monthly Income", f"₹{total_income:,}")
        st.metric("Loan Amount", f"₹{loan_amount * 1000:,}")

    with col_b:
        st.metric("Credit History", "Good" if credit_history_value == 1 else "Poor / None")
        st.metric("Education", education)

    with col_c:
        st.metric("Marital Status", married)
        st.metric("Property Area", property_area)

    st.markdown("---")

    # ============================================
    # KEY FACTORS
    # ============================================
    st.subheader("Key Factors Influencing the Decision")

    if credit_history_value == 0:
        st.error("Credit history is weak or unavailable — this is a major negative factor")
    else:
        st.success("Credit history is strong — this is a major positive factor")

    if loan_to_income > 0.05:
        st.warning(f"Loan-to-income ratio is high ({loan_to_income:.4f}) — repayment burden may be elevated")
    else:
        st.success(f"Loan-to-income ratio is healthy ({loan_to_income:.4f})")

    if total_income < 3000:
        st.warning("Total income is low — affordability may be a concern")
    elif total_income > 10000:
        st.success("Total income is strong — repayment capacity is favorable")

    if dependents_numeric >= 3:
        st.warning("Higher dependency count may increase household financial pressure")
    else:
        st.success("Dependency burden is manageable")

    st.markdown("---")

    # ============================================
    # FINAL RECOMMENDATION
    # ============================================
    st.subheader("Recommendation")

    if prediction[0] == 1:
        st.markdown(f"""
        <div class="res-green">
            <strong>Recommended for Approval</strong><br>
            {customer_name} demonstrates acceptable repayment capacity based on current income, credit history, and loan characteristics.
            Estimated approval confidence: {approval_prob:.1f}%.
            Standard pricing and documentation review may be applied.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="res-red">
            <strong>Not Recommended for Approval</strong><br>
            {customer_name} shows elevated default risk based on current income profile, credit history, or repayment burden.
            Estimated rejection confidence: {rejection_prob:.1f}%.
            Consider additional collateral, lower loan amount, or manual underwriting review.
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; color:#334155; font-size:14px;'>
        Built by Nainil Shah | Random Forest Model | Accuracy: 81.3% |
        <a href='https://github.com/Nainilshah04/loan-default-prediction' style='color:#2563EB; text-decoration:none;'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)