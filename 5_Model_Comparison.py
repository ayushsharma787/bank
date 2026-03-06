import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data, get_feature_target
from utils.styling import inject_css
from models.train_models import train_and_evaluate

st.set_page_config(page_title="Model Comparison · Universal Bank", layout="wide", page_icon="📊")
inject_css()

df = load_data()
X, y, features = get_feature_target(df)

st.markdown('<div class="section-badge">MODEL BENCHMARKING</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Algorithm <span>Comparison</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Full performance benchmark across all 10+ ML algorithms on Universal Bank dataset</div>', unsafe_allow_html=True)

@st.cache_resource(show_spinner="Benchmarking all algorithms…")
def get_results():
    results, trained, scaler, X_test, y_test, best = train_and_evaluate(X, y)
    return results, trained, scaler, X_test, y_test, best

results, trained_models, scaler, X_test, y_test, best_model_name = get_results()

results_df = pd.DataFrame(results).T.reset_index()
results_df.columns = ["Algorithm","Accuracy","Precision","Recall","F1","AUC-ROC","Confusion Matrix"]
results_df = results_df.sort_values("AUC-ROC", ascending=False).reset_index(drop=True)
results_df["Rank"] = range(1, len(results_df) + 1)

# ── TOP KPIs ──────────────────────────────────────────────────────────────────
best_row = results_df.iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏆 Best Model",    best_row["Algorithm"], f"{best_row['Accuracy']}% accuracy")
c2.metric("Best AUC-ROC",    str(best_row["AUC-ROC"]), best_row["Algorithm"])
c3.metric("Best F1 Score",   f"{results_df['F1'].max()}%", results_df.loc[results_df['F1'].idxmax(),'Algorithm'])
c4.metric("Models Evaluated", str(len(results_df)), "With SMOTE balancing")
st.markdown("---")

# ── CHARTS ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Accuracy Ranking**")
    fig = px.bar(results_df.sort_values("Accuracy"), x="Accuracy", y="Algorithm",
                 orientation="h", color="Accuracy",
                 color_continuous_scale=["#334155","#D4A853"],
                 text="Accuracy", template="plotly_dark")
    fig.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                      coloraxis_showscale=False, margin=dict(t=10),
                      yaxis=dict(autorange=True))
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Multi-Metric Radar**")
    radar_metrics = ["Accuracy","Precision","Recall","F1"]
    # Show top 5 by AUC
    top5 = results_df.head(5)
    fig2 = go.Figure()
    colors = ["#D4A853","#00D4AA","#3B82F6","#7C3AED","#EF4444"]
    for i, row in top5.iterrows():
        vals = [row[m] for m in radar_metrics]
        vals += [vals[0]]
        fig2.add_trace(go.Scatterpolar(
            r=vals,
            theta=radar_metrics + [radar_metrics[0]],
            name=row["Algorithm"],
            line_color=colors[i % len(colors)],
            fill="toself",
            fillcolor=colors[i % len(colors)] + "18",
        ))
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[85, 100]), bgcolor="#0C1120"),
        showlegend=True, template="plotly_dark",
        plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
        legend=dict(orientation="h", y=-0.15),
        margin=dict(t=20)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── AUC BAR ─────────────────────────────────────────────────────────────────
st.markdown("**AUC-ROC Comparison**")
auc_df = results_df[results_df["AUC-ROC"].notna()].copy()
fig3 = px.bar(auc_df.sort_values("AUC-ROC"), x="AUC-ROC", y="Algorithm",
              orientation="h", color="AUC-ROC",
              color_continuous_scale=["#334155","#00D4AA"],
              text="AUC-ROC", template="plotly_dark",
              range_x=[0.85, 1.0])
fig3.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                   coloraxis_showscale=False, margin=dict(t=10))
fig3.update_traces(texttemplate="%{text:.4f}", textposition="outside")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── FULL TABLE ────────────────────────────────────────────────────────────────
st.markdown("**Full Performance Matrix**")
display_df = results_df[["Rank","Algorithm","Accuracy","Precision","Recall","F1","AUC-ROC"]].copy()
display_df["Accuracy"]  = display_df["Accuracy"].apply(lambda x: f"{x}%")
display_df["Precision"] = display_df["Precision"].apply(lambda x: f"{x}%")
display_df["Recall"]    = display_df["Recall"].apply(lambda x: f"{x}%")
display_df["F1"]        = display_df["F1"].apply(lambda x: f"{x}%")
display_df.loc[0, "Rank"] = "🥇"
if len(display_df) > 1: display_df.loc[1, "Rank"] = "🥈"
if len(display_df) > 2: display_df.loc[2, "Rank"] = "🥉"
st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── CONFUSION MATRIX ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("**Confusion Matrix**")
cm_algo = st.selectbox("Select Algorithm", results_df["Algorithm"].tolist())
cm_row = results_df[results_df["Algorithm"] == cm_algo].iloc[0]
cm = cm_row["Confusion Matrix"]
if cm:
    cm_arr = np.array(cm)
    fig_cm = px.imshow(cm_arr, text_auto=True,
                       x=["Predicted Rejected","Predicted Accepted"],
                       y=["Actual Rejected","Actual Accepted"],
                       color_continuous_scale=["#0C1120","#D4A853"],
                       template="plotly_dark")
    fig_cm.update_layout(plot_bgcolor="#0C1120", paper_bgcolor="#0C1120",
                         margin=dict(t=10))
    st.plotly_chart(fig_cm, use_container_width=True)
