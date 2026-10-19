# Publicar Master Chief con un enlace público

La app se publica gratis en **Streamlit Community Cloud**. El acceso está
restringido a cuentas Google `@unab.edu.sv`. No se necesita Supabase, SMTP
ni ningún servidor propio.

## Antes de empezar

- El código debe estar en GitHub (`Heber666/chatbot-sistemas-expertos`).
- Nunca subas `.env` ni `.streamlit/secrets.toml`: ya están en `.gitignore`.
- Ten a mano tu clave de OpenAI y el `client_id` / `client_secret` de Google.
- Pon un **límite de gasto** en [OpenAI → Limits](https://platform.openai.com/settings/organization/limits):
  con un enlace público, cada estudiante que use la app consume tus créditos.

## 1. Subir los cambios a GitHub

```powershell
git status
```

Comprueba que **no** aparezcan `.env`, `.streamlit/secrets.toml` ni
`data/usuarios/`. Después sube los cambios y confirma que están en GitHub.

## 2. Crear la app en Streamlit Community Cloud

1. Entra a [share.streamlit.io](https://share.streamlit.io) e inicia sesión
   con tu cuenta de GitHub.
2. Pulsa **Create app → Deploy a public app from GitHub**.
3. Completa:
   - Repository: `Heber666/chatbot-sistemas-expertos`
   - Branch: `main`
   - Main file path: `chatbot_v5.py`
   - App URL: elige un nombre, por ejemplo `master-chief-unab`.
     Tu enlace será `https://master-chief-unab.streamlit.app`.
4. Abre **Advanced settings** y elige **Python 3.12** (la versión probada).
5. Todavía no pulses Deploy: primero configura los secretos.

## 3. Configurar los secretos

En **Advanced settings → Secrets** pega lo siguiente con tus valores reales.

> **Importante:** las claves sueltas deben ir **arriba** de `[auth]`.
> En TOML, todo lo que está debajo de `[auth]` pasa a pertenecer a esa
> sección, y la app no encontraría la clave de OpenAI.

```toml
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4o-mini"
ALLOWED_EMAIL_DOMAIN = "@unab.edu.sv"

[auth]
redirect_uri = "https://master-chief-unab.streamlit.app/oauth2callback"
cookie_secret = "una-clave-aleatoria-larga"
client_id = "tu-client-id.apps.googleusercontent.com"
client_secret = "tu-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

- `redirect_uri` debe usar **tu** URL de la app, terminada en `/oauth2callback`.
- `cookie_secret` puede ser el mismo de tu `secrets.toml` local o uno nuevo:

  ```powershell
  python -c "import secrets; print(secrets.token_urlsafe(48))"
  ```

Pulsa **Deploy**. La primera instalación tarda unos minutos.

## 4. Autorizar la URL pública en Google

En [Google Cloud Console](https://console.cloud.google.com) →
**APIs & Services → Credentials** → tu cliente OAuth:

1. En **Authorized redirect URIs** agrega, sin borrar la de localhost:

   ```text
   https://master-chief-unab.streamlit.app/oauth2callback
   ```

2. En **OAuth consent screen**, si la app está en modo **Testing**, solo
   pueden entrar los correos agregados como usuarios de prueba. Para que
   entre cualquier estudiante, pulsa **Publish app** (pasa a *In production*).
   Como solo usa nombre y correo, Google no exige una verificación adicional.

Si al entrar aparece `redirect_uri_mismatch`, la URL de Google y la de
`redirect_uri` no son idénticas: revisa `https`, el nombre de la app y que no
sobre ni falte una `/` al final.

## 5. Probar el enlace

Abre el enlace público en una ventana de incógnito y comprueba que:

- Entras con una cuenta `@unab.edu.sv`.
- Una cuenta de Gmail personal es rechazada.
- El chat responde (si dice que falta `OPENAI_API_KEY`, revisa el orden de
  los secretos del paso 3).

## Limitación importante: el historial no es permanente

Streamlit Community Cloud **no conserva archivos**. Las conversaciones se
guardan en `data/usuarios/` dentro del servidor, y se borran cada vez que la
app se reinicia: al subir cambios a GitHub, al reiniciarla desde el panel o
cuando se duerme por inactividad. Para un historial permanente hay que
guardarlo en una base de datos externa, por ejemplo Supabase.

## Ejecutar en tu equipo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run chatbot_v5.py
```

En local, la clave de OpenAI se lee de `.env` y Google de
`.streamlit/secrets.toml`, con `redirect_uri = "http://localhost:8501/oauth2callback"`.

La carpeta `supabase/` contiene un esquema para una futura versión con
historial permanente; no se usa en la versión actual.
