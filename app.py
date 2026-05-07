import streamlit as st

st.set_page_config(page_title="AI Workforce System", layout="wide")

# HEADER PRO
st.markdown("""
# 🤖 AI WORKFORCE SYSTEM
### Sistema inteligente de reclutamiento y gestión de talento
""")

st.markdown("---")

# INPUTS EN COLUMNAS
col1, col2, col3 = st.columns(3)

with col1:
    nombre = st.text_input("👤 Nombre del candidato")

with col2:
    exp = st.number_input("📊 Años de experiencia", 0, 40, 1)

with col3:
    cert = st.selectbox("🎓 Certificación", ["Sí", "No"])

horas = st.slider("⏱ Horas trabajadas por día", 0, 24, 8)

st.markdown("---")

# BOTÓN PRINCIPAL
if st.button("🚀 Ejecutar análisis de IA"):

    st.markdown("## 🧠 Panel de Agentes IA")

    # KPI CARDS
    col1, col2, col3 = st.columns(3)

    score = 50 + exp * 5 + (30 if cert == "Sí" else 0)

    estado = "APROBADO" if score >= 70 else "RECHAZADO"

    col1.metric("Score IA", score)
    col2.metric("Estado", estado)
    col3.metric("Riesgo", "BAJO" if horas < 10 else "ALTO")

    st.markdown("---")

    # AGENTES VISUALES
    st.info("🧠 Agente 1: Reclutamiento → Analizando CV")
    st.success(f"📋 Agente 2: Validación → {estado}")

    if estado == "APROBADO":
        st.success("📅 Agente 3: Escalas → Asignado a operación")
    else:
        st.error("📅 Agente 3: Escalas → No asignado")

    if exp < 2:
        st.warning("📊 Agente 4: Desempeño → Bajo")
    elif exp < 5:
        st.info("📊 Agente 4: Desempeño → Medio")
    else:
        st.success("📊 Agente 4: Desempeño → Alto")

    if horas >= 12:
        st.error("⚠️ Agente 5: Fatiga → ALTO RIESGO")
    else:
        st.success("⚠️ Agente 5: Fatiga → Controlado")

    if cert == "No":
        st.warning("🎓 Agente 6: Capacitación → Obligatoria")
    else:
        st.success("🎓 Agente 6: Capacitación → OK")

    st.markdown("---")
    st.success("✅ SISTEMA FINALIZADO - ANÁLISIS COMPLETO")