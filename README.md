# Master Chief - Tutor Virtual 🤖

Chatbot conversacional construido con **Streamlit**, **LangChain** y la **API de OpenAI**.

> Versión 5.0

Documentación actualizada el 2026-10-08. Entrada principal: `chatbot_v5.py`.

## Descripción

Aplicación de chat donde "Master Chief" responde con OpenAI. La versión 5
conserva la interfaz y el flujo de la versión 4, y añade contexto persistente,
quiz, documentos descargables y consultas por micrófono.

## Novedades de la versión 5

- `storage.py`: conversaciones y contexto por conversación. Los fragmentos,
  transcripciones y metadatos se guardan en `data/contextos/<id>.json`;
  los bytes de imágenes, en `data/archivos/<id>/`. Al recargar o cambiar de
  conversación se recuperan sin adjuntar otra vez. La selección del chat queda
  en la URL. JSON inválido e imágenes faltantes o dañadas se omiten.
  Un nombre de adjunto en un historial antiguo no contiene el archivo: si no
  existe contexto recuperable, la interfaz avisa que debes adjuntarlo de nuevo.
- `archivos.py`: lectores PDF/TXT/DOCX/XLSX, transcripción y exportación.
- `busqueda.py`: fragmentación y búsqueda TF-IDF. El chat envía el texto completo
  cuando cabe en el presupuesto de contexto. En documentos extensos recupera
  fragmentos relevantes; si una petición general como "revisa este documento"
  no tiene coincidencias, utiliza una muestra en lugar de omitir el documento.
- `chatbot_v5.py`: interfaz. `quiz.py`: esquema y validación del quiz.
- En la barra lateral, **Quiz** permite elegir entre 3 y 10 preguntas sobre los
  documentos de texto activos. Al enviar el formulario aparecen nota y
  explicaciones. Sin documentos, **Generar quiz** está deshabilitado.
- La generación de documentos es una capacidad del chat, no un panel aparte.
  Puedes pedir **"Genera un PDF sobre el agua"**, **"Exporta ese resumen a Word"**
  o **"Guárdalo en un TXT"**. El modelo invoca una herramienta para redactar el
  documento con los adjuntos, transcripciones e historial; el chatbot entrega
  la descarga y una vista previa dentro de su respuesta. Los documentos quedan
  guardados en los mensajes y sus descargas se recuperan al abrir el chat.
  El modelo seleccionado redacta el documento; opcionalmente puedes configurar
  `OPENAI_DOCUMENT_MODEL=gpt-4.1` en `.env` para usar otro modelo en la redacción
  (requiere acceso en tu cuenta). Las librerías locales construyen los archivos,
  sin ejecutar código generado por el modelo. Si falta tema o contexto, el
  asistente debe pedir aclaración antes de generar el archivo.
- El icono de **micrófono está integrado en la barra de chat**, junto a los
  adjuntos y al envío. Graba y envía desde esa misma barra, sin panel lateral.
  La grabación se transcribe con `gpt-4o-mini-transcribe` y se combina con el
  texto escrito para formar la consulta. También puedes pedir documentos por
  voz. Necesita permiso del navegador, un micrófono y localhost o HTTPS.
- **Quitar** borra el contexto y los archivos del chat, no sus mensajes.
  Eliminar una conversación borra también su contexto y sus imágenes.
  **Limpiar conversación** conserva los adjuntos, igual que en la versión 4.

Los límites están al principio de `chatbot_v5.py`: 5 archivos por mensaje,
20 MB por archivo y 25 MB por audio. A los audios y grabaciones se les aplica
el menor de los dos límites de tamaño (20 MB por defecto). Los archivos
excedidos se avisan y omiten; se procesan los demás. En revisión de adjuntos y
generación de quiz y documentos, material seleccionado de más de 60.000
caracteres se muestrea con una advertencia.
Los quizzes viven en la sesión. Los documentos generados se guardan con la
conversación, para recuperar la descarga y seguir consultando su contenido.

Las llamadas de chat, transcripción, quiz y redacción consumen créditos de
OpenAI. Los errores se muestran sin trazas técnicas y distinguen cuota/saldo,
clave inválida, modelo no disponible, conexión y otros fallos.

