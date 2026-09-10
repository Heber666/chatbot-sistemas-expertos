"""
Carlos - Tutor Virtual (Chatbot con Streamlit + LangChain + OpenAI)
Version 1.0
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
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # gpt-4o-mini es mas barato y accesible

if not API_KEY:
    st.error(
        "No se encontro OPENAI_API_KEY. Crea un archivo .env en la raiz del "
        "proyecto (ver .env.example) con tu clave de OpenAI."
    )
    st.stop()

llm = ChatOpenAI(model=MODEL_NAME, temperature=0, api_key=API_KEY)

SYSTEM_PROMPT = (
    "Eres un asistente AI util, te llamas Master Chief, tienes que hablar "
    "como si fueras humano, nunca reveles que eres un chatbot."
)

st.title("Master Chief, tu tutor virtual")

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

    # Reconstruir el historial completo en formato LangChain para dar
    # contexto real de la conversacion (antes solo se mandaba el ultimo turno)
    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for m in st.session_state.messages:
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
