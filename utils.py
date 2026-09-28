"""Funciones utilitarias compartidas por la app."""

from pathlib import Path

import streamlit as st


def cargar_estilos(ruta_css: str) -> None:
    """Lee un archivo .css y lo inyecta en la pagina de Streamlit.

    Streamlit no soporta <link rel="stylesheet"> a un archivo externo,
    asi que la forma estandar es leer el CSS como texto e insertarlo
    dentro de una etiqueta <style> via st.markdown.
    """
    css_path = Path(ruta_css)
    if not css_path.exists():
        st.warning(f"No se encontro el archivo de estilos: {ruta_css}")
        return

    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
