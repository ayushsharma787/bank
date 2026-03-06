import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data, get_summary_stats
from utils.styling import inject_css

st.set_page_config(page_title="Overview · Universal Bank", layout="wide", page_icon="🏦")
inject_css()

df = load_data()
stats = get_summary_stats(df)

# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-badge">EXECUTIVE SUMMARY</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Portfolio <span>Overview</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">5,000 customer records · Universal Bank Dataset · Real-time insights</div>', unsafe_allow_html=True)

# ── KPI ROW ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Customers", f"{stats['total_customers']:,}", "Active Portfolio")
c2.metric("Loan Acceptance Rate", f"{stats['acceptance_rate']}%", f"{stats['loan_accepted']} approved")
c3.metric("Avg. Annual Income", f"${stats['avg_income']}K", f"Range $8K–$224K")
c4.metric("Avg. CC Monthly Spend", f"${stats['avg_cc']}K", "Monthly average")

st.markdown("---")

# ── ROW 1: Income dist + Donut ────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("**Income Distribution by Loan Status**")
    bins = [0, 30, 60, 80, 100, 130, 160, 200, 300]
    labels = ["<30K","30-60K","60-80K","80-100K","100-130K","130-160K","160-200K","200K+"]
    df["Income Bracket"] = pd.cut(df["Income"], bins=bins, labels=labels)
    grp = df.groupby(["Income Bracket", "Personal Loan"], observed=True).size().reset_index(name="Count")
    grp["Status"] = grp["Personal Loan"].map({1: "Accepted", 0: "Rejected"})
    fig = px.bar(grp, x="Income Bracket", y="Count", color="Status",
                 color_discrete_map={"Accepted": "#D4A853", "Rejected": "#334155"},
                 barmode="group", template="plotly_dark")
    fig.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                      legend=dict(orientation="h", y=1.05), margin=dict(t=30, b=0))
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Personal Loan Split**")
    fig2 = go.Figure(go.Pie(
        labels=["Accepted (9.6%)", "Rejected (90.4%)"],
        values=[stats['loan_accepted'], stats['loan_rejected']],
        hole=0.72,
        marker_colors=["#D4A853", "#1E293B"],
        textinfo="label+percent",
    ))
    fig2.update_layout(
        showlegend=False, template="plotly_dark",
        plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
        margin=dict(t=10, b=10, l=0, r=0),
        annotations=[dict(text=f"<b>{stats['loan_accepted']}</b><br>loans", x=0.5, y=0.5,
                          font_size=18, showarrow=False, font_color="#D4A853")]
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── ROW 2: Education + Family + Digital ──────────────────────────────────────
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("**Customer Education Level**")
    edu_map = {1: "Undergrad", 2: "Graduate", 3: "Advanced"}
    edu_df = df["Education"].map(edu_map).value_counts().reset_index()
    edu_df.columns = ["Education", "Count"]
    fig3 = px.bar(edu_df, x="Count", y="Education", orientation="h",
                  color="Education",
                  color_discrete_sequence=["#3B82F6","#D4A853","#00D4AA"],
                  template="plotly_dark")
    fig3.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       showlegend=False, margin=dict(t=10, b=0))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("**Family Size Distribution**")
    fam_df = df["Family"].value_counts().sort_index().reset_index()
    fam_df.columns = ["Family Size", "Count"]
    fig4 = px.bar(fam_df, x="Family Size", y="Count",
                  color_discrete_sequence=["#7C3AED"],
                  template="plotly_dark")
    fig4.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       margin=dict(t=10, b=0))
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.markdown("**Digital Banking Adoption**")
    radar_cats = ["Online Banking", "Credit Card", "Securities Acct", "CD Account", "Mortgage"]
    radar_vals = [stats['online_pct'], stats['cc_holders_pct'],
                  stats['securities_pct'], stats['cd_pct'],
                  round(df[df["Mortgage"] > 0].shape[0] / len(df) * 100, 1)]
    fig5 = go.Figure(go.Scatterpolar(
        r=radar_vals + [radar_vals[0]],
        theta=radar_cats + [radar_cats[0]],
        fill="toself",
        fillcolor="rgba(212,168,83,0.15)",
        line_color="#D4A853",
        marker=dict(size=5, color="#D4A853"),
    ))
    fig5.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100]),
                   bgcolor="#0C1120"),
        showlegend=False, template="plotly_dark",
        plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ── ROW 3: Scatter + Alerts ───────────────────────────────────────────────────
col6, col7 = st.columns([2, 1])

with col6:
    st.markdown("**Age vs Income — Loan Acceptance**")
    scatter_sample = df.sample(min(1000, len(df)), random_state=42).copy()
    scatter_sample["Status"] = scatter_sample["Personal Loan"].map({1: "Accepted", 0: "Rejected"})
    fig6 = px.scatter(scatter_sample, x="Income", y="Age", color="Status",
                      color_discrete_map={"Accepted": "#D4A853", "Rejected": "#334155"},
                      opacity=0.7, template="plotly_dark",
                      hover_data=["Education", "CCAvg"])
    fig6.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       legend=dict(orientation="h", y=1.05), margin=dict(t=30))
    st.plotly_chart(fig6, use_container_width=True)

with col7:
    st.markdown("**System Alerts**")
    alerts = [
        ("🔴", "#EF4444", "High-Risk Cluster", "47 customers with Income <30K and Mortgage >200K flagged for manual review.", "2 min ago"),
        ("🟡", "#D4A853", "Model Drift Warning", "Last 500 records show 0.3% AUC drop. Retraining recommended.", "18 min ago"),
        ("🟢", "#22C55E", "Opportunity", "312 low-risk customers with Income >120K haven't been offered a personal loan.", "1 hr ago"),
        ("🔵", "#3B82F6", "Portfolio Health", "Overall risk score improved by 2.1 points this quarter.", "3 hrs ago"),
    ]
    for icon, color, title, desc, time in alerts:
        st.markdown(f"""
        <div class="info-card">
            <strong style="color:{color}">{icon} {title}</strong><br>
            {desc}<br>
            <span style="font-size:10px;color:#475569">{time}</span>
        </div>
        """, unsafe_allow_html=True)
