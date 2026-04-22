import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# Load model
model = joblib.load("xgb_model.pkl")

# Page config
st.set_page_config(
    page_title="FactoryGuard AI",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── HEADER ──────────────────────────────────────────────
col_logo, col_title, col_status = st.columns([0.5, 4, 1.5])
with col_logo:
    st.markdown("# 🏭")
with col_title:
    st.title("FactoryGuard AI")
    st.caption("Predictive Maintenance Intelligence System | XGBoost Classifier")
with col_status:
    st.success("🟢 System Online")

st.divider()

# ── TABS ────────────────────────────────────────────────
tab_predict, tab_about = st.tabs(["🔬 Run Diagnostic", "📋 About the Model"])

# ════════════════════════════════════════════════════════
# TAB 1 — PREDICTION
# ════════════════════════════════════════════════════════
with tab_predict:

    left, right = st.columns([1, 1.2], gap="large")

    # ── INPUT SIDE ──────────────────────────────────────
    with left:

        # Sensor readings
        st.subheader("⚙️ Sensor Readings")

        vibration   = st.slider("🔵 Vibration (mm/s)",  min_value=0.0, max_value=10.0,  value=1.5,  step=0.1)
        pressure    = st.slider("🟣 Pressure (bar)",    min_value=0.0, max_value=200.0, value=50.0, step=1.0)
        temperature = st.slider("🔴 Temperature (°C)", min_value=0.0, max_value=500.0, value=300.0, step=1.0)

        # Live sensor metrics
        st.markdown("##### 📟 Live Readings")
        m1, m2, m3 = st.columns(3)
        m1.metric("Vibration",   f"{vibration:.1f}",  delta="mm/s",  delta_color="off")
        m2.metric("Pressure",    f"{pressure:.0f}",   delta="bar",   delta_color="off")
        m3.metric("Temperature", f"{temperature:.0f}", delta="°C",   delta_color="off")

        st.divider()

        # Failure flags
        st.subheader("🚨 Failure Flags")
        st.caption("Toggle any active failure indicators below")

        fa, fb = st.columns(2)
        with fa:
            pwf = st.toggle("⚡ Power Failure (PWF)")
            osf = st.toggle("💪 Overstrain (OSF)")
        with fb:
            twf = st.toggle("🔧 Tool Wear (TWF)")
            hdf = st.toggle("🌡️ Heat Dissipation (HDF)")

        active_flags = [f for f, v in [("PWF", pwf), ("OSF", osf), ("TWF", twf), ("HDF", hdf)] if v]
        if active_flags:
            st.error(f"🔴 Active Flags Detected: **{', '.join(active_flags)}**")
        else:
            st.info("✅ All failure flags nominal")

        st.divider()
        predict_btn = st.button("🚀 Run Diagnostic Analysis", type="primary", use_container_width=True)

    # ── OUTPUT SIDE ─────────────────────────────────────
    with right:

        if predict_btn:
            with st.spinner("Analyzing sensor data..."):
                input_data = pd.DataFrame({
                    'UDI':                  [8001],
                    'temperature':          [temperature],
                    'Process temperature K':[temperature],
                    'vibration':            [vibration],
                    'pressure':             [pressure],
                    'Tool wear min':        [0],
                    'TWF':                  [int(twf)],
                    'HDF':                  [int(hdf)],
                    'PWF':                  [int(pwf)],
                    'OSF':                  [int(osf)],
                    'RNF':                  [0],
                    'temp_roll_mean_3':     [temperature],
                    'vib_roll_std_3':       [0.0]
                })
                probability = model.predict_proba(input_data)[0][1]

            pct = round(probability * 100, 1)

            # Risk level
            if probability < 0.3:
                risk_label = "LOW RISK"
                gauge_color = "#00C853"
                rec = "✅ Machine operating normally. Maintain standard monitoring schedule."
                st.success(f"### 🟢 {risk_label} — Failure Probability: **{pct}%**")
            elif probability < 0.7:
                risk_label = "MEDIUM RISK"
                gauge_color = "#FFB300"
                rec = "⚠️ Elevated stress detected. Schedule an inspection within 48 hours."
                st.warning(f"### 🟡 {risk_label} — Failure Probability: **{pct}%**")
            else:
                risk_label = "HIGH RISK"
                gauge_color = "#FF1744"
                rec = "🚨 Critical failure imminent! Initiate emergency maintenance immediately."
                st.error(f"### 🔴 {risk_label} — Failure Probability: **{pct}%**")

            # ── PLOTLY GAUGE ────────────────────────────
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pct,
                number={"suffix": "%", "font": {"size": 48, "color": gauge_color}},
                delta={"reference": 50, "valueformat": ".1f",
                       "increasing": {"color": "#FF1744"},
                       "decreasing": {"color": "#00C853"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1,
                             "tickcolor": "gray", "tickvals": [0, 30, 70, 100],
                             "ticktext": ["Safe", "Caution", "Danger", "Critical"]},
                    "bar":  {"color": gauge_color, "thickness": 0.25},
                    "bgcolor": "white",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0,  30], "color": "rgba(0,200,83,0.12)"},
                        {"range": [30, 70], "color": "rgba(255,179,0,0.12)"},
                        {"range": [70,100], "color": "rgba(255,23,68,0.12)"},
                    ],
                    "threshold": {
                        "line": {"color": gauge_color, "width": 3},
                        "thickness": 0.8,
                        "value": pct
                    }
                },
                title={"text": "Machine Failure Probability", "font": {"size": 16}}
            ))
            fig.update_layout(
                height=300,
                margin=dict(t=60, b=10, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                font={"family": "sans-serif"}
            )
            st.plotly_chart(fig, use_container_width=True)

            # ── SENSOR ANALYSIS BAR CHART ───────────────
            st.markdown("##### 📊 Sensor Readings vs Safe Threshold")

            sensor_df = pd.DataFrame({
                "Sensor":   ["Vibration", "Pressure", "Temperature"],
                "Reading":  [vibration,   pressure,   temperature],
                "Max Safe": [7.0,         150.0,      400.0],
            })
            sensor_df["% of Safe Limit"] = (sensor_df["Reading"] / sensor_df["Max Safe"] * 100).round(1)

            bar_fig = go.Figure()
            bar_fig.add_trace(go.Bar(
                name="Reading",
                x=sensor_df["Sensor"],
                y=sensor_df["% of Safe Limit"],
                marker_color=[
                    "#FF1744" if v > 100 else "#FFB300" if v > 80 else "#00C853"
                    for v in sensor_df["% of Safe Limit"]
                ],
                text=[f"{v}%" for v in sensor_df["% of Safe Limit"]],
                textposition="outside"
            ))
            bar_fig.add_hline(y=100, line_dash="dash", line_color="red",
                              annotation_text="Safe Limit", annotation_position="top right")
            bar_fig.update_layout(
                height=240,
                margin=dict(t=20, b=20, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)", title="% of Safe Limit"),
                showlegend=False
            )
            st.plotly_chart(bar_fig, use_container_width=True)

            # ── SUMMARY TABLE ───────────────────────────
            st.markdown("##### 🗂️ Diagnostic Summary")
            summary_df = pd.DataFrame({
                "Parameter": ["Vibration", "Pressure", "Temperature",
                              "Active Flags", "Failure Probability", "Risk Level"],
                "Value":     [f"{vibration:.1f} mm/s", f"{pressure:.0f} bar",
                              f"{temperature:.0f} °C",
                              ", ".join(active_flags) if active_flags else "None",
                              f"{pct}%", risk_label],
                "Status":    [
                    "⚠️ High"   if vibration    > 7   else "✅ Normal",
                    "⚠️ High"   if pressure     > 150 else "✅ Normal",
                    "⚠️ High"   if temperature  > 400 else "✅ Normal",
                    f"🔴 {len(active_flags)} triggered" if active_flags else "✅ All clear",
                    f"{'🔴' if probability >= 0.7 else '🟡' if probability >= 0.3 else '🟢'} {risk_label}",
                    "🔴 Critical" if probability >= 0.7 else "🟡 Monitor" if probability >= 0.3 else "✅ Safe"
                ]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

            # ── RECOMMENDATION ──────────────────────────
            st.markdown("##### 💡 Recommendation")
            if probability >= 0.7:
                st.error(rec)
            elif probability >= 0.3:
                st.warning(rec)
            else:
                st.success(rec)

        else:
            st.info("👈 Configure sensor values and press **Run Diagnostic Analysis** to begin.")
            st.markdown("""
            #### How it works
            1. **Adjust the sliders** to match live sensor readings
            2. **Toggle failure flags** if any are currently active on the machine
            3. **Run the analysis** — the XGBoost model scores failure probability
            4. **Read the output** — gauge, sensor chart, and recommendation

            #### Risk Levels
            | Level | Probability | Action |
            |-------|------------|--------|
            | 🟢 Low | < 30% | Normal operation |
            | 🟡 Medium | 30–70% | Schedule inspection |
            | 🔴 High | > 70% | Emergency maintenance |
            """)

# ════════════════════════════════════════════════════════
# TAB 2 — ABOUT
# ════════════════════════════════════════════════════════
with tab_about:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🤖 Model Information")
        st.markdown("""
        | Property | Detail |
        |----------|--------|
        | **Algorithm** | XGBoost Classifier |
        | **Task** | Binary Classification |
        | **Output** | Failure Probability (0–1) |
        | **Features** | 13 input features |
        | **Threshold** | 0.5 (default) |
        """)

        st.subheader("📥 Input Features")
        st.markdown("""
        **Sensor Data**
        - Temperature (°C) & Process Temperature (K)
        - Vibration (mm/s), Pressure (bar), Tool Wear (min)

        **Failure Flags:** TWF · HDF · PWF · OSF · RNF

        **Engineered Features**
        - `temp_roll_mean_3` — Rolling mean of temperature
        - `vib_roll_std_3` — Rolling std of vibration
        """)

    with c2:
        st.subheader("⚡ Tech Stack")
        st.markdown("""
        | Layer | Technology |
        |-------|-----------|
        | **ML Model** | XGBoost |
        | **Data** | Pandas, NumPy |
        | **Visualization** | Plotly |
        | **Frontend** | Streamlit |
        | **Deployment** | Streamlit Cloud |
        | **Saved Model** | Joblib (.pkl) |
        """)

        st.subheader("🚀 Future Improvements")
        st.markdown("""
        - 🌐 Real-time IoT sensor integration
        - 📊 Historical trend monitoring dashboard
        - 📱 SMS / Email alert system
        - 🧠 Deep learning model upgrade
        """)

        st.subheader("⚠️ Limitations")
        st.warning("""
        - No real-time sensor stream (manual input only)
        - Accuracy depends on training data quality
        - Model is dataset-specific; may need retraining for new machines
        """)

st.divider()
st.caption("⚡ FactoryGuard AI · Predictive Maintenance System · Built by Abhishek")
