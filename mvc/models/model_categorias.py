import os
from supabase import create_client, Client
from dotenv import load_dotenv
import hashlib
import hmac
from typing import Any, cast

import logging

load_dotenv()

logger = logging.getLogger(__name__)

class ModelCategorias:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL" , ""),
                os.environ.get("SUPABASE_KEY" , "")
            )
            self.SECRET_KEY = b"hola"
        except Exception as error:
            logger.error(f"ERROR 100: {str(error)}")
            print(f"ERROR 100: {str(error)}")

    def generarHash(self,id: int) -> str:
        try:
            """Genera un hash único a partir del ID."""
            mensaje = str(id).encode("utf-8")
            firma =  hmac.new(self.SECRET_KEY, mensaje, hashlib.sha256).hexdigest()
            # Concatena el id:firma
            return f"{id}:{firma}"
        except Exception as error:
            logger.error("ERROR 106: %s", error)
            print(f"ERROR 106: {str(error)}")
            return ""


    def validarHash(self,hash_a_validar: str) -> int|None:
        try:
            # Separa el id, separador y la firma
            id_str, sep, _ = hash_a_validar.partition(":")
            resultado_id = None

            # Solo calculamos el hash si la estructura básica es válida
            if sep and id_str.isdigit():
                token_esperado = self.generarHash(int(id_str))
                if hmac.compare_digest(token_esperado, hash_a_validar):
                    resultado_id = int(id_str)
                else:
                    resultado_id = None
            else:
                resultado_id = None

            return resultado_id
        except Exception as error:
            logger.error("ERROR 107: %s", error)
            print(f"ERROR 107: {str(error)}")
            return -1

    def obtenerCategorias(self) -> list[dict[str,Any]]:
        categorias: list[dict[str,Any]]
        try:
            # SELECT * FROM categorias ORDER BY nombre;
            response = self.supabase.table("categorias").select("*").order("nombre").execute()
            registros = response.data or []
            for registro in registros:
                id_num = int(registro["id"]) # type: ignore
                registro["id"] = self.generarHash(id_num) # type: ignore
            categorias = cast(list[dict[str, Any]],registros)
            return categorias
        except Exception as error:
            logger.error("ERROR 101: %s", error)
            print(f"ERROR 101: {str(error)}")
            return []

    def obtenerCategoriasConTotal(self) -> list[dict[str,Any]]:
        categorias: list[dict[str,Any]]
        try:
            # SELECT * FROM categorias ORDER BY nombre;
            response = self.supabase.table("categorias").select("*").order("nombre").execute()
            registros = response.data or []

            # SELECT categoria_id FROM productos WHERE disponible = TRUE;
            response_productos = self.supabase.table("productos").select("categoria_id").eq("disponible",True).execute()
            productos = response_productos.data or []

            # A cada categoría se le cuenta cuántos productos disponibles tiene
            for registro in registros:
                total = 0
                for producto in productos:
                    if producto["categoria_id"] == registro["id"]: # type: ignore
                        total = total + 1
                registro["total"] = total # type: ignore
                id_num = int(registro["id"]) # type: ignore
                registro["id"] = self.generarHash(id_num) # type: ignore
            categorias = cast(list[dict[str, Any]],registros)
            return categorias
        except Exception as error:
            logger.error("ERROR 102: %s", error)
            print(f"ERROR 102: {str(error)}")
            return []


if __name__ == "__main__":
    model_categorias = ModelCategorias()
    print(model_categorias.obtenerCategorias())
    print(model_categorias.obtenerCategoriasConTotal())
    