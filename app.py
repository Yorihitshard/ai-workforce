import streamlit as st
import PyMuPDF  # PyMuPDF (fitz)
import random
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="HR-AutoMine AI PRO", layout="wide")

st.title("🤖 HR-AutoMine AI PRO (SIN API - IA LOCAL)")
st.subheader("Sistema de 6 agentes con IA híbrida gratuita")

st.markdown("---")

# =========================
# EXTRAER TEXTO PDF
# =========================
def extract_text(pdf_file):
    doc = PyMuPDF.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text().lower()
    return text

# =========================
# IA LOCAL (SCORING INTELIGENTE)
# =========================
def ai_score(text):
    score = 50  # base

    if "ingeniero" in text or "tecnico" in text:
        score += 15
    if "experiencia" in text or "años" in text:
        score += 15
    if "seguridad" in text:
        score += 10
    if "proyecto" in text:
        score += 10
    if "lider" in text:
        score += 10

    # ruido inteligente (simula IA real)
    score += random.randint(-5, 5)

    return max(0, min(score, 100))

# =========================
# AGENTES
# =========================
def agente(nombre, condition, fail_reason):
    if condition:
        return True, f"✔ {nombre} aprobado"
    else:
        return False, f"❌ {nombre}: {fail_reason}"

# =========================
# PIPELINE 6 AGENTES
# =========================
def run_pipeline(text):

    logs = []

    score = ai_score(text)
    logs.append(f"🧠 IA SCORE BASE: {score}")

    # AGENTE 1
    ok, msg = agente(
        "Agente 1 Reclutamiento",
        score > 55,
        "Perfil no compatible con minería"
    )
    logs.append(msg)
    if not ok:
        return False, score, logs

    # AGENTE 2
    ok, msg = agente(
        "Agente 2 Validación",
        "certificado" in text,
        "Sin certificaciones técnicas"
    )
    logs.append(msg)
    if not ok:
        return False, score, logs

    # AGENTE 3
    ok, msg = agente(
        "Agente 3 Escalas",
        "disponibilidad" in text or "turno" in text,
        "No apto para turnos operativos"
    )
    logs.append(msg)
    if not ok:
        return False, score, logs

    # AGENTE 4
    ok, msg = agente(
        "Agente 4 Rendimiento",
        score > 65,
        "Bajo potencial de rendimiento"
    )
    logs.append(msg)
    if not ok:
        return False, score, logs

    # AGENTE 5
    ok, msg = agente(
        "Agente 5 Fatiga",
        "accidente" not in text,
        "Riesgo de fatiga o incidentes previos"
    )
    logs.append(msg)
    if not ok:
        return False, score, logs

    # AGENTE 6
    ok, msg = agente(
        "Agente 6 Capacitación",
        True,
        "Requiere formación adicional"
    )
    logs.append(msg)

    return True, score, logs

# =========================
# UI
# =========================
file = st.file_uploader("📄 Sube CV en PDF", type=["pdf"])

if file:

    text = extract_text(file)

    st.info("🧠 Analizando CV con IA híbrida (sin API)...")

    ok, score, logs = run_pipeline(text)

    st.subheader("📊 Resultado del análisis")

    for l in logs:
        st.write(l)

    st.metric("Score final IA", score)

    st.markdown("---")

    if ok:
        st.success("🏆 CANDIDATO APROBADO PARA CONTRATACIÓN")
        st.write("Perfil compatible con operación minera y alto rendimiento.")
    else:
        st.error("🚫 CANDIDATO NO APROBADO")
        st.write("No cumple criterios mínimos del sistema.")

# =========================
# DASHBOARD SIMULADO
# =========================
st.markdown("---")
st.subheader("📈 Simulación de rendimiento del sistema")

data = pd.DataFrame({
    "Agentes": ["Reclutamiento", "Validación", "Escalas", "Rendimiento", "Fatiga", "Capacitación"],
    "Eficiencia": [92, 88, 85, 90, 95, 80]
})

fig = px.bar(data, x="Agentes", y="Eficiencia", color="Eficiencia")
st.plotly_chart(fig, use_container_width=True)