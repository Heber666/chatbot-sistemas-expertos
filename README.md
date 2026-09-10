# Carlos - Tutor Virtual 🤖

Chatbot conversacional construido con **Streamlit**, **LangChain** y la **API de OpenAI**.

> Versión 1.0

## Descripción

Aplicación web simple de chat donde "Carlos" responde a las preguntas del usuario
usando un modelo de OpenAI, manteniendo el historial de la conversación en la sesión.

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
streamlit run chatbot.py
```

Esto abrirá automáticamente el navegador en `http://localhost:8501` con la
interfaz de chat.

## Estructura del proyecto

```
chatbot-carlos/
├── chatbot.py        # Código principal de la app
├── requirements.txt  # Dependencias del proyecto
├── .env.example       # Plantilla de variables de entorno
├── .gitignore
└── README.md
```

## Notas de seguridad

- **Nunca** subas tu archivo `.env` ni pegues tu API key directamente en el
  código fuente.
- Si una clave llegó a exponerse (por ejemplo en un commit, captura de
  pantalla o chat), revócala inmediatamente desde el dashboard de OpenAI y
  genera una nueva.

## Roadmap / próximas versiones

- [ ] Selección de modelo desde la interfaz
- [ ] Manejo de múltiples conversaciones/usuarios
- [ ] Despliegue en Streamlit Community Cloud

## Licencia

MIT
