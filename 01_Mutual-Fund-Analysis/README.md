# 💰 Mutual Fund Analysis — Finding High Return & Low Risk Funds

## 📌 Project Overview

This project focuses on analyzing mutual fund data to identify and compare funds based on their returns, expense ratio, fund age, risk level and other important financial parameters.

The project follows a complete data analytics workflow starting from data understanding and cleaning to exploratory analysis, fund scoring, ranking, Excel reporting and Power BI dashboard creation.

---

## 🎯 Business Objective

The objective of this project is to analyze a large number of mutual funds and generate meaningful insights that can help users compare funds based on performance, cost and other important characteristics.

---

## 📊 Dataset

The dataset contains:

- **814 mutual fund records**
- **20 columns**

Important attributes include:

- Scheme Name
- AMC Name
- Fund Size / AUM
- Expense Ratio
- Fund Age
- 1-Year Return
- 3-Year Return
- 5-Year Return
- Rating
- Risk Level
- Alpha
- Beta
- Sharpe Ratio
- Sortino Ratio
- Standard Deviation

---

## 🔄 Project Workflow

### 1. Business Understanding

Defined the business problem, business objective and financial goal for mutual fund analysis.

### 2. Dataset Understanding

Loaded and examined the dataset, its structure, columns, data types and important financial parameters.

### 3. Data Cleaning

Performed:

- Missing value analysis
- Data type checking
- Conversion of financial metrics from text to numeric
- Duplicate row checking
- Duplicate scheme name investigation

The financial parameters **Alpha, Beta, Sharpe, Sortino and Standard Deviation** were converted into numeric format for analysis.

### 4. Exploratory Data Analysis

Performed EDA to identify patterns and business insights using:

- Bar Chart
- Pie Chart
- Histogram
- Box Plot
- Scatter Plot

The analysis included category-wise returns, AMC-wise analysis, risk distribution, expense ratio and return analysis.

### 5. Data Normalization

Used **MinMaxScaler** to normalize selected variables into a common range between 0 and 1.

The following parameters were normalized:

- 3-Year Return
- Expense Ratio
- Fund Age
- 1-Year Return

An **Expense Score** was created because a lower expense ratio is preferable.

### 6. Fund Score Calculation

A weighted Fund Score was created using four important parameters:

| Parameter | Weight |
|---|---:|
| 3-Year Return | 40% |
| Expense Ratio | 30% |
| Fund Age | 20% |
| 1-Year Return | 10% |

The weighted scores were combined to calculate the final Fund Score for each fund.

### 7. Fund Ranking

All funds were sorted from the highest Fund Score to the lowest to create a complete ranking.

### 8. Top 30 Funds

The **Top 30 funds** with the highest Fund Scores were extracted and exported to Excel for further analysis and reporting.

---

## 🔍 Key Insights

- The dataset contains **814 mutual funds**.
- **ICICI Prudential Mutual Fund** had the highest AUM in the analyzed dataset.
- **Equity** had the highest average 3-Year Return at approximately **29.74%**.
- The overall average Expense Ratio was approximately **0.71%**.
- **Quant Small Cap Fund** had the highest 3-Year Return at **71.4%**.
- **Bank of India Credit Risk Fund** had the highest 1-Year Return at **130.8%**.
- The risk distribution was analyzed across six risk levels.

> These insights are based on the dataset used for this project and should not be treated as investment advice.

---

## 📈 Power BI Dashboard

An interactive Power BI dashboard was created with the following pages:

### Executive Summary
- Total Funds
- Total AUM
- Average 3-Year Return
- Average Expense Ratio

### Return Analysis
- Category-wise Returns
- AMC-wise Returns
- Top Performing Funds

### Risk Analysis
- Risk Level Distribution
- Risk vs Return Analysis

### Top 30 Funds
- Detailed Top 30 Fund Table
- Fund Score Comparison

### Mutual Fund Filters
Interactive filters for:

- AMC
- Category
- Risk Level
- Rating

---

## 🛠️ Tools & Technologies

- **Python**
- **Google Colab**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Matplotlib**
- **Seaborn**
- **Microsoft Excel**
- **Power BI**

---

## 📂 Project Files

- 📓 [Google Colab Notebook](./Mutual_Fund_Analysis_Project.ipynb)
- 📊 [Top 30 Mutual Funds Excel](./Top_30_Mutual_Funds.xlsx)
- 📈 [Power BI Dashboard (.pbix)](./Mutual_Fund_Analysis_Dashboard.pbix)
- 📄 [Power BI Dashboard PDF](./Mutual_Fund_Analysis_Dashboard.pdf)
- 📝 [Project Report](./Mutual_Fund_Analysis_Report.docx)

---

## 📌 Project Outcome

This project demonstrates a complete data analytics workflow:

**Raw Data → Data Cleaning → EDA → Normalization → Fund Scoring → Ranking → Top 30 Selection → Excel Reporting → Power BI Dashboard**

The project helped transform raw mutual fund data into structured analysis and interactive business insights.

---

## 👩‍💻 Author

**Yashasvi Agarwal**

B.Tech Computer Science Engineering

- [LinkedIn](https://www.linkedin.com/in/yashasvi-agarwal-3454a4324/)
- [GitHub](https://github.com/yashasviagarwal01)
