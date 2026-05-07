import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="HR-AutoMine AI", layout="wide")

# =========================
# CSS PROFESIONAL
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter';
    background-color: #0a0c10;
    color: white;
}

.card {
    background-color: #1a1d24;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #2a2f3a;
    transition: 0.3s;
}

.card:hover {
    background-color: #252a35;
    transform: scale(1.02);
}

.kpi {
    font-size: 26px;
    font-weight: bold;
}

.small {
    color: #a0a4b0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🤖 HR-AutoMine AI")
st.subheader("Autonomía total - La IA decide, los humanos ejecutan")

st.markdown("---")

# =========================
# KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="card">⚡ Reducción accidentes<br><div class="kpi">-38%</div><div class="small">Tendencia positiva</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">📊 Eficiencia operativa<br><div class="kpi">94%</div></div>', unsafe_allow_html=True)
    st.progress(0.94)

with col3:
    st.markdown('<div class="card">💰 Ahorro anual<br><div class="kpi">S/ 2.42M</div></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">🤖 Decisiones IA<br><div class="kpi">12,847</div></div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# GRÁFICOS
# =========================

col1, col2 = st.columns(2)

# --- Conflictos
with col1:
    st.subheader("📉 Reducción de Conflictos Socioambientales")

    fig1 = px.line(
        x=["E1","E2","E3","E4","E5","E6"],
        y=[24,18,15,11,8,5],
        markers=True
    )
    fig1.update_traces(line_color="#2ecc71")
    st.plotly_chart(fig1, use_container_width=True)

# --- Fatiga
with col2:
    st.subheader("⚠️ Nivel de Fatiga por Turno")

    fig2 = px.bar(
        x=["Día","Tarde","Noche"],
        y=[32,58,78],
        color=[32,58,78],
        color_continuous_scale=["green","yellow","red"]
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# DEFICITS
# =========================
st.subheader("📊 Déficits de habilidades")

fig3 = px.pie(
    values=[45,30,25],
    names=["Seguridad operativa","Equipos","Ambiental"]
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# =========================
# AGENTES IA
# =========================

st.subheader("🧠 Sistema de 6 Agentes IA")

def run_toast(msg):
    st.toast(msg)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🤖 Agente 1 - Reclutamiento")
    st.write("Selecciona candidatos óptimos")
    if st.button("Simular 1"):
        run_toast("✅ AGENTE 1: Candidato seleccionado automáticamente. Compatibilidad: 92%")

with col2:
    st.markdown("### 🛡 Agente 2 - Validación")
    st.write("Verifica certificaciones")
    if st.button("Simular 2"):
        run_toast("⚠️ AGENTE 2: Certificación obligatoria no vigente")

with col3:
    st.markdown("### 🔄 Agente 3 - Escalas")
    st.write("Optimiza cobertura")
    if st.button("Simular 3"):
        run_toast("🔄 AGENTE 3: Cobertura reasignada")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("### 📊 Agente 4 - Rendimiento")
    if st.button("Simular 4"):
        run_toast("📉 AGENTE 4: Bajo rendimiento detectado")

with col5:
    st.markdown("### ⚠️ Agente 5 - Fatiga")
    if st.button("Simular 5"):
        run_toast("🚨 AGENTE 5: ALTO RIESGO DE FATIGA")

with col6:
    st.markdown("### 🎓 Agente 6 - Capacitación")
    if st.button("Simular 6"):
        run_toast("📚 AGENTE 6: Curso asignado automáticamente")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.success("🚀 IA autónoma en operación minera")
st.caption("0 intervención humana en decisiones operativas")