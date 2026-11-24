import os
import hmac
import hashlib
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class ModelBase:
    """Conexión a Supabase y hash de los id. Todos los modelos heredan de esta clase."""

    def __init__(self) -> None:
        try:
            self.SECRET_KEY = os.environ.get("SECRET_KEY", "cambiar-esta-clave").encode("utf-8")
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", "")
            )
        except Exception as error:
            print(f"ERROR 100: {str(error)}")

    def generar_hash(self, id: int) -> str:
        """Genera un hash único a partir del ID (formato id:firma)."""
        try:
            mensaje = str(id).encode("utf-8")
            firma = hmac.new(self.SECRET_KEY, mensaje, hashlib.sha256).hexdigest()
            return f"{id}:{firma}"
        except Exception as error:
            print(f"ERROR 106: {str(error)}")
            return ""

    def validar_hash(self, hash_a_validar: str) -> int | None:
        """Regresa el id si el hash es válido; si no, regresa None."""
        try:
            id_str, sep, _ = hash_a_validar.partition(":")
            if sep and id_str.isdigit():
                token_esperado = self.generar_hash(int(id_str))
                if hmac.compare_digest(token_esperado, hash_a_validar):
                    return int(id_str)
            return None
        except Exception as error:
            print(f"ERROR 107: {str(error)}")
            return None
