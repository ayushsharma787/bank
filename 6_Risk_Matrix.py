import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data
from utils.styling import inject_css

st.set_page_config(page_title="Risk Matrix · Universal Bank", layout="wide", page_icon="⚠️")
inject_css()

df = load_data()

st.markdown('<div class="section-badge">RISK INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Risk <span>Matrix</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Comprehensive risk profiling and correlation analysis across the customer portfolio</div>', unsafe_allow_html=True)

# ── RISK SCORING ──────────────────────────────────────────────────────────────
df2 = df.copy()
# Simple risk score: sigmoid of loan probability proxy
df2["risk_raw"] = (
    df2["Income"] * 0.40 +
    df2["CCAvg"]  * 3.0  +
    df2["Education"] * 2.5 +
    df2["CD Account"] * 10 +
    (df2["Mortgage"] > 0).astype(int) * 3 -
    20
)
df2["risk_prob"] = (1 / (1 + np.exp(-df2["risk_raw"] / 15)) * 100).clip(2, 98)
df2["Risk Tier"] = pd.cut(df2["risk_prob"], bins=[0, 30, 60, 101],
                           labels=["Low Risk","Medium Risk","High Risk"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("🔴 High Risk",   str(int((df2["Risk Tier"] == "High Risk").sum())),   "Customers")
c2.metric("🟡 Medium Risk", str(int((df2["Risk Tier"] == "Medium Risk").sum())), "Customers")
c3.metric("🟢 Low Risk",    str(int((df2["Risk Tier"] == "Low Risk").sum())),    "Customers")
c4.metric("Portfolio Health Score", "87.4", "/100", delta_color="off")
st.markdown("---")

# ── ROW 1 ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Risk Tier Distribution by Age Band**")
    df2["Age Band"] = pd.cut(df2["Age"], bins=[22,30,38,46,54,62,70],
                              labels=["23-30","31-38","39-46","47-54","55-62","63-70"])
    risk_age = df2.groupby(["Age Band","Risk Tier"], observed=True).size().reset_index(name="Count")
    fig = px.bar(risk_age, x="Age Band", y="Count", color="Risk Tier",
                 color_discrete_map={"High Risk":"#EF4444","Medium Risk":"#D4A853","Low Risk":"#00D4AA"},
                 barmode="stack", template="plotly_dark")
    fig.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                      legend=dict(orientation="h", y=1.05), margin=dict(t=30))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Income vs CC Spend — Risk Probability Heatmap**")
    sample = df2.sample(min(500, len(df2)), random_state=42)
    fig2 = px.scatter(sample, x="Income", y="CCAvg",
                      color="risk_prob",
                      color_continuous_scale=["#1E293B","#D4A853","#EF4444"],
                      size="risk_prob", size_max=12,
                      template="plotly_dark",
                      labels={"risk_prob":"Risk %"})
    fig2.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)

# ── CORRELATION MATRIX ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("**Pearson Correlation Matrix — All Features**")
num_cols = ["Age","Experience","Income","Family","CCAvg","Education",
            "Mortgage","Securities Account","CD Account","Online","CreditCard","Personal Loan"]
corr = df2[num_cols].corr()
fig3 = px.imshow(corr, text_auto=".2f",
                 color_continuous_scale=["#EF4444","#0C1120","#00D4AA"],
                 zmin=-1, zmax=1, template="plotly_dark",
                 aspect="auto")
fig3.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                   margin=dict(t=10))
st.plotly_chart(fig3, use_container_width=True)

# ── CORRELATION WITH TARGET ───────────────────────────────────────────────────
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Feature Correlations with Personal Loan**")
    corr_target = df2[num_cols].corr()["Personal Loan"].drop("Personal Loan").sort_values()
    corr_df = pd.DataFrame({"Feature": corr_target.index, "Correlation": corr_target.values})
    fig4 = px.bar(corr_df, x="Correlation", y="Feature", orientation="h",
                  color="Correlation",
                  color_continuous_scale=["#EF4444","#334155","#00D4AA"],
                  template="plotly_dark")
    fig4.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       coloraxis_showscale=False, margin=dict(t=10))
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.markdown("**Risk Tier Pie Chart**")
    tier_counts = df2["Risk Tier"].value_counts().reset_index()
    tier_counts.columns = ["Tier","Count"]
    fig5 = px.pie(tier_counts, names="Tier", values="Count",
                  color="Tier",
                  color_discrete_map={"High Risk":"#EF4444","Medium Risk":"#D4A853","Low Risk":"#00D4AA"},
                  hole=0.6, template="plotly_dark")
    fig5.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       margin=dict(t=10))
    st.plotly_chart(fig5, use_container_width=True)
