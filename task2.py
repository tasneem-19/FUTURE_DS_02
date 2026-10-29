

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create an output folder for charts and reports
os.makedirs("outputs", exist_ok=True)

# Load the dataset
df = pd.read_csv(
    "churn_data.csv"
)

# Display the first five rows
print("\n--- FIRST FIVE ROWS ---")
print(df.head())

# Display dataset information
print("\n--- DATASET INFORMATION ---")
df.info()

# Check dataset dimensions
print("\n--- DATASET SHAPE ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Check for duplicate rows
print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

# Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# Remove duplicate rows, if any
df = df.drop_duplicates()

# Convert TotalCharges to numeric
# Blank or invalid entries will become NaN
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Check missing TotalCharges after conversion
print("\n--- MISSING TOTAL CHARGES ---")
print(df["TotalCharges"].isnull().sum())

# Investigate records with missing TotalCharges
print("\n--- CUSTOMERS WITH MISSING TOTAL CHARGES ---")
print(
    df.loc[
        df["TotalCharges"].isnull(),
        ["customerID", "tenure", "MonthlyCharges", "Churn"]
    ]
)

# These blank values occur for customers with zero tenure.
# Since they have no recorded tenure, fill TotalCharges
# with 0 rather than inventing a charge.
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Check the cleaned data
print("\n--- CLEANED DATA ---")
print(df.info())
print(df.isnull().sum().sum())

# Save the cleaned dataset
df.to_csv("outputs/cleaned_telco_churn.csv", index=False)

print("\nData cleaning completed!")

# ============================================
# PART 2: OVERALL CHURN ANALYSIS
# ============================================

# Count customers who stayed and left
churn_counts = df["Churn"].value_counts()

# Calculate total customers
total_customers = len(df)

# Calculate customers who left and stayed
churned_customers = (df["Churn"] == "Yes").sum()
retained_customers = (df["Churn"] == "No").sum()

# Calculate churn and retention rates
churn_rate = (churned_customers / total_customers) * 100
retention_rate = (retained_customers / total_customers) * 100

# Display results
print("\n--- OVERALL CHURN ANALYSIS ---")
print("Total Customers:", total_customers)
print("Customers Who Left:", churned_customers)
print("Customers Who Stayed:", retained_customers)
print(f"Churn Rate: {churn_rate:.2f}%")
print(f"Retention Rate: {retention_rate:.2f}%")

# Visualize customer churn distribution
plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Churn",
    hue="Churn",
    palette={"No": "seagreen", "Yes": "tomato"},
    legend=False
)

plt.title("Customer Churn Distribution")
plt.xlabel("Customer Churn Status")
plt.ylabel("Number of Customers")
plt.tight_layout()

plt.savefig("outputs/churn_distribution.png", dpi=300)
plt.show()

# Visualize churn and retention rates
plt.figure(figsize=(7, 5))

plt.pie(
    [retained_customers, churned_customers],
    labels=["Retained", "Churned"],
    autopct="%1.1f%%",
    startangle=90,
    colors=["seagreen", "tomato"]
)

plt.title("Customer Retention vs Churn")
plt.tight_layout()

plt.savefig("outputs/retention_vs_churn.png", dpi=300)
plt.show()

# ============================================
# PART 3: CHURN BY CONTRACT TYPE
# ============================================

# Calculate churn rate for each contract type
contract_churn = df.groupby("Contract").agg(
    Total_Customers=("customerID", "count"),
    Churned_Customers=(
        "Churn",
        lambda x: (x == "Yes").sum()
    )
)

contract_churn["Churn_Rate"] = (
    contract_churn["Churned_Customers"]
    / contract_churn["Total_Customers"]
) * 100

# Display results
print("\n--- CHURN BY CONTRACT TYPE ---")
print(contract_churn.round(2))

# Visualize churn rates
plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="Contract",
    y=df["Churn"].eq("Yes").astype(int),
    hue="Contract",
    palette="viridis",
    legend=False,
    errorbar=None
)

plt.title("Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate")
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
)

plt.tight_layout()
plt.savefig("outputs/churn_by_contract.png", dpi=300)
plt.show()

# ============================================
# PART 4: CUSTOMER TENURE ANALYSIS
# ============================================

# Create customer tenure groups
df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=[
        "0-12 months",
        "13-24 months",
        "25-48 months",
        "49-72 months"
    ]
)

# Calculate churn rate and average tenure
tenure_analysis = df.groupby(
    "TenureGroup", observed=False
).agg(
    Total_Customers=("customerID", "count"),
    Churned_Customers=(
        "Churn",
        lambda x: (x == "Yes").sum()
    ),
    Average_Tenure=("tenure", "mean")
)

tenure_analysis["Churn_Rate"] = (
    tenure_analysis["Churned_Customers"]
    / tenure_analysis["Total_Customers"]
) * 100

# Display results
print("\n--- CHURN BY CUSTOMER TENURE ---")
print(tenure_analysis.round(2))

# Plot churn rate by tenure group
plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="TenureGroup",
    y=df["Churn"].eq("Yes").astype(int),
    hue="TenureGroup",
    palette="mako",
    legend=False,
    errorbar=None
)

plt.title("Churn Rate by Customer Tenure")
plt.xlabel("Customer Tenure")
plt.ylabel("Churn Rate")

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
)

plt.tight_layout()
plt.savefig("outputs/churn_by_tenure.png", dpi=300)
plt.show()

# Plot the distribution of customer tenure
plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="tenure",
    hue="Churn",
    bins=30,
    multiple="stack"
)