Los PDF con texto se leen localmente. Las páginas escaneadas, como imágenes
dentro de un PDF, se envían automáticamente al modelo visual seleccionado
para transcribirlas. Esto consume créditos adicionales y se avisa antes de
procesarlas. No necesita instalar un motor de OCR externo. Se procesa un máximo
de 10 páginas sin texto por PDF (`MAX_PAGINAS_LECTURA_VISUAL`); el resto se omite
con un aviso de revisión parcial. En PDF mixtos se conservan tanto el texto
local como las transcripciones visuales. El resultado y los números de páginas
procesadas/omitidas quedan en el contexto, permitiendo consultas y quiz después
de recargar sin repetir la lectura visual.

Si el PDF está vacío, protegido, es ilegible o falla la lectura visual,
se indica con un aviso. Puedes adjuntar otra versión, TXT/DOCX o imágenes.
Si ninguno de los adjuntos de un mensaje se puede procesar, no se envía la
consulta al modelo sin su contenido. Los demás archivos válidos se procesan.
La transcripción visual puede cometer errores: comprueba datos importantes
contra el documento original.

Los contextos locales no están cifrados. Los contextos, imágenes e historiales
están excluidos de Git; no uses una instancia pública
compartida para conversaciones privadas. El material usado en las consultas
se envía a OpenAI.

## Requisitos previos

