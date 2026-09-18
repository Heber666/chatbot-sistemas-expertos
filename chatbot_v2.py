"""
Master Chief - Tutor Virtual (Chatbot con Streamlit + LangChain + OpenAI)
Version 2.0

Cambios respecto a v1.0:
- El bot ya no niega ser una IA cuando se le pregunta directamente (transparencia).
- Selector de modelo desde la barra lateral.
- Limite configurable de mensajes de historial que se reenvian al modelo (control de costo).
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ---------------------------------------------------------------------------
# Configuracion inicial
# ---------------------------------------------------------------------------
load_dotenv()  # Carga las variables definidas en el archivo .env

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error(
        "No se encontro OPENAI_API_KEY. Crea un archivo .env en la raiz del "
        "proyecto (ver .env.example) con tu clave de OpenAI."
    )
    st.stop()

# Modelos disponibles para elegir desde la UI (nombre visible -> modelo real de OpenAI)
MODELOS_DISPONIBLES = {
    "GPT-4o mini (rapido y economico)": "gpt-4o-mini",
    "GPT-4o (mas capaz, mas costoso)": "gpt-4o",
}

# Mejora 1: el prompt ya NO instruye a negar ser una IA.
# Se mantiene la personalidad/nombre, pero con honestidad si preguntan.
SYSTEM_PROMPT = (
    "Eres un asistente de inteligencia artificial. Tu nombre es Master Chief "
    "y respondes con un tono cercano y natural. Si el usuario pregunta "
    "directamente si eres una IA o un chatbot, responde con honestidad que "
    "si lo eres, sin dejar de mantener tu nombre y personalidad."
)

st.set_page_config(page_title="Master Chief - Tutor Virtual", page_icon="🤖")
st.title("Master Chief, tu tutor virtual")
st.caption("Version 2.0 — asistente de IA (no un humano) que mantiene el historial de la conversacion")

# ---------------------------------------------------------------------------
# Barra lateral: configuracion (Mejora 2 y 3)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Configuracion")

    modelo_visible = st.selectbox(
        "Modelo de OpenAI",
        options=list(MODELOS_DISPONIBLES.keys()),
        index=0,
        help="GPT-4o mini es suficiente para la mayoria de los casos y mucho mas barato.",
    )
    MODEL_NAME = MODELOS_DISPONIBLES[modelo_visible]

    max_historial = st.slider(
        "Mensajes de historial a recordar",
        min_value=2,
        max_value=30,
        value=10,
        step=2,
        help=(
            "Cuantos mensajes recientes se reenvian al modelo como contexto. "
            "Un numero mas alto da mas memoria, pero cuesta mas por cada turno."
        ),
    )

    if st.button("🗑️ Reiniciar conversacion"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(
        "Este chatbot es un asistente de IA construido con fines academicos. "
        "Las respuestas pueden contener errores."
    )

llm = ChatOpenAI(model=MODEL_NAME, temperature=0, api_key=API_KEY)

# ---------------------------------------------------------------------------
# Historial de chat (persistente durante la sesion del navegador)
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial existente al recargar la app
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------------------------
# Reaccionar a la entrada del usuario
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Mostrar y guardar el mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mejora 3: solo se reenvian los ultimos N mensajes (no toda la conversacion
    # completa desde el inicio), para limitar el costo por turno.
    historial_recortado = st.session_state.messages[-max_historial:]

    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for m in historial_recortado:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = llm.invoke(lc_messages).content
            except Exception as e:
                response = f"Ocurrio un error al contactar al modelo: {e}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
