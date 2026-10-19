# Documentación del Proyecto — Chatbot "Master Chief"

## 1. Descripción general

Chatbot conversacional construido con **Streamlit**, **LangChain** y la **API de OpenAI**,
desarrollado como práctica de clase. La versión actual permite conversar con historial
local persistente, analizar adjuntos, generar documentos y quizzes y consultar por voz.

- **Versión actual:** 6.0, entrada `chatbot_v6.py` (ver sección 11).
- **Última actualización:** 2026-10-18.
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
3. Instalación desde `requirements.txt` con `python -m pip install -r requirements.txt`.
   Además de Streamlit/LangChain incluye lectores, exportación y pruebas (ver sección 12).
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

## 8. Estructura inicial del repositorio (v1.0)

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

## 10. Versión 5.0: arquitectura y capacidades

Las versiones anteriores (`chatbot.py`, `chatbot_v2.py`, `chatbot_v3.py` y
`chatbot_v4.py`) se conservan como referencia. La interfaz y los estilos de v4
se reutilizan en v5; las funciones nuevas se integran al flujo del chat.

| Módulo | Responsabilidad |
|---|---|
| `chatbot_v5.py` | Interfaz Streamlit, selección de chat, entrada multimodal, streaming y ejecución de herramientas. |
| `storage.py` | Conversaciones, migración del historial y persistencia/recuperación/eliminación de contexto. |
| `archivos.py` | Lectores, transcripción de audio, lectura visual PDF, límites, errores y exportación DOCX/PDF/TXT. |
| `busqueda.py` | Fragmentación por palabras y recuperación TF-IDF. |
| `quiz.py` | Esquemas Pydantic, generación estructurada y calificación del quiz. |
| `utils.py` / `styles.css` | Inyección de estilos y tema «Cuaderno» (sombras, burbujas, portada); colores y fuentes en `.streamlit/config.toml`. |
| `tests/test_v5.py` | Pruebas unitarias y Streamlit AppTest con almacenamiento temporal y OpenAI simulado. |

### Conversaciones y almacenamiento

- `data/conversaciones.json` conserva títulos, mensajes y contenido/formato de
   los documentos generados. `data/historial.json` se usa para migrar datos antiguos.
- `data/contextos/<id>.json` guarda fragmentos documentales, transcripciones y
   metadatos por chat. Las imágenes se guardan fuera del JSON en `data/archivos/<id>/`.
- Las escrituras JSON usan un archivo temporal y reemplazo. Las imágenes tienen
   una huella SHA-256; se omiten archivos ausentes o dañados. El JSON de contexto
   corrupto no impide abrir la app.
- La selección del chat se conserva en el parámetro `chat` de la URL. El contexto
   se recupera al abrir o cambiar de conversación.
- **Quitar** elimina el contexto y sus imágenes; no elimina los mensajes ni los
   documentos generados guardados en ellos. Eliminar un chat borra también su contexto.
- **Limpiar conversación** vacía mensajes y título, pero conserva los adjuntos.
   Los quizzes son estado de sesión y no se recuperan después de cerrar la sesión.

### Lectura y revisión de documentos

Los formatos de texto admitidos son PDF, TXT, DOCX y XLSX. El PDF con texto se lee
con `pypdf`; Word incluye párrafos y tablas; Excel incluye las hojas y sus valores
almacenados, sin ejecutar macros ni recalcular fórmulas. No se implementa OCR local.

Las páginas PDF sin texto y con contenido visual se separan con `PdfWriter` y
se envían como archivo PDF base64 a Chat Completions. El modelo visual seleccionado
las transcribe; el resultado se guarda como texto de documento y puede alimentar
el chat y el quiz. Los PDF mixtos combinan texto nativo y transcripciones. Se avisa
del coste adicional y de las páginas omitidas; se guardan metadatos del alcance.

