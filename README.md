# FUTURE_DS_02: Customer Retention & Churn Analysis

**Future Interns – Data Science & Analytics Internship Program**

## 👩‍💻 Project Information

- **Task:** Task 2 – Customer Retention & Churn Analysis
- **Domain:** Data Science & Analytics
- **Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit
- **Dataset:** Telco Customer Churn Dataset

## 📌 Project Overview

Customer retention is important for businesses because keeping existing customers helps build long-term relationships and reduce customer loss.

This project analyzes customer churn using a telecommunications customer dataset. The goal is to identify patterns in customer behavior, understand the factors associated with churn, and provide insights that can help businesses improve customer retention.

The project includes data cleaning, exploratory data analysis (EDA), visualization, and an interactive dashboard built using Streamlit.

## 📊 Dashboard Preview

The interactive dashboard provides an overview of customer churn through key performance indicators, filters, and visualizations.

**Dashboard features include:**
- Total customers and churn rate
- Customer retention rate
- Churn analysis by contract type
- Churn patterns by internet service and payment method
- Customer tenure analysis
- Comparison of monthly charges between churned and retained customers
- Interactive filters for exploring the dataset

*Add a screenshot of your dashboard here after uploading it to the repository.*

## 📁 Repository Structure

```text
FUTURE_DS_02/
│
├── data/
│   └── churn_data.csv
│
├── outputs/
│   └── cleaned_telco_churn.csv
│
├── task2.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## 🔍 Key Findings

The analysis of 7,043 customer records produced the following findings:

- **Overall churn rate:** Approximately 26.54% of customers left the service.
- **Customer retention:** Approximately 73.46% of customers remained.
- **Contract type:** Month-to-month customers had the highest churn rate at approximately 42.71%, compared with 11.27% for one-year contracts and 2.83% for two-year contracts.
- **Customer tenure:** Customers with shorter tenure showed higher churn rates than long-term customers.
- **Payment method:** Customers using electronic checks had a churn rate of approximately 45.29%.
- **Internet service:** Fiber-optic customers had a churn rate of approximately 41.89%.
- **Additional services:** Customers without Online Security or Tech Support had higher churn rates than customers with these services.
- **Monthly charges:** Customers who churned had higher average monthly charges than customers who stayed.

These findings highlight customer groups that may benefit from targeted retention strategies.

## 💡 Business Recommendations

Based on the analysis, businesses could consider the following actions:

1. **Encourage longer contracts:** Offer suitable incentives to month-to-month customers to encourage longer-term subscriptions.
2. **Improve early customer engagement:** Provide additional support during the first year to help new customers understand and use the service.
3. **Review pricing and value:** Examine whether customers with higher monthly charges are receiving sufficient value for their subscriptions.
4. **Promote additional services:** Explain the benefits of Online Security and Tech Support to customers who do not currently use them.
5. **Investigate payment-related churn:** Review the customer experience associated with electronic-check payments.
6. **Monitor churn regularly:** Use dashboards and customer data to identify changes in churn patterns over time.

These recommendations are based on observed associations in the dataset and do not necessarily establish the causes of customer churn.

## 🛠️ Tools and Technologies

- **Python:** Main programming language
- **Pandas:** Data cleaning and manipulation
- **NumPy:** Numerical operations
- **Matplotlib and Seaborn:** Exploratory data visualization
- **Plotly:** Interactive charts
- **Streamlit:** Interactive dashboard development
- **VS Code:** Development environment

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/tasneem-19/FUTURE_DS_02.git
cd FUTURE_DS_02
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

### 3. Run the data analysis script

```bash
python task2.py
```

### 4. Launch the interactive dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser.

**Note:** Make sure the dataset is available in the expected `data/` directory and that the file paths in the scripts match the repository structure.

## 📈 Project Outcome

This project demonstrates practical skills in data cleaning, exploratory data analysis, customer churn analysis, data visualization, and interactive dashboard development.

It shows how data analytics can help businesses understand customer behavior, identify customer groups with higher churn rates, and develop data-informed retention strategies.

## 👩‍🎓 Author

**Khaisar Tasneem Shaik**

Data Science & Analytics Intern  
Future Interns

## 📌 Internship Task

This project was completed as part of **Task 2 – Customer Retention & Churn Analysis** in the Future Interns Data Science & Analytics Internship Program.

---