plt.title("Customer Tenure Distribution by Churn Status")
plt.xlabel("Tenure (Months)")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.savefig("outputs/tenure_distribution.png", dpi=300)
plt.show()

# ============================================
# PART 5: CHURN BY PAYMENT METHOD
# ============================================

# Calculate customers and churn for each payment method
payment_analysis = df.groupby("PaymentMethod").agg(
    Total_Customers=("customerID", "count"),
    Churned_Customers=(
        "Churn",
        lambda x: (x == "Yes").sum()
    )
)

# Calculate churn rate
payment_analysis["Churn_Rate"] = (
    payment_analysis["Churned_Customers"]
    / payment_analysis["Total_Customers"]
) * 100

# Display results, highest churn rate first
payment_analysis = payment_analysis.sort_values(
    "Churn_Rate", ascending=False
)

print("\n--- CHURN BY PAYMENT METHOD ---")
print(payment_analysis.round(2))

# Create a bar chart of churn rates
plt.figure(figsize=(10, 6))

sns.barplot(
    data=df,
    x="PaymentMethod",
    y=df["Churn"].eq("Yes").astype(int),
    hue="PaymentMethod",
    order=payment_analysis.index,
    palette="Set2",
    legend=False,
    errorbar=None
)

plt.title("Churn Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Churn Rate")

plt.xticks(rotation=20, ha="right")

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
)

plt.tight_layout()
plt.savefig("outputs/churn_by_payment_method.png", dpi=300)
plt.show()

# ============================================
# PART 6: CHURN BY INTERNET SERVICE
# AND TECHNICAL SUPPORT
# ============================================

# 1. Analyze churn by internet service
internet_analysis = df.groupby("InternetService").agg(
    Total_Customers=("customerID", "count"),
    Churned_Customers=("Churn", lambda x: (x == "Yes").sum())
)

internet_analysis["Churn_Rate"] = (
    internet_analysis["Churned_Customers"]
    / internet_analysis["Total_Customers"]
) * 100

print("\n--- CHURN BY INTERNET SERVICE ---")
print(internet_analysis.round(2))


# 2. Analyze churn by technical support
support_analysis = df.groupby("TechSupport").agg(
    Total_Customers=("customerID", "count"),
    Churned_Customers=("Churn", lambda x: (x == "Yes").sum())
)

support_analysis["Churn_Rate"] = (
    support_analysis["Churned_Customers"]
    / support_analysis["Total_Customers"]
) * 100

print("\n--- CHURN BY TECHNICAL SUPPORT ---")
print(support_analysis.round(2))


# 3. Visualize churn by internet service
plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="InternetService",
    y=df["Churn"].eq("Yes").astype(int),
    hue="InternetService",
    palette="Set2",
    legend=False,
    errorbar=None
)

plt.title("Churn Rate by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Churn Rate")

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
)

plt.tight_layout()
plt.savefig("outputs/churn_by_internet_service.png", dpi=300)
plt.show()


# 4. Visualize churn by technical support
plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="TechSupport",
    y=df["Churn"].eq("Yes").astype(int),
    hue="TechSupport",
    palette="Set3",
    legend=False,
    errorbar=None
)

plt.title("Churn Rate by Technical Support")
plt.xlabel("Technical Support")
plt.ylabel("Churn Rate")

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
)

plt.tight_layout()
plt.savefig("outputs/churn_by_technical_support.png", dpi=300)
plt.show()

# ============================================
# PART 7: CHURN BY MONTHLY CHARGES
# ============================================

# 1. Compare monthly charges for customers
# who stayed and customers who left

charges_analysis = df.groupby("Churn")["MonthlyCharges"].agg(
    ["count", "mean", "median"]
)

charges_analysis.columns = [
    "Total_Customers",
    "Average_Monthly_Charges",
    "Median_Monthly_Charges"
]

print("\n--- MONTHLY CHARGES BY CHURN STATUS ---")
print(charges_analysis.round(2))


# 2. Visualize monthly charges by churn status
plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Churn",
    y="MonthlyCharges",
    hue="Churn",
    palette="Set2",
    legend=False
)

plt.title("Monthly Charges: Customers Who Stayed vs Left")
plt.xlabel("Customer Churn")
plt.ylabel("Monthly Charges")

plt.tight_layout()
plt.savefig("outputs/monthly_charges_by_churn.png", dpi=300)
plt.show()

# ============================================
# PART 8: CHURN BY ONLINE SECURITY
# ============================================

# Calculate customer counts and churn rates
security_analysis = df.groupby("OnlineSecurity").agg(
    Total_Customers=("customerID", "count"),
    Churned_Customers=(
        "Churn",
        lambda x: (x == "Yes").sum()
    )
)

security_analysis["Churn_Rate"] = (
    security_analysis["Churned_Customers"]
    / security_analysis["Total_Customers"]
) * 100

print("\n--- CHURN BY ONLINE SECURITY ---")
print(security_analysis.round(2))


# Create a bar chart
plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="OnlineSecurity",
    y=df["Churn"].eq("Yes").astype(int),
    hue="OnlineSecurity",
    palette="Set2",
    legend=False,
    errorbar=None
)

plt.title("Churn Rate by Online Security")
plt.xlabel("Online Security")
plt.ylabel("Churn Rate")

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y * 100:.0f}%")
)

plt.tight_layout()
plt.savefig("outputs/churn_by_online_security.png", dpi=300)
plt.show()



