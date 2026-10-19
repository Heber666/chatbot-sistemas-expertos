"""Validación del usuario OIDC para la aplicación Streamlit."""

from dataclasses import dataclass


class AuthError(ValueError):
    """Error seguro para mostrar al usuario sin detalles del proveedor."""


@dataclass(frozen=True)
class AuthSettings:
    supabase_url: str
    supabase_anon_key: str
    allowed_email_domain: str = "@unab.edu.sv"


def validar_correo(correo: str, settings: AuthSettings) -> str:
    normalizado = correo.strip().lower()
    if not normalizado.endswith(settings.allowed_email_domain):
        raise AuthError("Debes utilizar tu cuenta Google institucional @unab.edu.sv.")
    return normalizado
