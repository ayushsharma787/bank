# 🏦 Universal Bank Intelligence Platform

> Enterprise-grade ML-powered banking analytics dashboard built with Streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Features

| Section | Description |
|---|---|
| 📊 **Overview** | Executive KPIs, income distribution, loan split, scatter analysis, live alerts |
| 👥 **Customer Analytics** | Demographics, behavioral filters, interactive data explorer |
| 💳 **Loan Analytics** | Acceptance rate by income, education, family size, CD account |
| 🤖 **AI Predictor** | Real-time loan prediction with 11 ML algorithms + feature importance |
| 📈 **Model Comparison** | Full benchmark: accuracy, precision, recall, F1, AUC-ROC, confusion matrix |
| ⚠️ **Risk Matrix** | Risk tier scoring, Pearson correlation heatmap, portfolio health |

---

## 🧠 ML Algorithms Included

| Algorithm | Type | Best For |
|---|---|---|
| **Gradient Boosting** | Ensemble | Imbalanced data (⭐ Default) |
| **XGBoost** | Ensemble | AUC optimization |
| **LightGBM** | Ensemble | Speed + accuracy |
| **Random Forest** | Ensemble | Stability & interpretability |
| **Extra Trees** | Ensemble | Low-variance predictions |
| **AdaBoost** | Ensemble | Boosting weak learners |
| **Decision Tree** | Tree | Fast inference, explainable |
| **Logistic Regression** | Linear | Baseline comparison |
| **KNN** | Instance-based | Non-linear boundaries |
| **SVM** | Kernel | High-dimensional data |
| **Neural Network (MLP)** | Deep Learning | Complex patterns |

> All models trained with **SMOTE oversampling** to handle the 9.6% class imbalance.

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/universalbank-dashboard.git
cd universalbank-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select:
   - **Repository**: `YOUR_USERNAME/universalbank-dashboard`
   - **Branch**: `main`
   - **Main file**: `app.py`
5. Click **Deploy** ✅

> ⚠️ Streamlit Cloud has a 1GB memory limit. All 11 models train in ~30 seconds and are cached via `@st.cache_resource`.

---

## 📁 Project Structure

```
universalbank_dashboard/
├── app.py                          # 🏠 Main entry point
├── requirements.txt                # 📦 Dependencies
├── README.md
├── .streamlit/
│   └── config.toml                 # 🎨 Dark gold theme
├── data/
│   └── UniversalBank.csv           # 📊 5,000 customer records
├── models/
│   ├── __init__.py
│   └── train_models.py             # 🤖 All ML algorithms
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # 📥 Data loading & stats
│   └── styling.py                  # 🎨 Premium CSS
└── pages/
    ├── 1_Overview.py               # 📊 Executive summary
    ├── 2_Customer_Analytics.py     # 👥 Customer deep-dive
    ├── 3_Loan_Analytics.py         # 💳 Loan portfolio
    ├── 4_AI_Predictor.py           # 🤖 Real-time predictor
    ├── 5_Model_Comparison.py       # 📈 Algorithm benchmark
    └── 6_Risk_Matrix.py            # ⚠️ Risk intelligence
```

---

## 📊 Dataset

**Universal Bank Dataset** — 5,000 customers with 14 features:

| Feature | Description |
|---|---|
| Age | Customer age (23–67) |
| Experience | Years of work experience |
| Income | Annual income in $K |
| Family | Family size (1–4) |
| CCAvg | Monthly credit card spend ($K) |
| Education | 1=Undergrad, 2=Graduate, 3=Advanced |
| Mortgage | Mortgage value ($K) |
| Personal Loan | **Target** — 1=Accepted, 0=Rejected |
| Securities Account | Has securities account (0/1) |
| CD Account | Has CD account (0/1) |
| Online | Uses online banking (0/1) |
| CreditCard | Has bank credit card (0/1) |

**Class imbalance**: 9.6% accepted (480) vs 90.4% rejected (4,520) → handled via SMOTE.

---

## 🛠 Tech Stack

- **Frontend**: Streamlit 1.32+
- **ML**: scikit-learn, XGBoost, LightGBM, imbalanced-learn
- **Visualization**: Plotly 5.x
- **Data**: Pandas, NumPy
- **Styling**: Custom CSS with Google Fonts (Syne + DM Mono)

---

## 📄 License

MIT License — free to use and modify.
