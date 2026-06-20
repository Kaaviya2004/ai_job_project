import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Market Analysis · AI Career Intel",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/global_ai_jobs.csv")

df = load_data()

# ── Shared CSS ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

[data-testid="stSidebarNav"] { display: none !important; }
*, *::before, *::after { box-sizing: border-box; }

.stApp { background: #040d1a; font-family: 'Inter', sans-serif; color: #e2e8f0; }

[data-testid="stSidebar"] { background: #060f1f !important; border-right: 1px solid #0f2040; }
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

.sidebar-brand { padding: 20px 16px 24px; border-bottom: 1px solid #0f2040; margin-bottom: 8px; }
.sidebar-brand h2 { font-size: 15px; font-weight: 700; color: #e2e8f0; }
.sidebar-brand p { font-size: 11px; color: #3b82f6; font-family: 'JetBrains Mono', monospace; margin-top: 4px; }

.page-header {
    padding: 36px 44px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0c1f45 0%, #0a1628 60%, #060f1f 100%);
    border: 1px solid #1e3a8a;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(37,99,235,0.15) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.page-eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(37,99,235,0.15); border: 1px solid rgba(37,99,235,0.35);
    border-radius: 100px; padding: 4px 14px;
    font-size: 11px; font-weight: 600; color: #60a5fa;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 14px;
}
.page-title { font-size: 38px; font-weight: 800; letter-spacing: -0.03em; color: #f1f5f9; line-height: 1.1; }
.page-title .accent { background: linear-gradient(90deg,#3b82f6,#818cf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.page-sub { font-size: 14px; color: #64748b; margin-top: 10px; }

.kpi-card {
    background: #060f1f; border: 1px solid #0f2040; border-radius: 14px;
    padding: 20px 22px; position: relative; overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.kpi-card:hover { border-color: #1e3a8a; transform: translateY(-2px); }
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #1e3a8a, #3b82f6); border-radius: 14px 14px 0 0;
}
.kpi-icon { font-size: 20px; margin-bottom: 10px; display: block; }
.kpi-value { font-size: 28px; font-weight: 800; color: #f1f5f9; letter-spacing: -0.03em; line-height: 1; font-family: 'JetBrains Mono', monospace; }
.kpi-label { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 5px; font-weight: 600; }

.section-header { display: flex; align-items: baseline; gap: 12px; margin: 36px 0 18px; }
.section-title { font-size: 18px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; }
.section-tag { font-size: 11px; color: #3b82f6; font-family: 'JetBrains Mono', monospace; font-weight: 500; background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.2); border-radius: 6px; padding: 2px 8px; }

.chart-card { background: #060f1f; border: 1px solid #0f2040; border-radius: 16px; padding: 22px; margin-bottom: 18px; }
.chart-label { font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 14px; }

.filter-card { background: #060f1f; border: 1px solid #0f2040; border-radius: 14px; padding: 20px; margin-bottom: 20px; }
.filter-label { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 6px; }

div[data-testid="stMetricValue"] > div { font-size: 22px !important; font-weight: 800 !important; color: #f1f5f9 !important; font-family: 'JetBrains Mono', monospace !important; }
div[data-testid="stMetricLabel"] > div { font-size: 10px !important; color: #475569 !important; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600 !important; }
.block-container { padding-top: 2rem !important; }
.stDivider { border-color: #0f2040 !important; }

.footer { border-top: 1px solid #0f2040; padding: 24px 0 12px; display: flex; justify-content: space-between; align-items: center; margin-top: 40px; }
.footer-left { font-size: 12px; color: #334155; font-weight: 500; }
.footer-right { font-size: 11px; color: #1e3a8a; font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>🤖 AI Career Intel</h2>
        <p>v1.0 · Final Year Project</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**Navigation**")
    st.page_link("app.py",                        label="🏠  Home"            )
    st.page_link("pages/Market_Analysis.py",      label="📈  Market Analysis" )
    st.page_link("pages/Salary_Predictor.py",     label="💰  Salary Predictor")
    st.page_link("pages/Career_Roadmaps.py",      label="🛣️  Career Roadmaps" )
    st.markdown("---")

    # ── Sidebar Filters ──
    st.markdown('<div class="filter-label">Filters</div>', unsafe_allow_html=True)
    selected_country = st.multiselect(
        "Country", options=sorted(df["country"].unique()), default=[]
    )
    selected_role = st.multiselect(
        "Job Role", options=sorted(df["job_role"].unique()), default=[]
    )
    selected_exp = st.multiselect(
        "Experience Level", options=sorted(df["experience_level"].unique()), default=[]
    )
    st.markdown("---")
   

# ── Filter data ───────────────────────────────────────
fdf = df.copy()
if selected_country: fdf = fdf[fdf["country"].isin(selected_country)]
if selected_role:    fdf = fdf[fdf["job_role"].isin(selected_role)]
if selected_exp:     fdf = fdf[fdf["experience_level"].isin(selected_exp)]

CHART_BG = "rgba(0,0,0,0)"
GRID_CLR  = "#0f2040"
TEXT_CLR  = "#94a3b8"

# ── Page Header ───────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">📈 Module 1</div>
    <div class="page-title">AI Job Market <span class="accent">Analysis</span></div>
    <div class="page-sub">Salary trends, role demand, country breakdowns — filtered in real time.</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────
kpis = [
    ("🗂️", f"{len(fdf):,}",                        "Records (filtered)"),
    ("🌍", str(fdf["country"].nunique()),           "Countries"),
    ("👔", str(fdf["job_role"].nunique()),          "Job Roles"),
    ("💵", f"${fdf['salary_usd'].mean():,.0f}",    "Avg. Salary"),
]
cols = st.columns(4)
for col, (icon, val, label) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Top Roles + Top Countries ─────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">Salary Benchmarks</div>
    <div class="section-tag">by role & country</div>
</div>""", unsafe_allow_html=True)

col_l, col_r = st.columns(2)

top_roles = (
    fdf.groupby("job_role")["salary_usd"].mean()
    .sort_values(ascending=False).head(10).reset_index()
)
with col_l:
    st.markdown('<div class="chart-card"><div class="chart-label">🏆 Top Paying Roles</div>', unsafe_allow_html=True)
    fig = px.bar(top_roles, x="salary_usd", y="job_role", orientation="h",
                 color="salary_usd",
                 color_continuous_scale=["#1e3a8a","#3b82f6","#818cf8"],
                 text=top_roles["salary_usd"].apply(lambda x: f"${x:,.0f}"),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont=dict(size=10, color=TEXT_CLR), marker_line_width=0)
    fig.update_layout(height=360, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      coloraxis_showscale=False, margin=dict(l=0,r=70,t=4,b=4),
                      xaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None),
                      yaxis=dict(showgrid=False,tickfont=dict(color=TEXT_CLR,size=11),title=None,autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

top_countries = (
    fdf.groupby("country")["salary_usd"].mean()
    .sort_values(ascending=False).head(10).reset_index()
)
with col_r:
    st.markdown('<div class="chart-card"><div class="chart-label">🌍 Top Paying Countries</div>', unsafe_allow_html=True)
    fig = px.bar(top_countries, x="country", y="salary_usd",
                 color="salary_usd",
                 color_continuous_scale=["#1e3a8a","#2563eb","#6366f1"],
                 text=top_countries["salary_usd"].apply(lambda x: f"${x:,.0f}"),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont=dict(size=9, color=TEXT_CLR), marker_line_width=0)
    fig.update_layout(height=360, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      coloraxis_showscale=False, margin=dict(l=4,r=4,t=4,b=50),
                      xaxis=dict(showgrid=False,tickfont=dict(color=TEXT_CLR,size=10),title=None,tickangle=-30),
                      yaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Experience + Work Mode ────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">Workforce Breakdown</div>
    <div class="section-tag">experience · work mode · education</div>
</div>""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

exp_sal = (
    fdf.groupby("experience_level")["salary_usd"].mean()
    .reset_index().sort_values("salary_usd", ascending=True)
)
with col_a:
    st.markdown('<div class="chart-card"><div class="chart-label">📊 Experience Level vs Salary</div>', unsafe_allow_html=True)
    fig = px.bar(exp_sal, x="salary_usd", y="experience_level", orientation="h",
                 color="salary_usd",
                 color_continuous_scale=["#1e3a8a","#3b82f6","#818cf8"],
                 text=exp_sal["salary_usd"].apply(lambda x: f"${x:,.0f}"),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont=dict(size=11, color=TEXT_CLR), marker_line_width=0)
    fig.update_layout(height=300, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      coloraxis_showscale=False, margin=dict(l=0,r=80,t=4,b=4),
                      xaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None),
                      yaxis=dict(showgrid=False,tickfont=dict(color=TEXT_CLR,size=12),title=None))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

work_sal = (
    fdf.groupby("work_mode")["salary_usd"].mean()
    .reset_index().sort_values("salary_usd", ascending=True)
)
with col_b:
    st.markdown('<div class="chart-card"><div class="chart-label">🏠 Work Mode vs Salary</div>', unsafe_allow_html=True)
    fig = px.bar(work_sal, x="salary_usd", y="work_mode", orientation="h",
                 color="work_mode",
                 color_discrete_sequence=["#1e3a8a","#2563eb","#3b82f6"],
                 text=work_sal["salary_usd"].apply(lambda x: f"${x:,.0f}"),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont=dict(size=11, color=TEXT_CLR), marker_line_width=0)
    fig.update_layout(height=300, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      showlegend=False, margin=dict(l=0,r=80,t=4,b=4),
                      xaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None),
                      yaxis=dict(showgrid=False,tickfont=dict(color=TEXT_CLR,size=12),title=None))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Education + Company Size ──────────────────────────
col_c, col_d = st.columns(2)

edu_sal = fdf.groupby("education_required")["salary_usd"].mean().reset_index()
with col_c:
    st.markdown('<div class="chart-card"><div class="chart-label">🎓 Education Level vs Salary</div>', unsafe_allow_html=True)
    fig = px.bar(edu_sal, x="education_required", y="salary_usd",
                 color="salary_usd",
                 color_continuous_scale=["#1e3a8a","#3b82f6","#818cf8"],
                 text=edu_sal["salary_usd"].apply(lambda x: f"${x:,.0f}"),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont=dict(size=10, color=TEXT_CLR), marker_line_width=0)
    fig.update_layout(height=300, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      coloraxis_showscale=False, margin=dict(l=4,r=4,t=4,b=40),
                      xaxis=dict(showgrid=False,tickfont=dict(color=TEXT_CLR,size=10),title=None),
                      yaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

co_sal = fdf.groupby("company_size")["salary_usd"].mean().reset_index()
with col_d:
    st.markdown('<div class="chart-card"><div class="chart-label">🏢 Company Size vs Salary</div>', unsafe_allow_html=True)
    fig = px.bar(co_sal, x="company_size", y="salary_usd",
                 color="company_size",
                 color_discrete_sequence=["#1e3a8a","#2563eb","#3b82f6"],
                 text=co_sal["salary_usd"].apply(lambda x: f"${x:,.0f}"),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont=dict(size=10, color=TEXT_CLR), marker_line_width=0)
    fig.update_layout(height=300, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      showlegend=False, margin=dict(l=4,r=4,t=4,b=40),
                      xaxis=dict(showgrid=False,tickfont=dict(color=TEXT_CLR,size=10),title=None),
                      yaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Specialization + Salary Distribution ─────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">Specialization & Distribution</div>
    <div class="section-tag">demand · spread</div>
</div>""", unsafe_allow_html=True)

col_e, col_f = st.columns(2)

spec = fdf["ai_specialization"].value_counts().head(8).reset_index()
spec.columns = ["Specialization","Count"]
with col_e:
    st.markdown('<div class="chart-card"><div class="chart-label">🤖 AI Specialization Demand</div>', unsafe_allow_html=True)
    fig = px.pie(spec, names="Specialization", values="Count", hole=0.55,
                 color_discrete_sequence=["#1e3a8a","#1d4ed8","#2563eb","#3b82f6","#60a5fa","#6366f1","#818cf8","#a5b4fc"],
                 template="plotly_dark")
    fig.update_traces(textfont=dict(size=10,color="#e2e8f0"), textposition="outside",
                      marker=dict(line=dict(color="#040d1a",width=2)))
    fig.update_layout(height=300, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      legend=dict(font=dict(color=TEXT_CLR,size=10),bgcolor="rgba(0,0,0,0)"),
                      margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_f:
    st.markdown('<div class="chart-card"><div class="chart-label">💰 Salary Distribution</div>', unsafe_allow_html=True)
    fig = px.histogram(fdf, x="salary_usd", nbins=40, template="plotly_dark",
                       color_discrete_sequence=["#2563eb"])
    fig.update_traces(marker_line_width=0, opacity=0.85)
    fig.update_layout(height=300, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                      margin=dict(l=4,r=4,t=4,b=4),
                      xaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None),
                      yaxis=dict(showgrid=True,gridcolor=GRID_CLR,tickfont=dict(color=TEXT_CLR,size=10),title=None))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Dataset Preview ───────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">Dataset Preview</div>
    <div class="section-tag">first 20 rows</div>
</div>""", unsafe_allow_html=True)

st.dataframe(
    fdf.head(20),
    use_container_width=True,
    hide_index=True
)

st.markdown("""
<div class="footer">
    <div class="footer-left">AI Career Intelligence Platform · Market Analysis</div>
    <div class="footer-right">Final Year Project · 2026</div>
</div>
""", unsafe_allow_html=True)