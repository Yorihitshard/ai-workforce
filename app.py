import streamlit as st
import time
import json
import base64
import anthropic

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HR AutoMine AI",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=Exo+2:wght@300;400;500;600;700&display=swap');

:root {
  --bg:        #070b12;
  --bg2:       #0d1420;
  --bg3:       #111b2e;
  --card:      #0f1929;
  --border:    #1e3050;
  --gold:      #f5a623;
  --gold2:     #ffcc44;
  --cyan:      #00d4ff;
  --cyan2:     #00fff7;
  --red:       #ff3b5c;
  --green:     #00e676;
  --text:      #e8edf5;
  --muted:     #6b7f9e;
  --pass:      #00e676;
  --fail:      #ff3b5c;
}

/* ── Base ── */
html, body, [data-testid="stApp"] {
  background: var(--bg) !important;
  font-family: 'Exo 2', sans-serif;
  color: var(--text);
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }

/* ── Remove streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO ── */
.hero {
  position: relative;
  min-height: 340px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 20px 40px;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 50% 0%, rgba(0,212,255,0.12) 0%, transparent 70%),
    radial-gradient(ellipse 60% 40% at 80% 100%, rgba(245,166,35,0.08) 0%, transparent 60%),
    linear-gradient(180deg, #070b12 0%, #0d1420 100%);
}
.hero-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 90% 90% at center, black 20%, transparent 80%);
}
.hero-badge {
  position: relative;
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(0,212,255,0.08);
  border: 1px solid rgba(0,212,255,0.25);
  border-radius: 40px;
  padding: 6px 18px;
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--cyan);
  text-transform: uppercase;
  margin-bottom: 24px;
}
.hero-badge::before {
  content: '';
  width: 7px; height: 7px;
  background: var(--cyan);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--cyan);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

.hero-title {
  position: relative;
  font-family: 'Rajdhani', sans-serif;
  font-size: clamp(42px, 7vw, 88px);
  font-weight: 700;
  line-height: 0.95;
  margin: 0 0 10px;
  letter-spacing: -1px;
}
.hero-title span.gold { color: var(--gold); }
.hero-title span.cyan { color: var(--cyan); }
.hero-sub {
  position: relative;
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  letter-spacing: 4px;
  color: var(--muted);
  text-transform: uppercase;
  margin-bottom: 16px;
}
.hero-desc {
  position: relative;
  max-width: 580px;
  font-size: 15px;
  color: #8fa3bf;
  line-height: 1.7;
  margin: 0 auto 32px;
}

/* ── Stats row ── */
.stats-row {
  display: flex; gap: 0;
  justify-content: center;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--card);
  position: relative;
  max-width: 700px;
  margin: 0 auto;
}
.stat-item {
  flex: 1;
  padding: 16px 24px;
  text-align: center;
  border-right: 1px solid var(--border);
  position: relative;
}
.stat-item:last-child { border-right: none; }
.stat-val {
  font-family: 'Rajdhani', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--gold);
}
.stat-label {
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  letter-spacing: 1.5px;
  color: var(--muted);
  text-transform: uppercase;
  margin-top: 2px;
}

/* ── Section ── */
.section {
  padding: 48px 40px;
  max-width: 1200px;
  margin: 0 auto;
}
.section-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 13px;
  letter-spacing: 4px;
  color: var(--cyan);
  text-transform: uppercase;
  margin-bottom: 8px;
}
.section-heading {
  font-family: 'Rajdhani', sans-serif;
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 8px;
}
.section-sub {
  color: var(--muted);
  font-size: 14px;
  margin-bottom: 36px;
}

/* ── Upload box ── */
.upload-box {
  background: var(--card);
  border: 2px dashed var(--border);
  border-radius: 16px;
  padding: 48px 32px;
  text-align: center;
  transition: border-color 0.3s;
  margin-bottom: 32px;
}
.upload-box:hover { border-color: var(--cyan); }
.upload-icon { font-size: 52px; margin-bottom: 16px; }
.upload-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 22px; font-weight: 600;
  margin-bottom: 8px;
}
.upload-hint { color: var(--muted); font-size: 13px; }

