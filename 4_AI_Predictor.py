import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data, get_feature_target
from utils.styling import inject_css
from models.train_models import (
    train_and_evaluate, load_trained_models, load_scaler,
    predict_single, get_feature_importance
)

st.set_page_config(page_title="AI Predictor · Universal Bank", layout="wide", page_icon="🤖")
inject_css()

df = load_data()
X, y, features = get_feature_target(df)

st.markdown('<div class="section-badge">AI-POWERED PREDICTION</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Loan Approval <span>Predictor</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Real-time ML prediction using 10+ algorithms trained on Universal Bank data</div>', unsafe_allow_html=True)

# ── TRAIN / LOAD ───────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Training models on Universal Bank data…")
def get_trained():
    results, trained, scaler, X_test, y_test, best = train_and_evaluate(X, y)
    return results, trained, scaler, X_test, y_test, best

results, trained_models, scaler, X_test, y_test, best_model_name = get_trained()

# ── ALGO SELECTOR ─────────────────────────────────────────────────────────────
algo_names = list(trained_models.keys())
selected_algo = st.selectbox("🧠 Select Algorithm", algo_names,
                              index=algo_names.index(best_model_name) if best_model_name in algo_names else 0)
model = trained_models[selected_algo]
metrics = results[selected_algo]

# ── MODEL METRICS STRIP ──────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Accuracy",  f"{metrics['accuracy']}%")
m2.metric("Precision", f"{metrics['precision']}%")
m3.metric("Recall",    f"{metrics['recall']}%")
m4.metric("F1 Score",  f"{metrics['f1']}%")
m5.metric("AUC-ROC",   str(metrics['auc_roc']))
st.markdown("---")

# ── INPUT FORM + RESULT ────────────────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown("**Customer Profile Input**")
    c1, c2 = st.columns(2)
    age      = c1.slider("Age", 18, 70, 35)
    exp      = c2.slider("Work Experience (yrs)", 0, 50, 10)
    income   = c1.slider("Annual Income ($K)", 8, 224, 75)
    cc_avg   = c2.slider("CC Monthly Spend ($K)", 0.0, 10.0, 2.0, step=0.1)
    family   = c1.selectbox("Family Size", [1, 2, 3, 4], index=1)
    edu      = c2.selectbox("Education", [1, 2, 3],
                             format_func=lambda x: {1:"Undergrad",2:"Graduate",3:"Advanced"}[x])
    mortgage = c1.slider("Mortgage ($K)", 0, 635, 0, step=5)
    st.markdown("**Banking Products**")
    bc1, bc2, bc3, bc4 = st.columns(4)
    sec_acct  = bc1.selectbox("Securities", ["No","Yes"], index=0)
    cd_acct   = bc2.selectbox("CD Account", ["No","Yes"], index=0)
    online    = bc3.selectbox("Online", ["Yes","No"], index=0)
    credit_cd = bc4.selectbox("Credit Card", ["No","Yes"], index=0)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("⚡ RUN PREDICTION", use_container_width=True)

with right:
    st.markdown("**Prediction Result**")

    input_data = {
        "Age": age, "Experience": exp, "Income": income,
        "Family": family, "CCAvg": cc_avg, "Education": edu,
        "Mortgage": mortgage,
        "Securities Account": 1 if sec_acct == "Yes" else 0,
        "CD Account": 1 if cd_acct == "Yes" else 0,
        "Online": 1 if online == "Yes" else 0,
        "CreditCard": 1 if credit_cd == "Yes" else 0,
    }

    pred_result = predict_single(model, scaler, input_data)
    prob = pred_result["probability"] or 50.0
    approved = pred_result["prediction"] == 1

    verdict_class = "approved" if approved else "declined"
    verdict_text  = "✅ APPROVED" if approved else "❌ DECLINED"
    bar_color     = "#22C55E" if approved else "#64748B"

    st.markdown(f"""
    <div class="result-box-{verdict_class}">
        <div class="result-label">PREDICTION OUTCOME</div>
        <div class="result-verdict-{verdict_class}">{verdict_text}</div>
        <div class="result-prob">{prob:.1f}<span style="font-size:24px;color:#64748B">%</span></div>
        <div class="result-label" style="margin-top:4px">Approval Probability</div>
    </div>
    """, unsafe_allow_html=True)

    # Prob bar
    fig_bar = go.Figure(go.Bar(
        x=[prob], y=[""], orientation="h",
        marker_color=bar_color, width=0.4,
    ))
    fig_bar.update_layout(
        xaxis=dict(range=[0, 100], showgrid=False),
        yaxis=dict(showticklabels=False),
        plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
        margin=dict(t=10, b=10, l=0, r=0), height=60
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Risk & confidence labels
    conf_label = "HIGH" if (prob > 80 or prob < 20) else "MEDIUM" if (prob > 65 or prob < 35) else "LOW"
    risk_label = "HIGH" if prob > 75 else "MEDIUM" if prob > 45 else "LOW"
    r1, r2, r3 = st.columns(3)
    r1.metric("Confidence", conf_label)
    r2.metric("Risk Level",  risk_label)
    r3.metric("Algorithm",  selected_algo.split()[0])

    st.markdown("---")

    # Feature importance
    st.markdown("**Feature Importance for This Model**")
    feat_imp = get_feature_importance(model, features)
    if feat_imp:
        fi_df = pd.DataFrame(feat_imp, columns=["Feature","Importance %"])
        fig_fi = px.bar(fi_df.head(8), x="Importance %", y="Feature",
                        orientation="h", color="Importance %",
                        color_continuous_scale=["#334155","#D4A853"],
                        template="plotly_dark")
        fig_fi.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                             showlegend=False, coloraxis_showscale=False,
                             margin=dict(t=10, b=0), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_fi, use_container_width=True)
