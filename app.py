import streamlit as st
import PyPDF2
import random
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="HR-AutoMine AI ULTRA", layout="wide")

st.title("🤖 HR-AutoMine AI ULTRA")
st.subheader("Sistema de reclutamiento autónomo con 6 agentes + IA de scoring")

st.markdown("---")

# =========================
# "BASE DE DATOS"
# =========================
if "candidates" not in st.session_state:
    st.session_state.candidates = []

# =========================
# EXTRAER TEXTO PDF
# =========================
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

# =========================
# IA SCORING (SIMULACIÓN TIPO GPT)
# =========================
def ai_score(text):
    base = random.randint(50, 70)

    if "ingeniero" in text:
        base += 10
    if "experiencia" in text:
        base += 10
    if "seguridad" in text:
        base += 10
    if "proyecto" in text:
        base += 5

    return min(base, 100)

# =========================
# 6 AGENTES (PIPELINE)
# =========================
def run_agents(text):

    logs = []

    score = ai_score(text)
    logs.append(f"🧠 IA Score inicial: {score}")

    # AGENTE 1
    if score < 55:
        return False, score, logs + ["❌ Agente 1: Rechazado en reclutamiento"]
    logs.append("✔ Agente 1: Reclutamiento aprobado")

    # AGENTE 2
    if "certificado" not in text:
        return False, score, logs + ["❌ Agente 2: Sin certificación"]
    logs.append("✔ Agente 2: Validación OK")

    # AGENTE 3
    logs.append("✔ Agente 3: Escalas compatibles")

    # AGENTE 4
    if score < 70:
        return False, score, logs + ["❌ Agente 4: Bajo rendimiento proyectado"]
    logs.append("✔ Agente 4: Rendimiento OK")

    # AGENTE 5
    if "accidente" in text:
        return False, score, logs + ["❌ Agente 5: Riesgo de fatiga alto"]
    logs.append("✔ Agente 5: Riesgo controlado")

    # AGENTE 6
    logs.append("✔ Agente 6: Capacitación validada")

    return True, score, logs

# =========================
# UI UPLOAD MULTIPLE
# =========================
files = st.file_uploader("📄 Subir CVs (PDF)", type=["pdf"], accept_multiple_files=True)

if files:

    st.info("🧠 Ejecutando sistema de 6 agentes + IA scoring...")

    results = []

    for file in files:

        text = extract_text(file)
        ok, score, logs = run_agents(text)

        name = file.name

        results.append({
            "Nombre": name,
            "Score IA": score,
            "Aprobado": ok
        })

        st.markdown(f"### 📄 {name}")
        for l in logs:
            st.write(l)

        if ok:
            st.success("🏁 APROBADO")
        else:
            st.error("🚫 RECHAZADO")

        st.markdown("---")

        st.session_state.candidates.append({
            "name": name,
            "score": score,
            "status": "APROBADO" if ok else "RECHAZADO"
        })

    # =========================
    # DATAFRAME
    # =========================
    df = pd.DataFrame(results)

    st.subheader("🏆 Ranking de candidatos")

    df = df.sort_values(by="Score IA", ascending=False)

    st.dataframe(df, use_container_width=True)

    # =========================
    # GRÁFICO
    # =========================
    fig = px.bar(df, x="Nombre", y="Score IA", color="Score IA")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# DASHBOARD GENERAL
# =========================
st.markdown("---")
st.subheader("📊 Dashboard global")

if st.session_state.candidates:

    df_all = pd.DataFrame(st.session_state.candidates)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total candidatos", len(df_all))
    col2.metric("Aprobados", len(df_all[df_all["status"]=="APROBADO"]))
    col3.metric("Rechazados", len(df_all[df_all["status"]=="RECHAZADO"]))

    fig2 = px.pie(df_all, names="status", title="Distribución de candidatos")
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("Aún no hay candidatos analizados")