El chat envía el texto completo cuando cabe en el presupuesto de contexto. Para
documentos extensos selecciona fragmentos relevantes. Si una petición general
como "revisa este documento" no tiene coincidencias, utiliza una muestra acotada,
en lugar de enviar al modelo solo el nombre del archivo.

Si no se procesa ningún adjunto del mensaje, no se envía la consulta al modelo
sin su contenido. Los otros archivos válidos continúan. Un nombre en el historial
no permite recuperar un PDF ausente: la app avisa que se debe adjuntar de nuevo.

### Quiz

Se genera desde la barra lateral con 3 a 10 preguntas basadas en el historial
del chat activo y en los documentos o transcripciones activos de esa conversación.
Cada pregunta tiene cuatro opciones distintas, índice correcto de 0 a 3 y una
explicación. Pydantic valida el esquema y la cantidad recibida; las preguntas se
muestran con `st.form`. Al responder todas se calcula la nota sobre 100 y se
muestran aciertos, respuestas correctas y explicaciones. La generación consume
créditos; la calificación es local. Sin mensajes ni material activo, el botón
está deshabilitado.

### Documentos como capacidad del chat

Solicitudes como "Genera un PDF" o "Exporta ese resumen a Word" permiten al modelo
invocar la herramienta `generar_documento`. No hay un panel de generación aparte
ni detección basada únicamente en palabras clave. Los argumentos aceptados son
formato (`PDF`, `DOCX`, `TXT`) e instrucciones. Si falta tema o contexto, se pide
aclaración. Se rechazan herramientas desconocidas o argumentos no válidos.

La herramienta obtiene título y secciones estructuradas. `python-docx` construye
Word, ReportLab construye PDF y TXT se codifica en UTF-8. La descarga y vista previa
aparecen en la respuesta; el contenido guardado permite recuperar la descarga y
seguir consultando ese documento. No se ejecuta código propuesto por el modelo.

La herramienta declara `strict=True` en su definición, además de la configuración
de LangChain, para evitar perder esa validación al usar un diccionario preformateado.

### Micrófono

`st.chat_input(accept_file="multiple", accept_audio=True)` integra adjuntos,
micrófono y envío en la misma barra. La grabación WAV se transcribe con
`gpt-4o-mini-transcribe`, se combina con el texto escrito y se guarda en el contexto.
No hay panel ni botón lateral de envío de grabaciones. Es necesario permiso del
navegador y un contexto seguro (localhost o HTTPS).

### Límites y errores

| Constante en `chatbot_v5.py` | Valor actual |
|---|---|
| `MAX_ARCHIVOS_POR_MENSAJE` | 5, incluyendo la grabación si existe. |
| `MAX_TAMANO_ARCHIVO` | 20 MB por archivo. |
| `MAX_TAMANO_AUDIO` | 25 MB; el límite efectivo es el menor de los dos límites de tamaño (20 MB). |
| `MAX_CARACTERES_GENERACION` | 60.000 caracteres de material seleccionado, antes de los separadores e instrucciones. |
| `MAX_PAGINAS_LECTURA_VISUAL` | 10 páginas sin texto por PDF. |

Los archivos excedidos se omiten con `st.warning`; se procesan los restantes.
El procesamiento visual incompleto se marca como revisión parcial. Los mensajes
de error distinguen saldo/cuota, límite temporal de solicitudes, clave inválida,
modelo no disponible/permisos, conexión, formato, almacenamiento y otros fallos.
Los errores de la API no se guardan como respuestas del asistente.

## 11. Versión 6.0: acceso universitario, datos por usuario e interfaz «Cuaderno»

La versión 6.0 (`chatbot_v6.py`) conserva todas las capacidades de la 5.0 y la
prepara para publicarse con un enlace público. `chatbot_v5.py` se conserva sin
cambios como referencia.

### Cambios principales

