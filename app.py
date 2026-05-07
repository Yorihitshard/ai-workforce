import streamlit as st

st.set_page_config(page_title="AI Workforce System", layout="wide")

st.title("🤖 AI WORKFORCE SYSTEM")
st.subheader("Sistema de 6 agentes IA para gestión de personal")

st.markdown("---")

# INPUTS
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("👤 Nombre del candidato")
    exp = st.number_input("📊 Años de experiencia", 0, 40, 1)

with col2:
    cert = st.selectbox("🎓 Certificación de seguridad", ["Sí", "No"])
    horas = st.number_input("⏱ Horas trabajadas por día", 0, 24, 8)

st.markdown("---")

if st.button("🚀 Ejecutar sistema de agentes"):

    st.markdown("## 🔄 Flujo de 6 Agentes IA")

    score = 50 + exp * 5 + (30 if cert == "Sí" else 0)

    st.success(f"🧠 Reclutamiento → Score: {score}")

    if score >= 85:
        estado = "APTO"
    elif score >= 70:
        estado = "OBSERVADO"
    else:
        estado = "NO APTO"

    st.info(f"📋 Validación → {estado}")

    if estado == "APTO":
        st.write("📅 Escalas → Asignado normal")
    elif estado == "OBSERVADO":
        st.write("📅 Escalas → Supervisión")
    else:
        st.write("📅 Escalas → No asignado")

    if exp < 2:
        st.write("📊 Desempeño → Bajo")
    elif exp < 5:
        st.write("📊 Desempeño → Medio")
    else:
        st.write("📊 Desempeño → Alto")

    if horas >= 12:
        st.warning("⚠️ Fatiga → ALTO RIESGO")
    elif horas >= 9:
        st.warning("⚠️ Fatiga → Riesgo medio")
    else:
        st.success("⚠️ Fatiga → Riesgo bajo")

    if cert == "No":
        st.error("🎓 Capacitación → Obligatoria")
    else:
        st.success("🎓 Capacitación → Opcional")

    st.markdown("---")
    st.success("🏁 SISTEMA COMPLETADO")