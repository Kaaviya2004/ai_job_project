import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Career Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/global_ai_jobs.csv")

df = load_data()

# =====================================================
# PRE-COMPUTE STATS
# =====================================================

total_jobs      = len(df)
total_countries = df["country"].nunique()
total_roles     = df["job_role"].nunique()
avg_salary      = df["salary_usd"].mean()
max_salary      = df["salary_usd"].max()
top_role        = df.groupby("job_role")["salary_usd"].mean().idxmax()
top_country     = df.groupby("country")["salary_usd"].mean().idxmax()

top_roles = (
    df.groupby("job_role")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(8)
    .reset_index()
)

top_countries = (
    df.groupby("country")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

specializations = (
    df["ai_specialization"]
    .value_counts()
    .head(6)
    .reset_index()
)
specializations.columns = ["Specialization", "Count"]

exp_salary = (
    df.groupby("experience_level")["salary_usd"]
    .mean()
    .reset_index()
    .sort_values("salary_usd", ascending=True)
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Hide Streamlit's default auto-generated page nav ── */
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #040d1a;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #060f1f !important;
    border-right: 1px solid #0f2040;
}

[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #64748b !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Sidebar logo area */
.sidebar-brand {
    padding: 20px 16px 24px;
    border-bottom: 1px solid #0f2040;
    margin-bottom: 8px;
}

.sidebar-brand h2 {
    font-size: 15px;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.01em;
}

.sidebar-brand p {
    font-size: 11px;
    color: #3b82f6;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 4px;
}

/* Sidebar nav links */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    border-radius: 8px;
    margin: 2px 8px;
    color: #94a3b8;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    text-decoration: none;
}

.nav-item:hover { background: #0f2040; color: #e2e8f0; }
.nav-item.active { background: #1e3a8a; color: #93c5fd; }

/* ── Hero ── */
.hero-wrap {
    padding: 60px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #0c1f45 0%,
        #0a1628 50%,
        #060f1f 100%
    );
    border: 1px solid #1e3a8a;
    margin-bottom: 32px;
}

.hero-wrap::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(37,99,235,0.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.10) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(37,99,235,0.15);
    border: 1px solid rgba(37,99,235,0.35);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    color: #60a5fa;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-eyebrow span { 
    width: 6px; height: 6px; 
    background: #3b82f6; 
    border-radius: 50%;
    display: inline-block;
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -0.03em;
    color: #f1f5f9;
    margin-bottom: 18px;
}

.hero-title .accent {
    background: linear-gradient(90deg, #3b82f6, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 16px;
    color: #94a3b8;
    line-height: 1.6;
    max-width: 520px;
    margin-bottom: 32px;
    font-weight: 400;
}

.hero-badges {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.badge {
    background: rgba(15,32,64,0.8);
    border: 1px solid #1e3a8a;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    color: #93c5fd;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
}

.hero-stat-cluster {
    position: absolute;
    right: 52px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 180px;
}

.hero-stat {
    background: rgba(15,32,64,0.7);
    border: 1px solid #1e3a8a;
    border-radius: 12px;
    padding: 14px 18px;
    backdrop-filter: blur(8px);
}

.hero-stat-value {
    font-size: 26px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}

.hero-stat-value .unit {
    font-size: 14px;
    color: #3b82f6;
    font-weight: 600;
}

.hero-stat-label {
    font-size: 10px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
    font-weight: 500;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 36px;
}

.kpi-card {
    background: #060f1f;
    border: 1px solid #0f2040;
    border-radius: 14px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}

.kpi-card:hover {
    border-color: #1e3a8a;
    transform: translateY(-2px);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #1e3a8a, #3b82f6);
    border-radius: 14px 14px 0 0;
}

.kpi-icon {
    font-size: 22px;
    margin-bottom: 12px;
    display: block;
}

.kpi-value {
    font-size: 30px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}

.kpi-label {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 6px;
    font-weight: 600;
}

.kpi-change {
    position: absolute;
    top: 18px; right: 18px;
    font-size: 11px;
    font-weight: 600;
    color: #22c55e;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 6px;
    padding: 3px 8px;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin: 40px 0 20px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}

.section-tag {
    font-size: 11px;
    color: #3b82f6;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 6px;
    padding: 2px 8px;
}

/* ── Feature Cards ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 40px;
}

.feature-card {
    background: #060f1f;
    border: 1px solid #0f2040;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.2s;
    cursor: pointer;
    text-decoration: none;
}

.feature-card:hover {
    border-color: #2563eb;
    background: #0a1628;
    transform: translateY(-3px);
}

.feature-icon {
    font-size: 28px;
    margin-bottom: 10px;
    display: block;
}

.feature-name {
    font-size: 13px;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 6px;
}

.feature-desc {
    font-size: 11px;
    color: #475569;
    line-height: 1.5;
}

/* ── Chart containers ── */
.chart-card {
    background: #060f1f;
    border: 1px solid #0f2040;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}

.chart-label {
    font-size: 13px;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Model Performance ── */
.model-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 36px;
}

.model-card {
    background: #060f1f;
    border: 1px solid #0f2040;
    border-radius: 14px;
    padding: 24px;
    text-align: center;
}

.model-value {
    font-size: 28px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
    color: #3b82f6;
}

.model-key {
    font-size: 10px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 6px;
    font-weight: 600;
}

/* ── About ── */
.about-card {
    background: linear-gradient(135deg, #060f1f, #040d1a);
    border: 1px solid #1e3a8a;
    border-radius: 16px;
    padding: 32px 36px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 32px;
    align-items: center;
    margin-bottom: 36px;
}

.about-title {
    font-size: 22px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}

.about-body {
    font-size: 14px;
    color: #64748b;
    line-height: 1.7;
}

.about-pills {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 16px;
}

.pill {
    background: rgba(37,99,235,0.12);
    border: 1px solid rgba(37,99,235,0.25);
    border-radius: 100px;
    padding: 4px 12px;
    font-size: 11px;
    color: #60a5fa;
    font-weight: 500;
}

.r2-display {
    text-align: center;
    background: rgba(15,32,64,0.6);
    border: 1px solid #1e3a8a;
    border-radius: 14px;
    padding: 28px 36px;
    min-width: 160px;
}

.r2-score {
    font-size: 48px;
    font-weight: 900;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #3b82f6, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    letter-spacing: -0.04em;
}

.r2-label {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 8px;
    font-weight: 600;
}

/* ── Footer ── */
.footer {
    border-top: 1px solid #0f2040;
    padding: 28px 0 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 40px;
}

.footer-left {
    font-size: 13px;
    color: #334155;
    font-weight: 500;
}

.footer-right {
    font-size: 11px;
    color: #1e3a8a;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Streamlit overrides ── */
div[data-testid="stMetric"] {
    background: #060f1f;
    border: 1px solid #0f2040;
    border-radius: 12px;
    padding: 16px 20px;
}

div[data-testid="stMetricValue"] > div {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

div[data-testid="stMetricLabel"] > div {
    font-size: 11px !important;
    color: #475569 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600 !important;
}

.stDivider { border-color: #0f2040 !important; }

/* hide default streamlit top padding */
.block-container { padding-top: 2rem !important; }

/* Fix plotly chart backgrounds */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>🤖 AI Career Intel</h2>
        <p>v1.0 · Final Year Project</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    st.page_link("app.py",                        label="🏠  Home",             )
    st.page_link("pages/Market_Analysis.py",      label="📈  Market Analysis"   )
    st.page_link("pages/Salary_Predictor.py",     label="💰  Salary Predictor"  )
    st.page_link("pages/Career_Roadmaps.py",      label="🛣️  Career Roadmaps"   )

    st.markdown("---")
   

# =====================================================
# HERO
# =====================================================

st.markdown(f"""
<div class="hero-wrap">

<div class="hero-eyebrow">
<span></span>
FINAL YEAR PROJECT • 2026
</div>

<div class="hero-title">
AI Career Intelligence Platform
</div>

<div class="hero-sub">
Analyze AI job market trends, predict salaries using machine learning,
and explore career opportunities across {total_countries} countries.
</div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# KPI CARDS
# =====================================================

st.markdown("""
<div class="kpi-grid">
""", unsafe_allow_html=True)

kpi_data = [
    ("🗂️", f"{total_jobs:,}",          "Total Job Records",     "AI Dataset"),
    ("🌍", f"{total_countries}",        "Countries Analyzed",    "Global Coverage"),
    ("👔", f"{total_roles}",            "AI Job Roles",          "Role Diversity"),
    ("💵", f"${int(avg_salary):,}",     "Avg. Salary (USD)",     "Market Benchmark"),
]

cols = st.columns(4)
for col, (icon, val, label, tag) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-change">{tag}</div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# FEATURE CARDS
# =====================================================

st.markdown("""
<div class="section-header">
    <div class="section-title">Platform Modules</div>
    <div class="section-tag">4 tools</div>
</div>
""", unsafe_allow_html=True)

features = [
    ("📈", "Market Analysis",   "KPIs, country heat maps, role salary trends, work mode & education breakdowns"),
    ("💰", "Salary Predictor",  "ML-powered prediction using 11 features with 92.17% accuracy"),
    ("🛣️", "Career Roadmaps",   "Step-by-step learning paths for 6 AI specializations"),
    ("🌍", "Country Analysis",  "Compare salaries, job openings, and AI maturity across nations"),
]

cols = st.columns(4)
for col, (icon, name, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <span class="feature-icon">{icon}</span>
            <div class="feature-name">{name}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# CHARTS — TOP ROLES & TOP COUNTRIES (2 col)
# =====================================================

st.markdown("""
<div class="section-header">
    <div class="section-title">Market Snapshot</div>
    <div class="section-tag">Live from dataset</div>
</div>
""", unsafe_allow_html=True)

col_l, col_r = st.columns(2)

# Chart config shared
CHART_BG = "rgba(0,0,0,0)"
GRID_CLR  = "#0f2040"
TEXT_CLR  = "#94a3b8"
BAR_CLR   = "#2563eb"
BAR_CLR2  = "#6366f1"

with col_l:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-label">🏆 Top Paying Roles</div>', unsafe_allow_html=True)

    fig_roles = px.bar(
        top_roles,
        x="salary_usd",
        y="job_role",
        orientation="h",
        color="salary_usd",
        color_continuous_scale=["#1e3a8a", "#3b82f6", "#818cf8"],
        template="plotly_dark",
        text=top_roles["salary_usd"].apply(lambda x: f"${x:,.0f}")
    )
    fig_roles.update_traces(
        textposition="outside",
        textfont=dict(size=10, color="#94a3b8"),
        marker_line_width=0,
    )
    fig_roles.update_layout(
        height=340,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor=GRID_CLR, tickfont=dict(color=TEXT_CLR, size=10), title=None),
        yaxis=dict(showgrid=False, tickfont=dict(color=TEXT_CLR, size=11), title=None, autorange="reversed"),
        margin=dict(l=0, r=60, t=10, b=10),
    )
    st.plotly_chart(fig_roles, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-label">🌍 Highest Paying Countries</div>', unsafe_allow_html=True)

    fig_ctry = px.bar(
        top_countries,
        x="country",
        y="salary_usd",
        color="salary_usd",
        color_continuous_scale=["#1e3a8a", "#2563eb", "#6366f1"],
        template="plotly_dark",
        text=top_countries["salary_usd"].apply(lambda x: f"${x:,.0f}")
    )
    fig_ctry.update_traces(
        textposition="outside",
        textfont=dict(size=9, color="#94a3b8"),
        marker_line_width=0,
    )
    fig_ctry.update_layout(
        height=340,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False, tickfont=dict(color=TEXT_CLR, size=10), title=None, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor=GRID_CLR, tickfont=dict(color=TEXT_CLR, size=10), title=None),
        margin=dict(l=10, r=10, t=10, b=50),
    )
    st.plotly_chart(fig_ctry, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# SPECIALIZATIONS + EXPERIENCE (2 col)
# =====================================================

col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-label">🤖 AI Specialization Distribution</div>', unsafe_allow_html=True)

    fig_spec = px.pie(
        specializations,
        names="Specialization",
        values="Count",
        color_discrete_sequence=[
            "#1e3a8a","#2563eb","#3b82f6","#60a5fa","#6366f1","#818cf8"
        ],
        template="plotly_dark",
        hole=0.55
    )
    fig_spec.update_traces(
        textfont=dict(size=11, color="#e2e8f0"),
        textposition="outside",
        marker=dict(line=dict(color="#040d1a", width=2))
    )
    fig_spec.update_layout(
        height=300,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        legend=dict(font=dict(color=TEXT_CLR, size=10), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_spec, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-label">📊 Experience Level vs Salary</div>', unsafe_allow_html=True)

    fig_exp = px.bar(
        exp_salary,
        x="salary_usd",
        y="experience_level",
        orientation="h",
        color="salary_usd",
        color_continuous_scale=["#1e3a8a", "#3b82f6", "#818cf8"],
        template="plotly_dark",
        text=exp_salary["salary_usd"].apply(lambda x: f"${x:,.0f}")
    )
    fig_exp.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#94a3b8"),
        marker_line_width=0,
    )
    fig_exp.update_layout(
        height=300,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor=GRID_CLR, tickfont=dict(color=TEXT_CLR, size=10), title=None),
        yaxis=dict(showgrid=False, tickfont=dict(color=TEXT_CLR, size=12), title=None),
        margin=dict(l=0, r=80, t=10, b=10),
    )
    st.plotly_chart(fig_exp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# MODEL PERFORMANCE
# =====================================================

st.markdown("""
<div class="section-header">
    <div class="section-title">Model Performance</div>
    <div class="section-tag">Random Forest</div>
</div>
""", unsafe_allow_html=True)

mc1, mc2, mc3 = st.columns(3)

model_stats = [
    ("0.9217",     "R² Score"),
    ("Random Forest Regressor", "Algorithm"),
    ("90,000",     "Training Records"),
]

for col, (val, key) in zip([mc1, mc2, mc3], model_stats):
    with col:
        st.markdown(f"""
        <div class="model-card">
            <div class="model-value">{val}</div>
            <div class="model-key">{key}</div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# ABOUT
# =====================================================

st.markdown("""
<div class="section-header">
    <div class="section-title">About This Project</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="about-card">
    <div>
        <div class="about-title">AI Career Intelligence Platform</div>
        <div class="about-body">
            A machine-learning powered dashboard that helps users analyze AI job market 
            trends across {total_countries} countries, predict expected salaries using 
            Random Forest Regression (R² = 0.9217), explore structured career roadmaps, 
            and compare opportunity by region, role, and experience level.
        </div>
        <div class="about-pills">
            <span class="pill">Streamlit</span>
            <span class="pill">Scikit-Learn</span>
            <span class="pill">Plotly</span>
            <span class="pill">Pandas</span>
            <span class="pill">Random Forest</span>
            <span class="pill">Joblib</span>
        </div>
    </div>
    <div class="r2-display">
        <div class="r2-score">92%</div>
        <div class="r2-label">Model Accuracy<br>(R² Score)</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