| Área | Cambio |
|---|---|
| Acceso | Inicio de sesión con Google mediante `st.login()` (OIDC de Streamlit). Solo se admiten correos `@unab.edu.sv`; otra cuenta se rechaza con opción de cerrar sesión. |
| Datos por usuario | `storage.py` acepta un `usuario_id` opcional y guarda conversaciones, contexto e imágenes en `data/usuarios/<id>/`. Un usuario no ve los datos de otro. Sin `usuario_id` conserva las rutas de la v5. |
| Interfaz | Tema «Cuaderno»: colores y fuentes en `.streamlit/config.toml` (papel, tinta, tomate, mostaza y barra lateral verde pizarra; Fraunces, Bricolage Grotesque y JetBrains Mono) y `styles.css` reescrito (sombras sólidas, burbujas, portada). |
| Inicio | Portada de acceso, saludo personalizado y cuatro sugerencias que envían la consulta con un clic. El encabezado muestra modo, nivel y modelo. |
| Configuración | `leer_configuracion()` busca cada valor en `.env`/variables de entorno y, si falta, en los Secrets de Streamlit. Si falta la clave, el error indica la causa sin mostrar su valor. |
| Publicación | `DEPLOYMENT.md` documenta la publicación en Streamlit Community Cloud. |

`auth.py` contiene la validación del dominio. La carpeta `supabase/` guarda un
esquema para una futura versión con historial permanente; la 6.0 no lo usa.

### Decisiones durante el desarrollo

Se evaluó migrar a Next.js, FastAPI y Supabase, y un segundo factor por código
enviado al correo. Se descartó para mantener Streamlit como interfaz única: el
correo OTP de Supabase exigía un SMTP propio para cambiar el enlace mágico por un
código, y no se disponía de uno. El acceso quedó solo con Google institucional; la
verificación en dos pasos depende de la configuración de cada cuenta de Google.

### Incidencias corregidas durante v6

| Incidencia | Causa y corrección |
|---|---|
| El correo enviaba un enlace mágico en vez de un código | Supabase solo permite editar la plantilla con SMTP propio. Se retiró el acceso por correo. |
| `StreamlitMissingAuthlibError` | `st.login` requiere Authlib. `requirements.txt` usa `streamlit[auth]`. |
| `StreamlitAuthError` para el proveedor `"google"` | `st.login("google")` busca `[auth.google]`; los secretos están directamente en `[auth]`. Se usa `st.login()`. |
| `OPENAI_API_KEY` no encontrada en Streamlit Cloud | No existe `.env` en la nube. Se lee también desde `st.secrets` y el error explica si la clave falta o quedó dentro de `[auth]`. |
| Conversaciones privadas sin excluir de Git | `data/usuarios/` no estaba en `.gitignore`; se agregó. |
| Pruebas detenidas en la portada | AppTest no tenía sesión iniciada. Las pruebas simulan un usuario autenticado. |

## 12. Instalación, configuración y mantenimiento actuales

- Python 3.10+; entorno verificado: Python 3.12.5 en Windows.
- Streamlit 1.63.0+ es necesario para audio dentro del chat. Se instala como
   `streamlit[auth]` para incluir Authlib, requerido por el inicio de sesión.
- `langchain-openai`, `langchain-core`, `openai` y `pydantic` soportan mensajes,
   herramientas y respuestas estructuradas. `python-dotenv` carga configuración.
- `pypdf`, `python-docx`, `openpyxl` y `reportlab` leen y exportan documentos;
   `scikit-learn` realiza la búsqueda local. `httpx` y `pillow` son importaciones
   directas de las pruebas de red simulada e imágenes PDF.
- `requirements.txt` declara mínimos, no un archivo lock. La compatibilidad de
   todas las combinaciones de versiones o plataformas no está certificada.
- `OPENAI_API_KEY` es obligatoria. `OPENAI_DOCUMENT_MODEL` es opcional; permite
   separar el modelo de redacción del seleccionado en el chat.
   `ALLOWED_EMAIL_DOMAIN` es opcional y vale `@unab.edu.sv` por defecto.
