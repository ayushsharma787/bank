import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data
from utils.styling import inject_css

st.set_page_config(page_title="Loans · Universal Bank", layout="wide", page_icon="💳")
inject_css()

df = load_data()

st.markdown('<div class="section-badge">LOAN PORTFOLIO</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Loan <span>Analytics</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Deep-dive into acceptance drivers and portfolio performance</div>', unsafe_allow_html=True)

accepted = df[df["Personal Loan"] == 1]
rejected = df[df["Personal Loan"] == 0]

# ── KPIs ──────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Loans Accepted", "480", "9.60% rate")
c2.metric("Loans Rejected", "4,520", "90.40% rate", delta_color="inverse")
c3.metric("Avg Income (Accepted)", f"${accepted['Income'].mean():.0f}K", f"vs ${rejected['Income'].mean():.0f}K rejected")
c4.metric("Avg CCAvg (Accepted)", f"${accepted['CCAvg'].mean():.2f}K", f"vs ${rejected['CCAvg'].mean():.2f}K rejected")
st.markdown("---")

# ── ACCEPTANCE RATE BY INCOME ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Loan Acceptance Rate by Income Bracket**")
    bins = [0, 30, 60, 80, 100, 130, 160, 200, 300]
    labels = ["<30K","30-60K","60-80K","80-100K","100-130K","130-160K","160-200K","200K+"]
    df2 = df.copy()
    df2["Bracket"] = pd.cut(df2["Income"], bins=bins, labels=labels)
    rates = df2.groupby("Bracket", observed=True)["Personal Loan"].mean().reset_index()
    rates["Rate %"] = (rates["Personal Loan"] * 100).round(1)
    fig = px.line(rates, x="Bracket", y="Rate %", markers=True,
                  color_discrete_sequence=["#D4A853"], template="plotly_dark")
    fig.update_traces(line_width=2.5, marker_size=8)
    fig.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120", margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Acceptance Rate by Education Level**")
    edu_map = {1:"Undergrad", 2:"Graduate", 3:"Advanced"}
    df3 = df.copy()
    df3["Education Label"] = df3["Education"].map(edu_map)
    edu_rates = df3.groupby("Education Label")["Personal Loan"].agg(["sum","count"]).reset_index()
    edu_rates["Rate %"] = (edu_rates["sum"] / edu_rates["count"] * 100).round(1)
    fig2 = px.bar(edu_rates, x="Education Label", y="Rate %",
                  color="Education Label",
                  color_discrete_sequence=["#3B82F6","#D4A853","#00D4AA"],
                  text="Rate %", template="plotly_dark")
    fig2.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       showlegend=False, margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)

# ── ROW 2 ──────────────────────────────────────────────────────────────────
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("**CD Account Impact**")
    cd_rates = df.groupby("CD Account")["Personal Loan"].mean().reset_index()
    cd_rates["Label"] = cd_rates["CD Account"].map({0:"No CD Account", 1:"Has CD Account"})
    cd_rates["Rate %"] = (cd_rates["Personal Loan"] * 100).round(1)
    fig3 = px.bar(cd_rates, x="Label", y="Rate %",
                  color_discrete_sequence=["#00D4AA"], text="Rate %",
                  template="plotly_dark")
    fig3.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       showlegend=False, margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("**Family Size Impact**")
    fam_rates = df.groupby("Family")["Personal Loan"].mean().reset_index()
    fam_rates["Rate %"] = (fam_rates["Personal Loan"] * 100).round(1)
    fig4 = px.bar(fam_rates, x="Family", y="Rate %",
                  color_discrete_sequence=["#7C3AED"], text="Rate %",
                  template="plotly_dark")
    fig4.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       showlegend=False, margin=dict(t=10))
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.markdown("**CCAvg vs Acceptance Rate**")
    df4 = df.copy()
    df4["CC Bracket"] = pd.cut(df4["CCAvg"], bins=[0,1,2,3,4,5,6,7,10],
                                labels=["0-1","1-2","2-3","3-4","4-5","5-6","6-7","7+"])
    cc_rates = df4.groupby("CC Bracket", observed=True)["Personal Loan"].mean().reset_index()
    cc_rates["Rate %"] = (cc_rates["Personal Loan"] * 100).round(1)
    fig5 = px.line(cc_rates, x="CC Bracket", y="Rate %", markers=True,
                   color_discrete_sequence=["#EF4444"], template="plotly_dark")
    fig5.update_traces(line_width=2.5, marker_size=7)
    fig5.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120", margin=dict(t=10))
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ── BOXPLOT ────────────────────────────────────────────────────────────────
st.markdown("**Income Distribution: Accepted vs Rejected**")
df5 = df.copy()
df5["Loan Status"] = df5["Personal Loan"].map({1:"Accepted ✅",0:"Rejected ❌"})
fig6 = px.box(df5, x="Loan Status", y="Income", color="Loan Status",
              color_discrete_map={"Accepted ✅":"#D4A853","Rejected ❌":"#334155"},
              points="outliers", template="plotly_dark")
fig6.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                   showlegend=False, margin=dict(t=10))
st.plotly_chart(fig6, use_container_width=True)
