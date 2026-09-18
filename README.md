# Master Chief - Tutor Virtual 🤖

Chatbot conversacional construido con **Streamlit**, **LangChain** y la **API de OpenAI**.

> Versión 2.0

## Descripción

Aplicación web simple de chat donde "Master Chief" responde a las preguntas del
usuario usando un modelo de OpenAI, manteniendo el historial de la conversación
en la sesión. La v2.0 permite elegir el modelo desde la interfaz y controlar
cuánto historial se reenvía al modelo en cada turno.

## Requisitos previos

- Python 3.10+
- Una cuenta de OpenAI con créditos disponibles y una API key
  (https://platform.openai.com/api-keys)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/<tu-usuario>/<tu-repo>.git
   cd <tu-repo>
   ```

2. Crea y activa un entorno virtual:

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   Si aparece un error de "ejecución de scripts deshabilitada", abre PowerShell
   como administrador y ejecuta:
   ```powershell
   Set-ExecutionPolicy Unrestricted -Force
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tu API key:
   - Copia `.env.example` a `.env`
   - Reemplaza `tu_clave_api_aqui` por tu clave real de OpenAI

   ```bash
   cp .env.example .env
   ```

   El archivo `.env` **nunca** se sube al repositorio (está en `.gitignore`).

## Uso

Ejecuta la aplicación:

```bash
streamlit run chatbot_v2.py
```

Esto abrirá automáticamente el navegador en `http://localhost:8501` con la
interfaz de chat. Desde la barra lateral puedes:

- Elegir el modelo de OpenAI a usar (GPT-4o mini o GPT-4o).
- Ajustar cuántos mensajes recientes se envían como contexto al modelo.
- Reiniciar la conversación con un clic.

> La versión anterior (`chatbot.py`) se conserva en el repositorio como
> referencia de la v1.0, pero la versión activa a partir de ahora es
> `chatbot_v2.py`.

## Estructura del proyecto

```
chatbot-carlos/
├── chatbot.py         # Versión 1.0 (se conserva como referencia)
├── chatbot_v2.py      # Versión 2.0 (versión activa)
├── requirements.txt   # Dependencias del proyecto
├── .env.example        # Plantilla de variables de entorno
├── .gitignore
├── README.md
└── DOCUMENTACION.md   # Bitácora del proceso de desarrollo
```

## Notas de seguridad

- **Nunca** subas tu archivo `.env` ni pegues tu API key directamente en el
  código fuente.
- Si una clave llegó a exponerse (por ejemplo en un commit, captura de
  pantalla o chat), revócala inmediatamente desde el dashboard de OpenAI y
  genera una nueva.

## Notas de diseño (v2.0)

- El bot ya **no niega ser una inteligencia artificial** cuando se le pregunta
  directamente: mantiene su nombre y personalidad, pero responde con
  honestidad ante esa pregunta específica.
- El historial que se reenvía al modelo está limitado (configurable desde la
  barra lateral) para evitar que el costo por turno crezca sin control en
  conversaciones largas.

## Roadmap / próximas versiones

- [x] Selección de modelo desde la interfaz
- [x] Límite configurable de historial reenviado al modelo
- [ ] Manejo de múltiples conversaciones/usuarios
- [ ] Streaming de la respuesta en tiempo real
- [ ] Despliegue en Streamlit Community Cloud

## Licencia

MIT
