"""Conversaciones y contexto persistente, sin dependencias de la interfaz."""

import hashlib
import json
import re
import shutil
import uuid
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
CONVERSACIONES_PATH = DATA_DIR / "conversaciones.json"
HISTORIAL_ANTERIOR_PATH = DATA_DIR / "historial.json"


def crear_conversacion(titulo="Nueva conversación"):
    return {"id": uuid.uuid4().hex[:8], "titulo": titulo, "mensajes": []}


def buscar_conversaciones(conversaciones, consulta):
    consulta = consulta.strip().casefold()
    return [
        conversacion for conversacion in conversaciones
        if not consulta or consulta in (
            str(conversacion.get("titulo", "")) + " " + " ".join(
                str(mensaje.get("content", ""))
                for mensaje in conversacion.get("mensajes", [])
            )
        ).casefold()
    ]


def obtener_fragmento_coincidente(conversacion, consulta):
    consulta = consulta.strip()
    if not consulta:
        return ""
    for mensaje in conversacion.get("mensajes", []):
        contenido = str(mensaje.get("content", "")).replace("\n", " ")
        indice = contenido.casefold().find(consulta.casefold())
        if indice >= 0:
            inicio = max(0, indice - 35)
            fin = min(len(contenido), indice + len(consulta) + 55)
            rol = "Tú" if mensaje.get("role") == "user" else "Master Chief"
            prefijo = "..." if inicio else ""
            sufijo = "..." if fin < len(contenido) else ""
            return f"{rol}: {prefijo}{contenido[inicio:fin]}{sufijo}"
    return ""


def _guardar_json(ruta, contenido):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix(".tmp")
    temporal.write_text(json.dumps(contenido, ensure_ascii=False, indent=2), encoding="utf-8")
    temporal.replace(ruta)


def _leer_json(ruta, predeterminado):
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return predeterminado


def guardar_conversaciones(conversaciones):
    _guardar_json(CONVERSACIONES_PATH, conversaciones)


def cargar_conversaciones():
    conversaciones = _leer_json(CONVERSACIONES_PATH, [])
    if isinstance(conversaciones, list):
        conversaciones = [
            conversacion for conversacion in conversaciones
            if isinstance(conversacion, dict)
            and isinstance(conversacion.get("id"), str)
            and re.fullmatch(r"[A-Za-z0-9_-]+", conversacion["id"])
            and isinstance(conversacion.get("titulo"), str)
            and isinstance(conversacion.get("mensajes"), list)
        ]
        if conversaciones:
            return conversaciones
    conversacion = crear_conversacion()
    historial = _leer_json(HISTORIAL_ANTERIOR_PATH, [])
    if isinstance(historial, list) and historial:
        conversacion["titulo"] = "Conversación anterior"
        conversacion["mensajes"] = historial
    conversaciones = [conversacion]
    guardar_conversaciones(conversaciones)
    return conversaciones


def _rutas_contexto(conversacion_id):
    if not isinstance(conversacion_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", conversacion_id):
        raise ValueError("Identificador de conversación inválido.")
    return DATA_DIR / "contextos" / f"{conversacion_id}.json", DATA_DIR / "archivos" / conversacion_id


def guardar_contexto(conversacion_id, contexto):
    ruta, carpeta = _rutas_contexto(conversacion_id)
    serializable = {clave: valor for clave, valor in contexto.items() if clave != "imagenes_activas"}
    imagenes = []
    for imagen in contexto.get("imagenes_activas", []):
        carpeta.mkdir(parents=True, exist_ok=True)
        nombre = uuid.uuid4().hex + ".bin"
        (carpeta / nombre).write_bytes(imagen["bytes"])
        imagenes.append({
            "nombre": imagen["nombre"], "tipo": imagen["tipo"], "archivo": nombre,
            "sha256": hashlib.sha256(imagen["bytes"]).hexdigest(),
        })
    serializable["imagenes_activas"] = imagenes
    _guardar_json(ruta, serializable)
    if carpeta.exists():
        activos = {imagen["archivo"] for imagen in imagenes}
        for archivo in carpeta.iterdir():
            if archivo.is_file() and archivo.name not in activos:
                archivo.unlink(missing_ok=True)


def cargar_contexto(conversacion_id):
    ruta, carpeta = _rutas_contexto(conversacion_id)
    datos = _leer_json(ruta, {})
    if not isinstance(datos, dict) or not datos:
        return {}
    contexto = {}
    for clave in ("documento_fragmentos", "documento_nombres", "audio_nombres"):
        valor = datos.get(clave)
        if isinstance(valor, list) and all(isinstance(elemento, str) for elemento in valor):
            contexto[clave] = valor
    if isinstance(datos.get("audio_transcripciones"), str):
        contexto["audio_transcripciones"] = datos["audio_transcripciones"]
    if isinstance(datos.get("metadatos"), list):
        contexto["metadatos"] = [elemento for elemento in datos["metadatos"] if isinstance(elemento, dict)]
    imagenes = datos.get("imagenes_activas", [])
    contexto["imagenes_activas"] = []
    if isinstance(imagenes, list):
        for imagen in imagenes:
            if not isinstance(imagen, dict) or not all(isinstance(imagen.get(clave), str) for clave in ("archivo", "nombre", "tipo")):
                continue
            if not re.fullmatch(r"[a-f0-9]{32}\.bin", imagen["archivo"]):
                continue
            try:
                contenido = (carpeta / imagen["archivo"]).read_bytes()
                if contenido and hashlib.sha256(contenido).hexdigest() == imagen.get("sha256"):
                    contexto["imagenes_activas"].append({"nombre": imagen["nombre"], "tipo": imagen["tipo"], "bytes": contenido})
            except OSError:
                continue
    return contexto


def eliminar_contexto(conversacion_id):
    ruta, carpeta = _rutas_contexto(conversacion_id)
    ruta.unlink(missing_ok=True)
    if carpeta.exists():
        shutil.rmtree(carpeta)