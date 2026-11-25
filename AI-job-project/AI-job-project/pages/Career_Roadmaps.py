import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Career Roadmaps · AI Career Intel",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    jobs_df    = pd.read_csv("data/global_ai_jobs.csv")
    roadmap_df = pd.read_csv("data/roadmaps.csv")
    return jobs_df, roadmap_df

jobs_df, roadmap_df = load_data()

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
    padding: 36px 44px; border-radius: 18px;
    background: linear-gradient(135deg, #0c1f45 0%, #0a1628 60%, #060f1f 100%);
    border: 1px solid #1e3a8a; margin-bottom: 32px; position: relative; overflow: hidden;
}
.page-header::after {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(37,99,235,0.15) 0%, transparent 70%);
    border-radius: 50%; pointer-events: none;
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

/* KPI cards */
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

/* Timeline roadmap */
.timeline-wrap { position: relative; padding-left: 28px; }
.timeline-wrap::before {
    content: ''; position: absolute; left: 10px; top: 8px; bottom: 8px;
    width: 2px; background: linear-gradient(180deg, #1e3a8a, #3b82f6, #6366f1);
    border-radius: 2px;
}
.timeline-step {
    position: relative; margin-bottom: 14px;
    background: #060f1f; border: 1px solid #0f2040;
    border-radius: 12px; padding: 16px 18px;
    transition: border-color 0.2s, transform 0.15s;
}
.timeline-step:hover { border-color: #2563eb; transform: translateX(4px); }
.timeline-step::before {
    content: ''; position: absolute;
    left: -23px; top: 18px;
    width: 10px; height: 10px;
    background: #2563eb; border-radius: 50%;
    border: 2px solid #040d1a;
    box-shadow: 0 0 0 2px #1e3a8a;
}
.step-num {
    font-size: 10px; font-weight: 700; color: #3b82f6;
    text-transform: uppercase; letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace; margin-bottom: 4px;
}
.step-text { font-size: 13px; color: #cbd5e1; line-height: 1.5; font-weight: 500; }

/* Snapshot panel */
.snapshot-panel {
    background: #060f1f; border: 1px solid #0f2040; border-radius: 16px; padding: 24px;
    position: sticky; top: 20px;
}
.snap-title { font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 18px; letter-spacing: -0.01em; }
.snap-progress-label {
    display: flex; justify-content: space-between;
    font-size: 11px; color: #64748b; margin-bottom: 6px;
}
.snap-track { height: 6px; background: #0f2040; border-radius: 3px; overflow: hidden; margin-bottom: 20px; }
.snap-fill { height: 100%; background: linear-gradient(90deg,#1e3a8a,#3b82f6); border-radius: 3px; }

.snap-stat { margin-bottom: 14px; }
.snap-stat-label { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 3px; }
.snap-stat-val { font-size: 20px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #f1f5f9; }

.pill-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 16px; }
.pill {
    background: rgba(37,99,235,0.12); border: 1px solid rgba(37,99,235,0.25);
    border-radius: 100px; padding: 4px 12px;
    font-size: 11px; color: #60a5fa; font-weight: 500;
}

/* Strategy box */
.strategy-box {
    background: #060f1f; border: 1px solid #0f2040; border-radius: 14px; padding: 24px;
    margin-top: 24px;
}
.strategy-title { font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 14px; }
.strategy-item {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid #0a1628;
}
.strategy-item:last-child { border-bottom: none; }
.strategy-num {
    width: 22px; height: 22px; border-radius: 6px;
    background: rgba(37,99,235,0.15); border: 1px solid rgba(37,99,235,0.3);
    font-size: 11px; font-weight: 700; color: #60a5fa;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; font-family: 'JetBrains Mono', monospace;
}
.strategy-text { font-size: 13px; color: #94a3b8; line-height: 1.5; }

.section-header { display: flex; align-items: baseline; gap: 12px; margin: 32px 0 16px; }
.section-title { font-size: 18px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; }
.section-tag { font-size: 11px; color: #3b82f6; font-family: 'JetBrains Mono', monospace; font-weight: 500; background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.2); border-radius: 6px; padding: 2px 8px; }

.block-container { padding-top: 2rem !important; }
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

    st.markdown("### 🎯 Select Career Path")

    role = st.selectbox(
        "",
        sorted(roadmap_df["role"].unique())
    )
    st.markdown("""
    <div style='font-size:11px; color:#334155; padding: 4px 4px 0;'>
        <div style='margin-bottom:6px; color:#475569; text-transform:uppercase; letter-spacing:0.08em; font-size:10px; font-weight:600;'>Roadmap covers</div>
        <div style='margin-bottom:4px;'>✅ Learning Steps</div>
        <div style='margin-bottom:4px;'>✅ Career Snapshot</div>
        <div>✅ Job Strategy</div>
    </div>
    """, unsafe_allow_html=True)

# ── Data for selected role ────────────────────────────
role_mapping = {
     "AI Research Scientist": "Research Scientist",
    "Machine Learning Engineer": "Machine Learning Engineer",
    "Computer Vision Engineer": "Computer Vision Engineer",
    "Data Scientist": "Data Scientist",
    "Data Analyst": "Data Analyst",
    "NLP Engineer": "NLP Engineer"
}

dataset_role = role_mapping.get(role, role)

job_data = jobs_df[
    jobs_df["job_role"] == dataset_role
]

if len(job_data) > 0:

    avg_salary = float(job_data["salary_usd"].mean())
    growth = float(job_data["career_growth_score"].mean())
    openings = float(job_data["job_openings"].mean())
    skill_dem = float(job_data["skill_demand_score"].mean())

else:

    avg_salary = 0
    growth = 0
    openings = 0
    skill_dem = 0

    st.warning(
        f"No matching dataset role found for: {role}"
    )

# KEEP THIS
role_steps = roadmap_df[
    roadmap_df["role"] == role
].sort_values("step_no")



# ── Page Header ───────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-eyebrow">🛣️ Module 3</div>
    <div class="page-title">Career <span class="accent">Roadmaps</span></div>
    <div class="page-sub">Step-by-step learning paths for AI roles · Currently viewing: <strong style="color:#93c5fd">{role}</strong></div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────
kpis = [
    ("💵", f"${avg_salary:,.0f}",  "Average Salary"),
    ("📈", f"{growth:.1f}/100",    "Growth Score"),
    ("🏢", f"{int(openings)}",     "Job Openings"),
    ("⚡", f"{skill_dem:.1f}/100", "Skill Demand"),
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

# ── Main layout: timeline left, snapshot right ────────
st.markdown("""
<div class="section-header">
    <div class="section-title">Learning Roadmap</div>
    <div class="section-tag">step by step</div>
</div>""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    if len(role_steps) > 0:
        steps_html = '<div class="timeline-wrap">'
        for _, row in role_steps.iterrows():
            steps_html += f"""
            <div class="timeline-step">
                <div class="step-num">Step {int(row['step_no'])}</div>
                <div class="step-text">{row['step']}</div>
            </div>"""
        steps_html += '</div>'
        st.markdown(steps_html, unsafe_allow_html=True)
    else:
        st.warning("No roadmap steps available for this role.")

with col_right:

    st.subheader("🎯 Career Snapshot")

    st.metric(
        "Growth Score",
        f"{growth:.1f}/100"
    )

    st.progress(
        min(int(growth), 100)
    )

    st.metric(
        "Skill Demand",
        f"{skill_dem:.1f}/100"
    )

    st.progress(
        min(int(skill_dem), 100)
    )

    st.metric(
        "Average Salary",
        f"${avg_salary:,.0f}"
    )

    # Mini radar chart
    if len(job_data) > 0:
        categories  = ["Salary Score", "Growth", "Skill Demand", "Job Security", "Work-Life"]
        max_vals    = [200000, 100, 100, 100, 100]
        role_vals   = [
            avg_salary,
            growth,
            skill_dem,
            float(job_data["job_security_score"].mean()),
            float(job_data["work_life_balance_score"].mean()),
        ]
        norm_vals = [min(v/m*100, 100) for v, m in zip(role_vals, max_vals)]

        fig = go.Figure(go.Scatterpolar(
            r=norm_vals + [norm_vals[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(37,99,235,0.15)',
            line=dict(color='#3b82f6', width=2),
            marker=dict(color='#60a5fa', size=6)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color='#334155',size=9),
                                gridcolor='#0f2040', linecolor='#0f2040'),
                angularaxis=dict(tickfont=dict(color='#94a3b8',size=10), gridcolor='#0f2040', linecolor='#0f2040')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=240,
            margin=dict(l=30,r=30,t=20,b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Strategy ──────────────────────────────────────────
strategies = [
    ("01", "Master the fundamentals — Python, ML, deep learning core concepts."),
    ("02", "Build 3 portfolio projects and publish them to GitHub with READMEs."),
    ("03", "Complete at least one Kaggle competition in your specialization."),
    ("04", "Write 2–3 LinkedIn articles to establish domain expertise."),
    ("05", "Practice 50+ LeetCode problems and 10+ ML system design questions."),
    ("06", "Apply consistently — aim for 10 applications per week."),
]

st.markdown(f"""
<div class="strategy-box">
    <div class="strategy-title">✅ Recommended Strategy for {role}</div>
    {''.join(f'''<div class="strategy-item">
        <div class="strategy-num">{num}</div>
        <div class="strategy-text">{text}</div>
    </div>''' for num, text in strategies)}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="footer-left">AI Career Intelligence Platform · Career Roadmaps</div>
    <div class="footer-right">Final Year Project · 2026</div>
</div>
""", unsafe_allow_html=True)

