# 🔬 Employee Attrition Intelligence Suite

A comprehensive, interactive Streamlit dashboard that performs **Descriptive, Diagnostic, Predictive, and Prescriptive analysis** on employee attrition data — answering the central question: **Why do employees stay or leave?**

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?logo=plotly)

---

## 🎯 Objective

To understand **why employees stay or leave** the organisation, tracked via the `Attrition` column, through four layers of analytics:

| Analysis Type | Question Answered | Techniques Used |
|---|---|---|
| **Descriptive** | What happened? | Distributions, KPIs, Sunburst drill-downs, demographic breakdowns |
| **Diagnostic** | Why did it happen? | Correlation analysis, Chi-Square tests, Cramér's V, Risk factor combinations |
| **Predictive** | What will happen? | Logistic Regression, Random Forest, Gradient Boosting, ROC curves |
| **Prescriptive** | What should we do? | Risk scoring simulator, strategic recommendations, impact-cost matrix |

---

## 🚀 Quick Start

### Local Setup
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/employee-attrition-dashboard.git
cd employee-attrition-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deploy on Streamlit Cloud
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Deploy!

---

## 📊 Dashboard Features

- **Interactive Sidebar Filters** — slice data by Department, Gender, Job Role, OverTime, Age, and Income
- **6 KPI Cards** — real-time summary metrics
- **Sunburst & Treemap Drill-Downs** — click to explore hierarchical attrition patterns
- **Radar Charts** — multi-dimensional satisfaction comparison
- **Statistical Tests** — Chi-Square with Cramér's V effect sizes
- **3 ML Models** — with cross-validated AUC, ROC curves, and feature importance
- **Risk Score Simulator** — interactive gauge to estimate individual attrition risk
- **Impact vs Cost Matrix** — prioritise interventions by effectiveness and cost

---

## 📁 Project Structure

```
employee-attrition-dashboard/
├── app.py                  # Main Streamlit application
├── EA.csv                  # Employee Attrition dataset (1,470 × 35)
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── .gitignore
└── README.md
```

---

## 📦 Dataset

- **1,470 employees** × **35 features**
- Target variable: `Attrition` (Yes/No)
- Features include demographics, compensation, satisfaction scores, tenure, and work conditions
- No missing values

---

## 🛠️ Tech Stack

- **Streamlit** — Dashboard framework
- **Plotly** — Interactive visualisations
- **scikit-learn** — Predictive models
- **SciPy / statsmodels** — Statistical tests
- **Pandas / NumPy** — Data processing

---

## 📄 License

MIT License — free to use, modify, and distribute.
