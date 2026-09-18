# Documentación del Proyecto — Chatbot "Master Chief"

## 1. Descripción general

Chatbot conversacional construido con **Streamlit**, **LangChain** y la **API de OpenAI**,
desarrollado como práctica de clase. Permite chatear con un asistente que mantiene el
historial de la conversación durante la sesión.

- **Versión actual:** 2.0 (ver sección 9 para el detalle de esta versión)
- **Stack:** Python, Streamlit, LangChain (`langchain-openai`), OpenAI API
- **Repositorio:** subido a GitHub como proyecto público/privado del curso

## 2. Origen del proyecto y hallazgo inicial

El punto de partida fue un código de ejemplo compartido en clase (`CODIGO.pdf`) junto con
una guía de configuración del entorno (`CHATBOT.pdf`). Durante la revisión se detectaron
dos problemas en el código original:

1. **API key expuesta directamente en el código fuente** (hardcodeada como string).
   Aunque era una clave de práctica compartida intencionalmente por el docente, se
   corrigió para no dejar el hábito de exponer credenciales en el código.
2. **Historial de conversación incompleto**: el script original solo enviaba el último
   mensaje al modelo, sin el contexto previo de la conversación.

## 3. Configuración del entorno de desarrollo

Pasos seguidos para levantar el proyecto localmente:

1. Creación de un entorno virtual de Python (`python -m venv venv`).
2. Activación del entorno (`venv\Scripts\activate` en Windows / `source venv/bin/activate`
   en Mac/Linux).
3. Instalación de dependencias desde `requirements.txt`
   (`streamlit`, `langchain-openai`, `python-dotenv`).
4. Generación de una **API key propia** en [platform.openai.com](https://platform.openai.com/api-keys),
   con una compra de crédito mínima de $5 USD, más que suficiente para el uso de la práctica.
5. Configuración de la clave en un archivo `.env` local (nunca en el código ni en el
   repositorio), usando `.env.example` como plantilla.

## 4. Correcciones aplicadas al código original

| Problema detectado | Solución aplicada |
|---|---|
| API key hardcodeada en el script | Lectura desde variable de entorno (`os.getenv`) vía `python-dotenv` |
| Solo se enviaba el último mensaje al modelo | Se reconstruye el historial completo (`SystemMessage`, `HumanMessage`, `AIMessage`) en cada request |
| Modelo `gpt-4o` daba error 404 (sin acceso) | Se cambió el modelo por defecto a `gpt-4o-mini`, configurable por variable de entorno |
| Sin manejo de errores de la API | Se agregó un `try/except` alrededor de la llamada al modelo |

## 5. Cambio de identidad del bot

Después de la primera publicación en GitHub, se decidió cambiar el nombre del asistente
de "Carlos" a **"Master Chief"**, actualizando:

- El `SYSTEM_PROMPT` que define la persona del bot.
- El título mostrado en la interfaz (`st.title(...)`).
- Las referencias correspondientes en el `README.md`.

Este cambio se subió como un commit adicional sobre la rama principal.

## 6. Control de versiones y publicación

1. Inicialización de un repositorio local con `git init`.
2. Exclusión de archivos sensibles y de entorno mediante `.gitignore`
   (`.env`, `venv/`, `__pycache__/`, etc.).
3. Commit inicial y `push` a un repositorio remoto en GitHub.
4. Etiquetado de la primera entrega estable como `v1.0` (`git tag -a v1.0`).
5. Commit posterior para el cambio de nombre del bot, sobre la misma rama `main`.

## 7. Buenas prácticas de seguridad aplicadas

- Ninguna credencial se almacena en el código fuente ni en el historial de Git.
- El archivo `.env` con la clave real nunca se sube al repositorio.
- Se documentó la recomendación de revocar cualquier clave que haya sido expuesta
  públicamente (por ejemplo, en materiales de clase compartidos como PDF).

## 8. Estructura final del repositorio

```
chatbot-carlos/
├── chatbot.py        # Lógica principal de la app (Streamlit + LangChain)
├── requirements.txt  # Dependencias del proyecto
├── .env.example       # Plantilla de variables de entorno (sin datos sensibles)
├── .gitignore         # Exclusión de archivos sensibles y temporales
└── README.md          # Instalación, uso y notas del proyecto
```

## 9. Versión 2.0 — mejoras aplicadas

A partir del análisis de riesgos y buenas prácticas revisado durante el curso
(ver sección de preguntas de la guía), se implementaron tres mejoras
concretas sobre la v1.0, en un archivo nuevo `chatbot_v2.py` (se conservó
`chatbot.py` como referencia de la v1.0):

| Mejora | Qué cambió | Por qué |
|---|---|---|
| Transparencia ética | El `SYSTEM_PROMPT` ya no instruye al bot a negar ser una IA. Ahora responde con honestidad si se le pregunta directamente, manteniendo su nombre y personalidad. | Evitar el engaño activo hacia el usuario; alinear el bot con principios de transparencia de IA. |
| Selector de modelo | Se agregó un `st.selectbox` en la barra lateral para elegir entre `gpt-4o-mini` y `gpt-4o` en tiempo real, sin tocar el código. | Dar control al usuario sobre el balance costo/capacidad, en vez de fijar el modelo de forma rígida. |
| Límite de historial | Un `st.slider` define cuántos mensajes recientes (`st.session_state.messages[-max_historial:]`) se reenvían al modelo en cada turno, en vez de toda la conversación desde el inicio. | Controlar el costo por turno en conversaciones largas (relacionado con el análisis de gestión de saldo de la Pregunta 8). |

Adicionalmente se agregó un botón de "Reiniciar conversación" en la barra
lateral y `st.set_page_config` para un título/ícono de pestaña más pulido.

### Flujo de publicación de la v2.0

1. Commit del archivo `chatbot_v2.py` sobre la rama `main`.
2. Actualización de `README.md` y de este documento para reflejar la nueva
   versión.
3. Etiquetado del release como `v2.0` (`git tag -a v2.0`).

## 10. Posibles próximos pasos

- Manejo de múltiples conversaciones o usuarios.
- Streaming de la respuesta en tiempo real.
- Manejo diferenciado de errores (cuota agotada vs. modelo no disponible vs. fallo de red).
- Despliegue en un servicio de hosting (por ejemplo, Streamlit Community Cloud),
  usando gestión de secretos propia de la plataforma en vez de `.env`.