- El inicio de sesión con Google usa `.streamlit/secrets.toml` con una sección
   `[auth]` (`redirect_uri`, `cookie_secret`, `client_id`, `client_secret` y
   `server_metadata_url`). En la nube, todos estos valores van en los Secrets de
   Streamlit; las claves de nivel raíz deben ir antes de `[auth]`.

Instalación dentro del entorno virtual y arranque local:

```bash
python -m pip install -r requirements.txt
python -m streamlit run chatbot_v6.py
```

Abre `http://localhost:8501`: debe coincidir con el host de `redirect_uri`
(`http://localhost:8501/oauth2callback`), o Google rechazará el acceso. La
activación de PowerShell y los pasos para crear `.env` están en `README.md`; no
requieren privilegios de administrador. La publicación está en `DEPLOYMENT.md`.

Al actualizar dependencias, detén Streamlit con `Ctrl+C`, ejecuta la instalación,
`python -m pip check` y la suite de pruebas, y vuelve a iniciar la app. El tema
se carga desde `.streamlit/config.toml`.

### Incidencias corregidas durante v5

| Incidencia | Causa y corrección |
|---|---|
| "No puedo revisar documentos" al pedir una revisión general | TF-IDF podía devolver cero coincidencias; se añade contenido de respaldo e instrucciones de revisión. |
| PDF citado en el historial sin contenido | El nombre no conserva el documento. Se diferencia historial de contexto activo y se solicita volver a adjuntar. |
| PDF escaneado sin texto extraíble | Se incorpora lectura visual por página con OpenAI y persistencia de la transcripción. |
| `unexpected keyword argument 'modelo_vision'` | Un módulo en memoria podía conservar la firma anterior; se comprueba y recarga antes de importar las funciones. |
| `localhost` abría otra instancia | Dos servidores podían usar el mismo puerto en IPv4 e IPv6. Se recomienda una sola instancia y dirección IPv4 explícita. |

## 13. Validación y privacidad

```bash
python -m unittest discover -s tests -p test_v6.py -v
```

La suite de la v6 tiene 40 pruebas al 2026-10-18. Usa carpetas temporales y
respuestas OpenAI simuladas; no modifica historiales personales ni consume
créditos. Además de lo cubierto en la v5 (persistencia, datos corruptos, límites,
PDF escaneado/mixto, fallos visuales, streaming de herramientas, recuperación de
descargas, quiz, audio y recarga de una función antigua en memoria), verifica el
aislamiento de datos entre usuarios, la portada sin sesión, las sugerencias y la
lectura de la clave desde los Secrets. La suite original de la v5
(`-p test_v5.py`, 34 pruebas) sigue pasando contra `chatbot_v5.py`. No acredita
exactitud del OCR, decisiones del modelo real, el inicio de sesión real con
Google, disponibilidad de la cuenta ni funcionamiento de un micrófono físico:
estos aspectos requieren pruebas manuales.

Los contextos y conversaciones locales no están cifrados y pueden contener datos
personales. Se excluyen de Git `.env`, secretos de Streamlit, entornos virtuales,
historiales, contextos, imágenes y `data/usuarios/`. `.gitignore` no elimina datos
ya rastreados o publicados: revisa el diff antes de hacer commit. El texto,
imágenes, PDF de lectura visual y audio utilizados se envían a OpenAI. La v6 exige
una cuenta Google `@unab.edu.sv` y separa los datos por usuario; aun así, el
servidor que la aloja puede leer todas las carpetas. En Streamlit Community Cloud
los archivos no son permanentes: las conversaciones se pierden al reiniciarse la app.

## 14. Posibles próximos pasos

- Historial permanente en una base de datos externa (por ejemplo, Supabase) para
  que las conversaciones sobrevivan a los reinicios de Streamlit Cloud.
- Segundo factor propio de la app, si se dispone de un SMTP institucional.
- Pruebas de instalación en un entorno limpio y bloqueo reproducible de versiones.
- Pruebas reales controladas de lectura visual y calidad de transcripción.
- Mejoras de seguimiento de costes y límites por usuario.
