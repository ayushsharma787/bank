import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data, get_summary_stats
from utils.styling import inject_css

st.set_page_config(page_title="Customers · Universal Bank", layout="wide", page_icon="👥")
inject_css()

df = load_data()
stats = get_summary_stats(df)

st.markdown('<div class="section-badge">CUSTOMER INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Customer <span>Base Analysis</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Behavioral and demographic breakdown of 5,000 customers</div>', unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Online Banking", f"{stats['online_pct']}%", f"{stats['online_pct']/100*5000:.0f} customers")
c2.metric("Credit Card Holders", f"{stats['cc_holders_pct']}%", "1,470 customers")
c3.metric("Securities Account", f"{stats['securities_pct']}%", "522 customers")
c4.metric("Avg Age", f"{stats['avg_age']} yrs", "Range 23–67")
st.markdown("---")

# ── FILTERS ───────────────────────────────────────────────────────────────────
with st.expander("🔍 Filters", expanded=False):
    f1, f2, f3, f4 = st.columns(4)
    inc_range = f1.slider("Income Range ($K)", 0, 250, (0, 250))
    age_range = f2.slider("Age Range", 18, 70, (18, 70))
    edu_filter = f3.multiselect("Education", [1, 2, 3], default=[1, 2, 3],
                                format_func=lambda x: {1:"Undergrad",2:"Graduate",3:"Advanced"}[x])
    loan_filter = f4.selectbox("Loan Status", ["All", "Accepted", "Rejected"])

mask = (
    df["Income"].between(*inc_range) &
    df["Age"].between(*age_range) &
    df["Education"].isin(edu_filter)
)
if loan_filter == "Accepted":
    mask &= df["Personal Loan"] == 1
elif loan_filter == "Rejected":
    mask &= df["Personal Loan"] == 0
filtered = df[mask]
st.caption(f"Showing **{len(filtered):,}** customers")

st.markdown("---")

# ── ROW 1 ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Age Distribution by Education Level**")
    edu_map = {1:"Undergrad", 2:"Graduate", 3:"Advanced"}
    tmp = filtered.copy()
    tmp["Education Label"] = tmp["Education"].map(edu_map)
    fig = px.histogram(tmp, x="Age", color="Education Label", nbins=20, barmode="stack",
                       color_discrete_sequence=["#3B82F6","#D4A853","#00D4AA"],
                       template="plotly_dark")
    fig.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                      legend=dict(orientation="h", y=1.05), margin=dict(t=30))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Credit Card Monthly Spend Distribution**")
    fig2 = px.histogram(filtered, x="CCAvg", nbins=30,
                        color_discrete_sequence=["#7C3AED"], template="plotly_dark")
    fig2.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120", margin=dict(t=30))
    st.plotly_chart(fig2, use_container_width=True)

# ── ROW 2 ──────────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Income vs CCAvg — Bubble by Family Size**")
    sample = filtered.sample(min(800, len(filtered)), random_state=1)
    sample["Loan Status"] = sample["Personal Loan"].map({1:"Accepted", 0:"Rejected"})
    fig3 = px.scatter(sample, x="Income", y="CCAvg", size="Family",
                      color="Loan Status",
                      color_discrete_map={"Accepted":"#D4A853","Rejected":"#334155"},
                      template="plotly_dark", opacity=0.7)
    fig3.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                       legend=dict(orientation="h", y=1.05), margin=dict(t=30))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("**Mortgage Distribution (Customers with Mortgage)**")
    mdf = filtered[filtered["Mortgage"] > 0]
    fig4 = px.histogram(mdf, x="Mortgage", nbins=30,
                        color_discrete_sequence=["#00D4AA"], template="plotly_dark")
    fig4.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120", margin=dict(t=30))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── DATA TABLE ────────────────────────────────────────────────────────────────
st.markdown("**Customer Records Explorer**")
display_df = filtered.copy()
display_df["Education"] = display_df["Education"].map({1:"Undergrad",2:"Graduate",3:"Advanced"})
display_df["Personal Loan"] = display_df["Personal Loan"].map({1:"✅ Accepted", 0:"❌ Rejected"})
display_df["Online"] = display_df["Online"].map({1:"Yes",0:"No"})
display_df["CreditCard"] = display_df["CreditCard"].map({1:"Yes",0:"No"})
display_df["CD Account"] = display_df["CD Account"].map({1:"Yes",0:"No"})
display_df["Securities Account"] = display_df["Securities Account"].map({1:"Yes",0:"No"})
display_df["Income"] = display_df["Income"].apply(lambda x: f"${x}K")
st.dataframe(display_df.head(200), use_container_width=True, hide_index=True)
