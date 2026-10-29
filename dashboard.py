import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# CUSTOMER RETENTION & CHURN ANALYSIS DASHBOARD
# ============================================

# Page configuration
st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Customer Retention & Churn Analysis")

st.markdown(
    """
    Understand customer behaviour, explore churn patterns,
    and identify customer groups with higher churn rates.
    Use the filters in the sidebar to interact with the data.
    """
)

st.divider()


# ============================================
# LOAD CLEANED DATASET
# ============================================

@st.cache_data
def load_data():
    return pd.read_csv("outputs/cleaned_telco_churn.csv")


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "Cleaned dataset not found. Please run task2.py first "
        "and make sure outputs/cleaned_telco_churn.csv exists."
    )
    st.stop()


# ============================================
# INTERACTIVE FILTERS
# ============================================

st.sidebar.header("Filter Customers")

contract_options = ["All"] + sorted(
    df["Contract"].dropna().unique().tolist()
)

internet_options = ["All"] + sorted(
    df["InternetService"].dropna().unique().tolist()
)

churn_options = ["All"] + sorted(
    df["Churn"].dropna().unique().tolist()
)

selected_contract = st.sidebar.selectbox(
    "Contract Type",
    contract_options
)

selected_internet = st.sidebar.selectbox(
    "Internet Service",
    internet_options
)

selected_churn = st.sidebar.selectbox(
    "Churn Status",
    churn_options
)

# Apply contract and internet filters to the analysis data
analysis_df = df.copy()

if selected_contract != "All":
    analysis_df = analysis_df[
        analysis_df["Contract"] == selected_contract
    ]

if selected_internet != "All":
    analysis_df = analysis_df[
        analysis_df["InternetService"] == selected_internet
    ]

# Apply the churn filter to the customer table only.
# This keeps the churn-rate calculations meaningful.
display_df = analysis_df.copy()

if selected_churn != "All":
    display_df = display_df[
        display_df["Churn"] == selected_churn
    ]


# ============================================
# KEY PERFORMANCE INDICATORS
# ============================================

total_customers = len(analysis_df)

churned_customers = (
    analysis_df["Churn"] == "Yes"
).sum()

retained_customers = (
    analysis_df["Churn"] == "No"
).sum()

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0 else 0
)

retention_rate = (
    retained_customers / total_customers * 100
    if total_customers > 0 else 0
)

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Customers Churned",
    f"{churned_customers:,}"
)

col3.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col4.metric(
    "Retention Rate",
    f"{retention_rate:.2f}%"
)

if total_customers == 0:
    st.warning("No customers match the selected filters.")

st.divider()


# ============================================
# CHART 1: CHURN BY CONTRACT TYPE
# ============================================

st.subheader("Churn Analysis")