- Python 3.10+ (pruebas ejecutadas con Python 3.12.5).
- Streamlit 1.63.0+ para el micrófono integrado en `st.chat_input`.
- Una cuenta de OpenAI con créditos disponibles y una API key
  (https://platform.openai.com/api-keys)
- Acceso a `gpt-4o-mini` o `gpt-4o` y a `gpt-4o-mini-transcribe` si usas audio.
- Un navegador con permiso de micrófono y localhost o HTTPS para grabar.

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
  .\venv\Scripts\Activate.ps1
   ```
  Si PowerShell bloquea la activación, permite scripts solo en esta sesión,
  sin abrir una consola como administrador:
   ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  .\venv\Scripts\Activate.ps1
   ```
  También puedes ejecutar directamente `venv\Scripts\python.exe` sin activar
  el entorno ni cambiar políticas.

   **macOS / Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
  python -m pip install -r requirements.txt
   ```

4. Configura tu API key:
   - Copia `.env.example` a `.env`
   - Reemplaza `tu_clave_api_aqui` por tu clave real de OpenAI

  **Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
  **macOS / Linux:**
  ```bash
  cp .env.example .env
   ```

   El archivo `.env` **nunca** se sube al repositorio (está en `.gitignore`).
  No sobrescribas un `.env` que ya hayas configurado.

### Variables de entorno

| Variable | Uso |
|---|---|
| `OPENAI_API_KEY` | Obligatoria. Clave del proyecto OpenAI; no se publica. |
| `OPENAI_DOCUMENT_MODEL` | Opcional. Modelo de redacción de documentos, por ejemplo `gpt-4.1`; si no se configura, se usa el modelo del chat. |

El modelo de chat y de lectura visual se selecciona en la barra lateral. La
transcripción de audio usa `gpt-4o-mini-transcribe`.

## Uso

Ejecuta la aplicación:

```bash
python -m streamlit run chatbot_v5.py --server.address 127.0.0.1 --server.port 8501
```

Abre `http://127.0.0.1:8501`. El servidor solo escucha en el equipo local.
Desde la barra lateral puedes:

- Elegir el modelo de OpenAI a usar (GPT-4o mini o GPT-4o).
- Ajustar cuántos mensajes recientes se envían como contexto al modelo.
- Crear, buscar, cambiar y eliminar conversaciones.
- Limpiar los mensajes del chat actual y descargar su historial como TXT.
- Generar y responder un quiz a partir de los documentos activos.

Los documentos se adjuntan en la barra del chat. El micrófono está en esa misma
barra. Para crear archivos, escribe la solicitud en el chat; no hay un panel
independiente de generación de documentos.

> Las versiones anteriores se conservan como referencia; `chatbot_v4.py` no
> se modifica para implementar la versión 5.

## Pruebas locales

```bash
python -m unittest discover -s tests -p test_v5.py -v
```

Usan carpetas temporales y OpenAI simulado, sin consumir créditos. Cubren
persistencia y recuperación en una nueva sesión, cambio de chat, eliminación,
archivos corruptos, límites, lectores, errores, quiz, transcripción y descargas.
La generación conversacional usa herramientas de OpenAI, no coincidencias
de palabras; su decisión semántica requiere una comprobación con un modelo real.
El permiso y la captura de un micrófono físico requieren una comprobación manual.
La lectura visual de un PDF y las llamadas reales a OpenAI también necesitan
una prueba manual con crédito disponible. La suite incluye 34 pruebas al
2026-10-08, incluyendo PDF escaneado/mixto, límites y módulo antiguo en memoria.

## Mantenimiento

`requirements.txt` declara versiones mínimas, no un entorno bloqueado.
Antes de actualizar, guarda los cambios de código y detén Streamlit con
`Ctrl+C` en la terminal que lo ejecuta. Dentro del entorno virtual:

```bash
python -m pip install --upgrade -r requirements.txt
python -m pip check
python -m unittest discover -s tests -p test_v5.py -v
```

Reinicia la aplicación después de actualizar dependencias. No se ha certificado
cada combinación de versiones ni todas las versiones de Python compatibles.
Revisa los cambios de versiones mayores antes de actualizar.

### Solución de problemas

- **`unexpected keyword argument 'modelo_vision'`:** una instancia puede haber
  retenido una función anterior. La app detecta esa firma y recarga el módulo;
  si persiste, detén esa instancia con `Ctrl+C` y reinicia desde este repositorio.
- **Dos apps distintas en el puerto 8501:** `localhost` puede resolver a IPv6
  mientras otra instancia escucha en IPv4. Usa `http://127.0.0.1:8501` y una
  sola instancia. Si el puerto está ocupado, detén la que no necesitas o usa
  `--server.port 8502` y abre `http://127.0.0.1:8502`.
- **Un adjunto solo aparece en el historial:** su nombre no contiene los bytes
  ni el texto. Adjunta de nuevo y comprueba que aparezca en **Contexto activo**.
- **PDF sin texto:** se intentará lectura visual. Si falla, comprueba el aviso
  de clave, saldo, permisos del modelo o páginas ilegibles. La lectura parcial
  se indica explícitamente; la app no implementa OCR local con Tesseract.
- **Micrófono no disponible:** revisa permisos y usa localhost o HTTPS. No basta
  con acceder por una dirección HTTP de otro equipo.

## Estructura del proyecto

```
ChatbotProject/
├── chatbot.py         # Versión 1.0 (se conserva como referencia)
├── chatbot_v2.py      # Versión 2.0
├── chatbot_v3.py      # Versión 3.0 (conservada)
├── chatbot_v4.py      # Versión 4.0 (conservada)
├── chatbot_v5.py      # Versión 5.0 (versión activa)
├── storage.py         # Conversaciones y contexto persistente
├── archivos.py        # Lectura, transcripción y exportación
├── busqueda.py        # Fragmentación y búsqueda documental
├── quiz.py            # Quiz estructurado y validación
├── tests/test_v5.py   # Pruebas locales aisladas
├── utils.py           # Inyección de estilos
├── styles.css         # Diseño compartido con versiones anteriores
├── config.toml        # Tema de referencia; Streamlit usa .streamlit/config.toml
├── data/              # Datos locales privados, creados durante el uso
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
- `.gitignore` no elimina archivos ya publicados o rastreados. Si un historial
  está rastreado, usa `git rm --cached data/conversaciones.json` (o la ruta
  correspondiente) antes de publicar. Revisa `git status` y el diff del commit.
- El tema de `config.toml` es de referencia. Para que Streamlit lo cargue
  automáticamente debe ubicarse en `.streamlit/config.toml`; la app inyecta
  además `styles.css`. Las reglas CSS dependen de atributos internos de
  Streamlit y deben revisarse tras actualizarlo.

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
- [x] Manejo de múltiples conversaciones locales (sin autenticación multiusuario)
- [x] Streaming de la respuesta en tiempo real
- [ ] Despliegue en Streamlit Community Cloud

## Licencia

MIT