/* ── Pipeline ── */
.pipeline-wrap {
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* ── Agent card ── */
.agent-card {
  display: flex; gap: 20px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px 28px;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}
.agent-card.active {
  border-color: var(--cyan);
  box-shadow: 0 0 30px rgba(0,212,255,0.1);
}
.agent-card.passed {
  border-color: var(--green);
  box-shadow: 0 0 20px rgba(0,230,118,0.08);
}
.agent-card.failed {
  border-color: var(--red);
  box-shadow: 0 0 20px rgba(255,59,92,0.08);
}
.agent-card.waiting { opacity: 0.45; }
.agent-card::before {
  content: '';
  position: absolute; left: 0; top: 0; bottom: 0;
  width: 3px;
  background: var(--border);
  transition: background 0.3s;
}
.agent-card.active::before { background: var(--cyan); }
.agent-card.passed::before { background: var(--green); }
.agent-card.failed::before { background: var(--red); }

.agent-num {
  width: 52px; height: 52px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  font-family: 'Space Mono', monospace;
  font-size: 14px; font-weight: 700;
  color: var(--muted);
  position: relative;
}
.agent-num.active-num { color: var(--cyan); border-color: var(--cyan); background: rgba(0,212,255,0.08); }
.agent-num.pass-num  { color: var(--green); border-color: var(--green); background: rgba(0,230,118,0.08); }
.agent-num.fail-num  { color: var(--red); border-color: var(--red); background: rgba(255,59,92,0.08); }

.agent-body { flex: 1; }
.agent-name {
  font-family: 'Rajdhani', sans-serif;
  font-size: 20px; font-weight: 700;
  margin-bottom: 2px;
}
.agent-role {
  font-family: 'Space Mono', monospace;
  font-size: 10px; letter-spacing: 2px;
  color: var(--muted); text-transform: uppercase;
  margin-bottom: 12px;
}
.agent-result {
  font-size: 14px;
  line-height: 1.7;
  color: #aabbd4;
  background: var(--bg2);
  border-radius: 8px;
  padding: 12px 16px;
  margin-top: 10px;
  border-left: 3px solid var(--border);
}
.agent-result.res-pass { border-left-color: var(--green); color: #c8ffe8; }
.agent-result.res-fail { border-left-color: var(--red); color: #ffd0d8; }

.badge-status {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 12px; border-radius: 20px;
  font-family: 'Space Mono', monospace;
  font-size: 10px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase;
  margin-left: 10px;
}
.badge-pass { background: rgba(0,230,118,0.12); color: var(--green); border: 1px solid rgba(0,230,118,0.3); }
.badge-fail { background: rgba(255,59,92,0.12); color: var(--red); border: 1px solid rgba(255,59,92,0.3); }
.badge-proc { background: rgba(0,212,255,0.12); color: var(--cyan); border: 1px solid rgba(0,212,255,0.3); animation: pulse 1.5s infinite; }

/* ── Connector ── */
.connector {
  width: 2px; height: 24px; margin: 0 auto;
  background: linear-gradient(var(--border), var(--border));
}
.connector.con-pass { background: var(--green); }
.connector.con-fail { background: var(--red); }

/* ── Final verdict ── */
.verdict-box {
  border-radius: 16px;
  padding: 32px 36px;
  text-align: center;
  margin-top: 24px;
  border: 1px solid var(--border);
}
.verdict-box.v-pass {
  background: linear-gradient(135deg, rgba(0,230,118,0.08), rgba(0,230,118,0.03));
  border-color: var(--green);
  box-shadow: 0 0 60px rgba(0,230,118,0.12);
}
.verdict-box.v-fail {
  background: linear-gradient(135deg, rgba(255,59,92,0.08), rgba(255,59,92,0.03));
  border-color: var(--red);
  box-shadow: 0 0 60px rgba(255,59,92,0.12);
}
.verdict-icon { font-size: 56px; margin-bottom: 16px; }
.verdict-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 32px; font-weight: 700;
  margin-bottom: 12px;
}
.verdict-body { color: #8fa3bf; font-size: 15px; line-height: 1.7; max-width: 600px; margin: 0 auto; }

/* ── Processing animation ── */
.thinking-dots::after {
  content: '...';
  animation: dots 1.5s steps(4,end) infinite;
}
@keyframes dots {
  0%,20%{ content: '.' }
  40%{ content: '..' }
  60%,100%{ content: '...' }
}

/* ── CTA button ── */
.stButton > button {
  background: linear-gradient(135deg, var(--gold), #e8920f) !important;
  color: #070b12 !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 14px 36px !important;
  width: 100% !important;
  transition: all 0.3s !important;
  box-shadow: 0 4px 24px rgba(245,166,35,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(245,166,35,0.45) !important;
}

/* Uploader */
[data-testid="stFileUploader"] {
  background: transparent !important;
}
[data-testid="stFileUploader"] > div {
  background: var(--card) !important;
  border: 2px dashed var(--border) !important;
  border-radius: 14px !important;
  padding: 32px !important;
  transition: border-color 0.3s !important;
}
[data-testid="stFileUploader"] > div:hover {
  border-color: var(--cyan) !important;
}
[data-testid="stFileUploaderDropzoneInput"] { display: none; }

/* Progress */
[data-testid="stProgress"] > div > div {
  background: var(--cyan) !important;
}

/* Divider */
hr { border-color: var(--border) !important; margin: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Agent definitions ───────────────────────────────────────────────────────────
AGENTS = [
    {
        "id": 1,
        "icon": "🔍",
        "name": "Agente de Reclutamiento Inteligente",
        "role": "Screening & Compatibilidad de Perfil",
        "desc": "Analiza datos básicos: experiencia, formación académica y sectores previos. Filtra candidatos incompatibles con el entorno minero.",
        "system": """Eres el Agente 1 de HR-AutoMine AI: Reclutamiento Inteligente para minería peruana.
Analiza el CV y evalúa:
- ¿Tiene experiencia laboral relevante (mínimo mencionar algún trabajo)?
- ¿Su formación académica o técnica es compatible con industria extractiva, construcción, manufactura, logística o afines?
- ¿Es peruano o tiene permiso de trabajo en Perú (inferir si es posible)?
- ¿El perfil básico es coherente y no está vacío?

Responde SOLO en JSON con este formato exacto:
{"aprobado": true/false, "puntaje": número_del_1_al_100, "razon": "explicación detallada en 3-4 oraciones de por qué aprueba o no, qué encontraste en el CV y qué criterios evaluaste"}"""
    },
    {
        "id": 2,
        "icon": "📋",
        "name": "Agente de Evaluación y Validación",
        "role": "Certificaciones & Requisitos Técnicos Mineros",
        "desc": "Verifica certificaciones obligatorias para el sector minero: seguridad, manejo de equipos, IPERC, primeros auxilios.",
        "system": """Eres el Agente 2 de HR-AutoMine AI: Evaluación y Validación Técnica para minería peruana.
Analiza el CV y evalúa:
- ¿Tiene certificaciones de seguridad (IPERC, ATS, PETS, SSMA, SCTR o equivalentes)?
- ¿Menciona cursos o conocimiento en normativas mineras peruanas (Reglamento de Seguridad Minera D.S. 024)?
- ¿Tiene entrenamiento en primeros auxilios o manejo de emergencias?
- ¿Sus habilidades técnicas son verificables y coherentes con minería o industrias afines?

Responde SOLO en JSON con este formato exacto:
{"aprobado": true/false, "puntaje": número_del_1_al_100, "razon": "explicación detallada en 3-4 oraciones evaluando certificaciones encontradas o ausentes, su importancia en el sector minero y recomendaciones"}"""
    },
    {
        "id": 3,
        "icon": "📅",
        "name": "Agente de Planificación y Cobertura Operativa",
        "role": "Disponibilidad & Turnos de Trabajo",
        "desc": "Evalúa disponibilidad para turnos rotativos, trabajo en zonas remotas y capacidad de adaptación a condiciones de campo minero.",
        "system": """Eres el Agente 3 de HR-AutoMine AI: Planificación y Cobertura Operativa para minería peruana.
Analiza el CV y evalúa:
- ¿Ha trabajado en zonas remotas, campamentos o fuera de su ciudad de origen?
- ¿Tiene experiencia con regímenes de trabajo 14x7, 21x7, o turnos rotativos (diurno/nocturno)?
- ¿Muestra flexibilidad geográfica para trabajar en regiones andinas (Cajamarca, Ancash, Cusco, Puno, etc.)?
- ¿Su historial laboral muestra estabilidad o alta rotación injustificada?

Responde SOLO en JSON con este formato exacto:
{"aprobado": true/false, "puntaje": número_del_1_al_100, "razon": "explicación detallada en 3-4 oraciones sobre disponibilidad operativa detectada, patrones de movilidad laboral y compatibilidad con el régimen minero peruano"}"""
    },
    {
        "id": 4,
        "icon": "📈",
        "name": "Agente de Rendimiento y OKRs",
        "role": "Productividad & Logros Cuantificables",
        "desc": "Mide si el candidato demuestra resultados concretos, métricas de producción y orientación a objetivos en su historial profesional.",
        "system": """Eres el Agente 4 de HR-AutoMine AI: Evaluación de Rendimiento y OKRs para minería peruana.
Analiza el CV y evalúa:
- ¿El candidato incluye logros cuantificables (toneladas procesadas, % mejora, proyectos completados, equipos a cargo)?
- ¿Menciona KPIs de productividad o eficiencia en sus roles anteriores?
- ¿Demuestra progresión de carrera y asunción de responsabilidades crecientes?
- ¿Su historial sugiere orientación a resultados o roles meramente pasivos?

Responde SOLO en JSON con este formato exacto:
{"aprobado": true/false, "puntaje": número_del_1_al_100, "razon": "explicación detallada en 3-4 oraciones sobre los logros detectados, nivel de orientación a resultados del candidato y su potencial de contribución operativa"}"""
    },
    {
        "id": 5,
        "icon": "🧠",
        "name": "Agente de Fatiga, Salud y Bienestar",
        "role": "Aptitud Física & Riesgo de Fatiga Laboral",
        "desc": "Analiza indicadores de salud ocupacional, carga laboral previa y factores de riesgo para operar en altura y condiciones extremas.",
        "system": """Eres el Agente 5 de HR-AutoMine AI: Evaluación de Fatiga, Salud y Bienestar para minería peruana.
Analiza el CV y evalúa:
- ¿El candidato menciona haber trabajado a gran altitud (>3,000 msnm) o en condiciones climáticas extremas?
- ¿Ha tenido historial de múltiples empleos simultáneos que sugieran sobrecarga laboral crónica?
- ¿Menciona actividades físicas, deportes o hábitos de bienestar que indiquen buena condición física?
- ¿Su historial muestra periodos de descanso razonables o patrones de trabajo insostenibles?

Responde SOLO en JSON con este formato exacto:
{"aprobado": true/false, "puntaje": número_del_1_al_100, "razon": "explicación detallada en 3-4 oraciones sobre aptitud física estimada, factores de riesgo de fatiga detectados y compatibilidad con trabajo en altura en el sector minero peruano"}"""
    },
    {
        "id": 6,
        "icon": "🎓",
        "name": "Agente de Capacitación y Mejora Continua",
        "role": "Desarrollo Profesional & Brecha de Habilidades",
        "desc": "Detecta brechas de formación, potencial de aprendizaje y alineación del perfil con las necesidades de capacitación del sector.",
        "system": """Eres el Agente 6 de HR-AutoMine AI: Evaluación de Capacitación y Mejora Continua — el agente final y decisor.
Analiza el CV completo y evalúa:
- ¿El candidato muestra hábito de formación continua (cursos, diplomados, especializaciones recientes)?
- ¿Qué brechas de habilidades detectas comparado con el perfil ideal minero peruano?
- ¿Tiene potencial de desarrollo a mediano plazo en el sector?
- Considerando todo el perfil: ¿Es un candidato apto para el sector minero peruano?

Como agente final, emite el veredicto definitivo del sistema HR-AutoMine AI.
Responde SOLO en JSON con este formato exacto:
{"aprobado": true/false, "puntaje": número_del_1_al_100, "razon": "veredicto final detallado en 4-5 oraciones que sintetiza el perfil completo, menciona las fortalezas y debilidades clave, brechas de capacitación identificadas y la conclusión definitiva sobre si el candidato es apto para el sector minero peruano"}"""
    },
]


# ── Utility ─────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from PDF using PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except ImportError:
        # Fallback: send as base64 to Claude vision if needed
        return None
    except Exception as e:
        return None


def call_agent(agent: dict, cv_text: str) -> dict:
    """Call Claude API for a specific agent."""
    client = anthropic.Anthropic()

    user_msg = f"""Analiza el siguiente CV para el proceso de selección de HR-AutoMine AI (minería peruana):

=== CV DEL CANDIDATO ===
{cv_text[:8000]}
========================

Evalúa según tus criterios específicos como {agent['name']}."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=agent["system"],
            messages=[{"role": "user", "content": user_msg}]
        )

        raw = response.content[0].text.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw.strip())
        return result
    except json.JSONDecodeError:
        # Fallback parse
        approved = "aprobado" in raw.lower() and ("true" in raw.lower() or '"aprobado": true' in raw)
        return {
            "aprobado": approved,
            "puntaje": 50,
            "razon": raw[:400] if raw else "Error al procesar respuesta del agente."
        }
    except Exception as e:
        return {
            "aprobado": False,
            "puntaje": 0,
            "razon": f"Error de comunicación con el agente: {str(e)}"
        }


# ── Render functions ─────────────────────────────────────────────────────────────

def render_hero():
    st.markdown("""
    <div class="hero">
      <div class="hero-grid"></div>
      <div class="hero-badge">⛏️ &nbsp; Sistema Autónomo de RRHH · Minería Peruana</div>
      <div class="hero-title">
        HR <span class="gold">AUTO</span><span class="cyan">MINE</span><br>
        <span style="font-size:0.6em; letter-spacing:6px; color:#8fa3bf; font-weight:400;">ARTIFICIAL INTELLIGENCE</span>
      </div>
      <div class="hero-desc">
        Sistema de 6 agentes de IA que evalúa curricula de forma autónoma y secuencial.
        Cada agente filtra según criterios especializados del sector minero peruano.
      </div>
      <div class="stats-row">
        <div class="stat-item">
          <div class="stat-val">6</div>
          <div class="stat-label">Agentes IA</div>
        </div>
        <div class="stat-item">
          <div class="stat-val">−38%</div>
          <div class="stat-label">Accidentes fatiga</div>
        </div>
        <div class="stat-item">
          <div class="stat-val">94%</div>
          <div class="stat-label">Eficiencia</div>
        </div>
        <div class="stat-item">
          <div class="stat-val">51</div>
          <div class="stat-label">Proyectos mineros</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_agent_card(agent, status="waiting", result=None):
    """Render a single agent card with its status."""
    card_class = f"agent-card {status}"
    num_class  = {"waiting": "", "active": "active-num", "passed": "pass-num", "failed": "fail-num"}.get(status, "")

    badge_html = ""
    if status == "active":
        badge_html = '<span class="badge-status badge-proc">⚡ Analizando</span>'
    elif status == "passed":
        badge_html = f'<span class="badge-status badge-pass">✓ Aprobado · {result.get("puntaje", 0)}pts</span>'
    elif status == "failed":
        badge_html = f'<span class="badge-status badge-fail">✗ Rechazado · {result.get("puntaje", 0)}pts</span>'

    result_html = ""
    if result and status in ("passed", "failed"):
        res_class = "res-pass" if status == "passed" else "res-fail"
        arrow = "✅" if status == "passed" else "❌"
        result_html = f'<div class="agent-result {res_class}">{arrow} {result.get("razon","")}</div>'

    html = f"""
    <div class="{card_class}">
      <div class="agent-num {num_class}">{agent['icon']}</div>
      <div class="agent-body">
        <div style="display:flex; align-items:center; flex-wrap:wrap; gap:4px;">
          <span class="agent-name">Agente {agent['id']} · {agent['name']}</span>
          {badge_html}
        </div>
        <div class="agent-role">{agent['role']}</div>
        <div style="font-size:13px; color:var(--muted);">{agent['desc']}</div>
        {result_html}
      </div>
    </div>
    """
    return html


def render_verdict(results: list, agents: list):
    """Render the final verdict box."""
    last_result = results[-1]
    approved_count = sum(1 for r in results if r.get("aprobado"))
    total_score = sum(r.get("puntaje", 0) for r in results) // len(results)
    final_approved = last_result.get("aprobado", False)

    if final_approved:
        st.markdown(f"""
        <div class="verdict-box v-pass">
          <div class="verdict-icon">🏆</div>
          <div class="verdict-title" style="color:var(--green);">CANDIDATO APROBADO</div>
          <div style="display:flex; gap:20px; justify-content:center; margin:16px 0;">
            <span class="badge-status badge-pass">✓ {approved_count}/{len(results)} Agentes Aprobados</span>
            <span class="badge-status badge-pass">⭐ Score Final: {total_score}/100</span>
          </div>
          <div class="verdict-body">{last_result.get('razon','')}</div>
          <div style="margin-top:20px; font-family:'Space Mono',monospace; font-size:11px; color:var(--muted); letter-spacing:2px;">
            PERFIL COMPATIBLE CON EL SECTOR MINERO PERUANO · HR-AUTOMINE AI
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        agent_stopped = len(results)
        st.markdown(f"""
        <div class="verdict-box v-fail">
          <div class="verdict-icon">🚫</div>
          <div class="verdict-title" style="color:var(--red);">CANDIDATO NO SELECCIONADO</div>
          <div style="display:flex; gap:20px; justify-content:center; margin:16px 0;">
            <span class="badge-status badge-fail">✗ Detenido en Agente {agent_stopped}</span>
            <span class="badge-status badge-fail">📊 Score: {total_score}/100</span>
          </div>
          <div class="verdict-body">{last_result.get('razon','')}</div>
          <div style="margin-top:20px; font-family:'Space Mono',monospace; font-size:11px; color:var(--muted); letter-spacing:2px;">
            PERFIL INCOMPATIBLE CON EL SECTOR MINERO PERUANO · HR-AUTOMINE AI
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    render_hero()

    st.markdown('<hr style="border-color:#1e3050; margin:0;">', unsafe_allow_html=True)

    # ── Upload section ──
    st.markdown("""
    <div class="section">
      <div class="section-title">// Carga de Currículo</div>
      <div class="section-heading">Evaluación de Candidatos</div>
      <div class="section-sub">Sube el CV en PDF. Los 6 agentes lo analizarán de forma autónoma y secuencial.</div>
    </div>
    """, unsafe_allow_html=True)

    col_upload, col_info = st.columns([3, 2], gap="large")

    with col_upload:
        st.markdown('<div style="padding: 0 40px;">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "📄 Arrastra el CV aquí o haz clic para seleccionar",
            type=["pdf"],
            help="Formato PDF · Tamaño máximo 10MB"
        )

        if uploaded_file:
            st.markdown(f"""
            <div style="background:rgba(0,230,118,0.06); border:1px solid rgba(0,230,118,0.2);
                        border-radius:10px; padding:14px 18px; margin:12px 0;
                        display:flex; align-items:center; gap:10px;">
              <span style="font-size:20px;">📄</span>
              <div>
                <div style="font-family:'Rajdhani',sans-serif; font-weight:600; font-size:16px;">{uploaded_file.name}</div>
                <div style="font-family:'Space Mono',monospace; font-size:10px; color:var(--muted); letter-spacing:1px;">
                  {uploaded_file.size // 1024} KB · PDF · LISTO PARA ANALIZAR
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        analyze_btn = st.button("⚡ INICIAR EVALUACIÓN CON 6 AGENTES IA", disabled=not uploaded_file)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div style="padding: 0 20px 0 0; margin-top: 8px;">
          <div style="background:var(--card); border:1px solid var(--border); border-radius:14px; padding:24px;">
            <div style="font-family:'Space Mono',monospace; font-size:10px; letter-spacing:2px;
                        color:var(--cyan); text-transform:uppercase; margin-bottom:16px;">
              Pipeline de Evaluación
            </div>
        """, unsafe_allow_html=True)

        for i, ag in enumerate(AGENTS):
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:10px 0;
                        border-bottom: 1px solid {'var(--border)' if i < len(AGENTS)-1 else 'transparent'};">
              <div style="width:32px; height:32px; background:var(--bg2); border:1px solid var(--border);
                          border-radius:8px; display:flex; align-items:center; justify-content:center;
                          font-size:16px; flex-shrink:0;">{ag['icon']}</div>
              <div>
                <div style="font-family:'Rajdhani',sans-serif; font-weight:600; font-size:14px;">
                  Agente {ag['id']}
                </div>
                <div style="font-family:'Space Mono',monospace; font-size:9px; color:var(--muted);
                            letter-spacing:1px;">{ag['role']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Pipeline section ──
    st.markdown('<hr style="border-color:#1e3050;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 40px 40px 16px;">
      <div class="section-title">// Análisis en Tiempo Real</div>
      <div class="section-heading">Pipeline de Evaluación</div>
      <div class="section-sub">Cada agente analiza el CV y decide si el candidato avanza al siguiente filtro.</div>
    </div>
    """, unsafe_allow_html=True)

    pipeline_container = st.container()

    # Initial pipeline display (all waiting)
    with pipeline_container:
        agent_placeholders = []
        verdict_placeholder = st.empty()

        cols = st.columns([1, 10, 1])
        with cols[1]:
            for i, agent in enumerate(AGENTS):
                ph = st.empty()
                ph.markdown(render_agent_card(agent, "waiting"), unsafe_allow_html=True)
                agent_placeholders.append(ph)

    # ── Run analysis ──
    if analyze_btn and uploaded_file:
        uploaded_file.seek(0)
        cv_text = extract_text_from_pdf(uploaded_file)

        if not cv_text or len(cv_text.strip()) < 50:
            st.error("⚠️ No se pudo extraer texto del PDF. Asegúrate de que no sea un PDF escaneado sin OCR.")
            return

        results = []
        progress_bar = st.progress(0, text="Iniciando análisis autónomo...")

        with st.columns([1, 10, 1])[1]:
            for i, agent in enumerate(AGENTS):
                # Mark as active
                agent_placeholders[i].markdown(
                    render_agent_card(agent, "active"), unsafe_allow_html=True
                )
                progress_bar.progress(
                    (i) / len(AGENTS),
                    text=f"Agente {i+1}/6 analizando: {agent['name']}..."
                )

                # Call API
                result = call_agent(agent, cv_text)
                results.append(result)

                approved = result.get("aprobado", False)
                status = "passed" if approved else "failed"

                # Update card with result
                agent_placeholders[i].markdown(
                    render_agent_card(agent, status, result), unsafe_allow_html=True
                )

                progress_bar.progress(
                    (i + 1) / len(AGENTS),
                    text=f"Agente {i+1} completado · {'✓ Aprobado' if approved else '✗ Rechazado'}"
                )

                time.sleep(0.4)

                # If failed and not the last agent, stop pipeline
                if not approved and i < len(AGENTS) - 1:
                    # Mark remaining as waiting/skipped
                    for j in range(i + 1, len(AGENTS)):
                        agent_placeholders[j].markdown(f"""
                        <div class="agent-card waiting">
                          <div class="agent-num">{AGENTS[j]['icon']}</div>
                          <div class="agent-body">
                            <div class="agent-name" style="opacity:0.5;">Agente {AGENTS[j]['id']} · {AGENTS[j]['name']}</div>
                            <div class="agent-role">{AGENTS[j]['role']}</div>
                            <div style="font-size:12px; color:var(--muted); margin-top:8px; font-style:italic;">
                              ⏭️ Evaluación detenida — candidato no avanzó al siguiente agente
                            </div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    break

        progress_bar.progress(1.0, text="✅ Análisis completado")
        time.sleep(0.5)
        progress_bar.empty()

        # Final verdict
        st.markdown('<div style="padding: 0 40px 60px;">', unsafe_allow_html=True)
        render_verdict(results, AGENTS)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div style="border-top: 1px solid var(--border); padding: 32px 40px; text-align:center;">
      <div style="font-family:'Rajdhani',sans-serif; font-size:20px; font-weight:700; margin-bottom:6px;">
        HR <span style="color:var(--gold);">AUTO</span><span style="color:var(--cyan);">MINE</span>
        <span style="color:var(--muted); font-size:14px; font-weight:400;"> · Artificial Intelligence</span>
      </div>
      <div style="font-family:'Space Mono',monospace; font-size:10px; color:var(--muted); letter-spacing:2px;">
        UNIVERSIDAD CÉSAR VALLEJO · SISTEMA AUTÓNOMO DE GESTIÓN DE RRHH MINERO · PERÚ 2026
      </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
