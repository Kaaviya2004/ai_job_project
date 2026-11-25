import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

st.set_page_config(
    page_title="Salary Predictor · AI Career Intel",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/global_ai_jobs.csv")

@st.cache_resource
def load_model():
    model    = joblib.load("models/salary_model.pkl")
    encoders = joblib.load("models/label_encoders.pkl")
    return model, encoders

df              = load_data()
model, encoders = load_model()

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

/* Input panel */
.input-panel {
    background: #060f1f; border: 1px solid #0f2040; border-radius: 16px; padding: 28px;
}
.input-section-label {
    font-size: 10px; color: #475569; text-transform: uppercase;
    letter-spacing: 0.12em; font-weight: 700; margin-bottom: 14px; margin-top: 22px;
}
.input-section-label:first-child { margin-top: 0; }

/* Result card */
.result-wrap {
    background: #060f1f; border: 1px solid #0f2040; border-radius: 16px;
    padding: 28px; height: 100%;
}
.result-empty {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 320px; color: #334155; text-align: center; gap: 12px;
}
.result-empty-icon { font-size: 48px; }
.result-empty-text { font-size: 14px; color: #334155; font-weight: 500; }

.result-label {
    font-size: 10px; color: #475569; text-transform: uppercase;
    letter-spacing: 0.12em; font-weight: 700; margin-bottom: 8px;
}
.result-salary {
    font-size: 56px; font-weight: 900; letter-spacing: -0.04em; line-height: 1;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #3b82f6, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.result-range {
    display: flex; gap: 12px; margin-top: 20px; flex-wrap: wrap;
}
.range-card {
    flex: 1; background: #040d1a; border: 1px solid #0f2040; border-radius: 10px;
    padding: 14px 16px; text-align: center; min-width: 100px;
}
.range-val { font-size: 18px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #f1f5f9; }
.range-lbl { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; font-weight: 600; }

.confidence-bar-wrap { margin-top: 24px; }
.confidence-label { font-size: 11px; color: #64748b; margin-bottom: 6px; display: flex; justify-content: space-between; }
.confidence-track { height: 6px; background: #0f2040; border-radius: 3px; overflow: hidden; }
.confidence-fill { height: 100%; background: linear-gradient(90deg, #1e3a8a, #3b82f6, #818cf8); border-radius: 3px; }

.insight-row { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
.insight-chip {
    background: rgba(37,99,235,0.1); border: 1px solid rgba(37,99,235,0.2);
    border-radius: 8px; padding: 8px 14px; font-size: 12px; color: #93c5fd; font-weight: 500;
}

/* Streamlit widget overrides */
.stSelectbox > div > div { background: #040d1a !important; border-color: #0f2040 !important; color: #e2e8f0 !important; }
.stSlider > div { color: #e2e8f0; }
div[data-testid="stSlider"] label { color: #94a3b8 !important; font-size: 12px !important; }
div[data-baseweb="select"] { background: #040d1a !important; }
.stButton > button {
    width: 100%; background: linear-gradient(135deg, #1e3a8a, #2563eb) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 14px !important; font-size: 15px !important; font-weight: 700 !important;
    letter-spacing: -0.01em; transition: all 0.2s !important; margin-top: 8px;
}
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }

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
    

# ── Page Header ───────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">💰 Module 2</div>
    <div class="page-title">AI Salary <span class="accent">Predictor</span></div>
   </div>
""", unsafe_allow_html=True)


# ── Layout: inputs left, result right ─────────────────
col_form, col_result = st.columns([1, 1], gap="large")

with col_form:

    st.markdown('<div class="input-section-label">📍 Location & Role</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        country = st.selectbox("Country", sorted(df["country"].unique()), key="country")
    with c2:
        job_role = st.selectbox("Job Role", sorted(df["job_role"].unique()), key="role")

    ai_specialization = st.selectbox(
        "AI Specialization", sorted(df["ai_specialization"].unique()), key="spec"
    )

    st.markdown('<div class="input-section-label">🎓 Background</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        experience_level = st.selectbox(
            "Experience Level", sorted(df["experience_level"].unique()), key="exp_lvl"
        )
    with c4:
        education_required = st.selectbox(
            "Education", sorted(df["education_required"].unique()), key="edu"
        )

    experience_years = st.slider("Years of Experience", 0, 20, 3, key="exp_yrs")

    st.markdown('<div class="input-section-label">🏢 Company & Work Style</div>', unsafe_allow_html=True)
    c5, c6, c7 = st.columns(3)
    with c5:
        industry = st.selectbox("Industry", sorted(df["industry"].unique()), key="ind")
    with c6:
        company_size = st.selectbox("Company Size", sorted(df["company_size"].unique()), key="co")
    with c7:
        work_mode = st.selectbox("Work Mode", sorted(df["work_mode"].unique()), key="wm")

    st.markdown('<div class="input-section-label">📊 Scores</div>', unsafe_allow_html=True)
    c8, c9 = st.columns(2)
    with c8:
        skill_demand_score   = st.slider("Skill Demand Score",   0, 100, 65, key="skill")
    with c9:
        career_growth_score  = st.slider("Career Growth Score",  0, 100, 70, key="growth")

    predict_btn = st.button("⚡ Predict My Salary", use_container_width=True)
    

# ── Result Panel ──────────────────────────────────────
with col_result:

    if predict_btn:

       
        try:
            input_df = pd.DataFrame({
                "country":             [country],
                "job_role":            [job_role],
                "ai_specialization":   [ai_specialization],
                "experience_level":    [experience_level],
                "experience_years":    [experience_years],
                "education_required":  [education_required],
                "industry":            [industry],
                "company_size":        [company_size],
                "work_mode":           [work_mode],
                "skill_demand_score":  [skill_demand_score],
                "career_growth_score": [career_growth_score],
            })
            for col_enc in encoders:
                input_df[col_enc] = encoders[col_enc].transform(input_df[col_enc])

            prediction = model.predict(input_df)[0]
            low        = prediction * 0.88
            high       = prediction * 1.12
            confidence = 92.17

            st.markdown(f"""
            <div class="result-label">Predicted Annual Salary (USD)</div>
            <div class="result-salary">${prediction:,.0f}</div>

            <div class="result-range">
                <div class="range-card">
                    <div class="range-val">${low:,.0f}</div>
                    <div class="range-lbl">Range Low</div>
                </div>
                <div class="range-card">
                    <div class="range-val">${prediction:,.0f}</div>
                    <div class="range-lbl">Predicted</div>
                </div>
                <div class="range-card">
                    <div class="range-val">${high:,.0f}</div>
                    <div class="range-lbl">Range High</div>
                </div>
            </div>

            <div class="confidence-bar-wrap">
                <div class="confidence-label">
                    <span>Model Confidence</span>
                    <span style="color:#60a5fa; font-weight:700;">{confidence}%</span>
                </div>
                <div class="confidence-track">
                    <div class="confidence-fill" style="width:{confidence}%;"></div>
                </div>
            </div>

            <div class="insight-row">
                <div class="insight-chip">📍 {country}</div>
                <div class="insight-chip">👔 {job_role}</div>
                <div class="insight-chip">⏱ {experience_years} yrs exp</div>
                <div class="insight-chip">🏢 {company_size}</div>
            </div>
            """, unsafe_allow_html=True)

            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction,
                number={"prefix": "$", "font": {"size": 28, "color": "#f1f5f9", "family": "JetBrains Mono"}},
                gauge={
                    "axis": {"range": [0, df["salary_usd"].max()],
                             "tickfont": {"color": "#475569", "size": 10},
                             "tickcolor": "#0f2040"},
                    "bar": {"color": "#2563eb", "thickness": 0.25},
                    "bgcolor": "#040d1a",
                    "bordercolor": "#0f2040",
                    "steps": [
                        {"range": [0, df["salary_usd"].quantile(0.25)],  "color": "#060f1f"},
                        {"range": [df["salary_usd"].quantile(0.25), df["salary_usd"].quantile(0.75)], "color": "#0a1628"},
                        {"range": [df["salary_usd"].quantile(0.75), df["salary_usd"].max()], "color": "#0c1f45"},
                    ],
                    "threshold": {"line": {"color": "#818cf8", "width": 3},
                                  "thickness": 0.8, "value": prediction},
                }
            ))
            fig_gauge.update_layout(
                height=220,
                paper_bgcolor="rgba(0,0,0,0)",
                font={"color": "#94a3b8"},
                margin=dict(l=20, r=20, t=30, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Market comparison bar
            market_avg = df["salary_usd"].mean()
            role_avg   = df[df["job_role"] == job_role]["salary_usd"].mean()
            diff_pct   = ((prediction - market_avg) / market_avg) * 100

            comp_df = pd.DataFrame({
                "Label": ["Market Avg", f"{job_role} Avg", "Your Prediction"],
                "Salary": [market_avg, role_avg, prediction]
            })
            fig_comp = go.Figure(go.Bar(
                x=comp_df["Label"],
                y=comp_df["Salary"],
                marker_color=["#1e3a8a","#2563eb","#818cf8"],
                text=[f"${v:,.0f}" for v in comp_df["Salary"]],
                textposition="outside",
                textfont=dict(color="#94a3b8", size=11),
            ))
            fig_comp.update_layout(
                height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, tickfont=dict(color="#94a3b8", size=11)),
                yaxis=dict(showgrid=True, gridcolor="#0f2040", tickfont=dict(color="#94a3b8", size=10)),
                margin=dict(l=4, r=4, t=30, b=4),
                title=dict(text=f"vs Market  ({'+' if diff_pct>=0 else ''}{diff_pct:.1f}% vs avg)",
                           font=dict(color="#64748b", size=12), x=0)
            )
            st.plotly_chart(fig_comp, use_container_width=True)

            

        except Exception as e:
            st.error(f"Prediction error: {e}")

    

st.markdown("""
<div class="footer">
    <div class="footer-left">AI Career Intelligence Platform · Salary Predictor</div>
    
</div>
""", unsafe_allow_html=True)