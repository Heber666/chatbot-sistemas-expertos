"""
Master Chief - Tutor Virtual (Chatbot con Streamlit + LangChain + OpenAI)
Version 3.0

Cambios respecto a v2.0:
- Streaming: la respuesta del modelo se muestra palabra por palabra en tiempo real.
- Persistencia: el historial se guarda en un archivo local y sobrevive a un refresh
  de la pagina (antes se perdia porque solo vivia en session_state).
- Estilo visual Frutiger Aero, cargado desde styles.css (ver utils.cargar_estilos).
"""

import os
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from utils import cargar_estilos

# ---------------------------------------------------------------------------
# Configuracion inicial
# ---------------------------------------------------------------------------
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error(
        "No se encontro OPENAI_API_KEY. Crea un archivo .env en la raiz del "
        "proyecto (ver .env.example) con tu clave de OpenAI."
    )
    st.stop()

MODELOS_DISPONIBLES = {
    "GPT-4o mini (rapido y economico)": "gpt-4o-mini",
    "GPT-4o (mas capaz, mas costoso)": "gpt-4o",
}

SYSTEM_PROMPT = (
    "Eres un asistente de inteligencia artificial. Tu nombre es Master Chief "
    "y respondes con un tono cercano y natural. Si el usuario pregunta "
    "directamente si eres una IA o un chatbot, responde con honestidad que "
    "si lo eres, sin dejar de mantener tu nombre y personalidad."
)

st.set_page_config(page_title="Master Chief - Tutor Virtual", page_icon="🤖")
cargar_estilos("styles.css")

# ---------------------------------------------------------------------------
# Persistencia: guardar/cargar historial en disco
# ---------------------------------------------------------------------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
HISTORIAL_PATH = DATA_DIR / "historial.json"


def cargar_historial() -> list[dict]:
    """Lee el historial guardado en disco, o devuelve una lista vacia si no existe."""
    if HISTORIAL_PATH.exists():
        try:
            return json.loads(HISTORIAL_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def guardar_historial(mensajes: list[dict]) -> None:
    """Escribe el historial completo a disco."""
    HISTORIAL_PATH.write_text(
        json.dumps(mensajes, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def borrar_historial() -> None:
    if HISTORIAL_PATH.exists():
        HISTORIAL_PATH.unlink()


st.title("Master Chief, tu tutor virtual")
st.caption("Version 3.0 — asistente de IA con respuesta en vivo e historial persistente")

# ---------------------------------------------------------------------------
# Barra lateral: configuracion
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Configuracion")

    modelo_visible = st.selectbox(
        "Modelo de OpenAI",
        options=list(MODELOS_DISPONIBLES.keys()),
        index=0,
    )
    MODEL_NAME = MODELOS_DISPONIBLES[modelo_visible]

    max_historial = st.slider(
        "Mensajes de historial a recordar",
        min_value=2,
        max_value=30,
        value=10,
        step=2,
    )

    if st.button("🗑️ Reiniciar conversacion"):
        st.session_state.messages = []
        borrar_historial()
        st.rerun()

    # Exportar conversacion como texto plano
    if st.session_state.get("messages"):
        texto_exportado = "\n\n".join(
            f"{'Tu' if m['role'] == 'user' else 'Master Chief'}: {m['content']}"
            for m in st.session_state.messages
        )
        st.download_button(
            "⬇️ Descargar conversacion",
            data=texto_exportado,
            file_name="conversacion_master_chief.txt",
            mime="text/plain",
        )

    st.divider()
    st.caption(
        "Este chatbot es un asistente de IA construido con fines academicos. "
        "Las respuestas pueden contener errores. El historial se guarda "
        "localmente y persiste aunque recargues la pagina."
    )

llm = ChatOpenAI(model=MODEL_NAME, temperature=0, api_key=API_KEY)

# ---------------------------------------------------------------------------
# Historial: se carga desde disco la primera vez que arranca la sesion
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = cargar_historial()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------------------------
# Reaccionar a la entrada del usuario
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Escribe tu mensaje..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    guardar_historial(st.session_state.messages)

    historial_recortado = st.session_state.messages[-max_historial:]

    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for m in historial_recortado:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    with st.chat_message("assistant"):
        try:
            # Streaming: llm.stream() devuelve pedazos (chunks) de la respuesta
            # a medida que el modelo los genera, en vez de esperar el texto completo.
            def generar_chunks():
                for chunk in llm.stream(lc_messages):
                    if chunk.content:
                        yield chunk.content

            response = st.write_stream(generar_chunks)
        except Exception as e:
            response = f"Ocurrio un error al contactar al modelo: {e}"
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    guardar_historial(st.session_state.messages)