contract_analysis = (
    analysis_df.groupby("Contract")
    .agg(
        Total_Customers=("customerID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

contract_analysis["Churn_Rate"] = (
    contract_analysis["Churned_Customers"]
    / contract_analysis["Total_Customers"]
) * 100

col1, col2 = st.columns(2)

with col1:
    if not contract_analysis.empty:
        fig_contract = px.bar(
            contract_analysis,
            x="Contract",
            y="Churn_Rate",
            text=(
                contract_analysis["Churn_Rate"]
                .round(1).astype(str) + "%"
            ),
            title="Churn Rate by Contract Type",
            labels={
                "Contract": "Contract Type",
                "Churn_Rate": "Churn Rate (%)"
            },
            color="Churn_Rate",
            color_continuous_scale="Blues"
        )

        fig_contract.update_traces(
            textposition="outside"
        )

        fig_contract.update_layout(
            yaxis_range=[
                0,
                min(
                    100,
                    max(50, contract_analysis["Churn_Rate"].max() + 10)
                )
            ],
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_contract,
            use_container_width=True
        )
    else:
        st.info("No data available for this chart.")


# ============================================
# CHART 2: CHURN BY CUSTOMER TENURE
# ============================================

tenure_bins = [-1, 12, 24, 48, 72]

tenure_labels = [
    "0–12 months",
    "13–24 months",
    "25–48 months",
    "49–72 months"
]

# Create tenure groups using the filtered data
tenure_df = analysis_df.copy()

tenure_df["TenureGroup"] = pd.cut(
    tenure_df["tenure"],
    bins=tenure_bins,
    labels=tenure_labels
)

tenure_analysis = (
    tenure_df.groupby(
        "TenureGroup",
        observed=False
    )
    .agg(
        Total_Customers=("customerID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

# Avoid division by zero for empty groups
tenure_analysis["Churn_Rate"] = (
    tenure_analysis["Churned_Customers"]
    .div(tenure_analysis["Total_Customers"].replace(0, float("nan")))
    .mul(100)
    .fillna(0)
)

with col2:
    if not tenure_analysis.empty:
        fig_tenure = px.bar(
            tenure_analysis,
            x="TenureGroup",
            y="Churn_Rate",
            text=(
                tenure_analysis["Churn_Rate"]
                .round(1).astype(str) + "%"
            ),
            title="Churn Rate by Customer Tenure",
            labels={
                "TenureGroup": "Customer Tenure",
                "Churn_Rate": "Churn Rate (%)"
            },
            color="Churn_Rate",
            color_continuous_scale="Oranges"
        )

        fig_tenure.update_traces(
            textposition="outside"
        )

        fig_tenure.update_layout(
            yaxis_range=[
                0,
                min(
                    100,
                    max(55, tenure_analysis["Churn_Rate"].max() + 10)
                )
            ],
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_tenure,
            use_container_width=True
        )
    else:
        st.info("No data available for this chart.")

st.divider()


# ============================================
# ADDITIONAL CUSTOMER CHURN ANALYSIS
# ============================================

st.subheader("Customer Service and Payment Insights")


def create_churn_chart(data, category, title, x_label):
    analysis = (
        data.groupby(category)
        .agg(
            Total_Customers=("customerID", "count"),
            Churned_Customers=(
                "Churn",
                lambda x: (x == "Yes").sum()
            )
        )
        .reset_index()
    )

    analysis["Churn_Rate"] = (
        analysis["Churned_Customers"]
        / analysis["Total_Customers"]
    ) * 100

    fig = px.bar(
        analysis,
        x=category,
        y="Churn_Rate",
        text=(
            analysis["Churn_Rate"]
            .round(1).astype(str) + "%"
        ),
        title=title,
        labels={
            category: x_label,
            "Churn_Rate": "Churn Rate (%)"
        },
        color="Churn_Rate",
        color_continuous_scale="Teal"
    )

    fig.update_traces(
        textposition="outside"
    )

    max_rate = (
        analysis["Churn_Rate"].max()
        if not analysis.empty else 0
    )

    fig.update_layout(
        yaxis_range=[
            0,
            min(100, max(10, max_rate + 10))
        ],
        coloraxis_showscale=False
    )

    return fig


# ============================================
# CHART 3: CHURN BY PAYMENT METHOD
# ============================================

col1, col2 = st.columns(2)

with col1:
    payment_fig = create_churn_chart(
        analysis_df,
        "PaymentMethod",
        "Churn Rate by Payment Method",
        "Payment Method"
    )

    st.plotly_chart(
        payment_fig,
        use_container_width=True
    )


# ============================================
# CHART 4: CHURN BY INTERNET SERVICE
# ============================================

with col2:
    internet_fig = create_churn_chart(
        analysis_df,
        "InternetService",
        "Churn Rate by Internet Service",
        "Internet Service"
    )

    st.plotly_chart(
        internet_fig,
        use_container_width=True
    )


# ============================================
# CHART 5: CHURN BY TECHNICAL SUPPORT
# ============================================

col1, col2 = st.columns(2)

with col1:
    support_fig = create_churn_chart(
        analysis_df,
        "TechSupport",
        "Churn Rate by Technical Support",
        "Technical Support"
    )

    st.plotly_chart(
        support_fig,
        use_container_width=True
    )


# ============================================
# CHART 6: CHURN BY ONLINE SECURITY
# ============================================

with col2:
    security_fig = create_churn_chart(
        analysis_df,
        "OnlineSecurity",
        "Churn Rate by Online Security",
        "Online Security"
    )

    st.plotly_chart(
        security_fig,
        use_container_width=True
    )

st.divider()


# ============================================
# PREVIEW FILTERED CUSTOMER DATA
# ============================================

with st.expander("View cleaned customer data"):
    st.write(
        f"Showing {len(display_df):,} customer records."
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )

st.caption(
    "Data source: Telco Customer Churn dataset. "
    "Contract and internet service filters update the KPIs "
    "and charts. Churn status filters the customer data table."
)

# ============================================
# KEY FINDINGS
# ============================================

st.divider()

st.subheader("Key Findings")

st.markdown("""
### 1. Contract Type
Month-to-month customers have a much higher churn rate
than customers with one-year or two-year contracts.

### 2. Customer Tenure
Customers with shorter tenures show higher churn rates.
The first 12 months are an important period to examine
when planning customer retention strategies.

### 3. Payment Method
Customers using electronic checks have a higher churn
rate than customers using automatic payment methods.

### 4. Internet Service
Fiber optic customers show a higher churn rate than
DSL customers in this dataset.

### 5. Technical Support and Online Security
Customers without technical support or online security
show higher churn rates than customers who have these
services.

### Overall Conclusion
The analysis identifies customer groups with different
churn rates. The company could investigate these groups
further and evaluate targeted retention strategies.
""")
