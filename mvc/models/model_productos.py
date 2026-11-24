import os
from supabase import create_client, Client
from dotenv import load_dotenv
import hashlib
import hmac
from typing import Any, cast

import logging

load_dotenv()

logger = logging.getLogger(__name__)

class ModelProductos:

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

    def obtenerProductos(self,id_categoria:str="",buscar:str="",orden:str="populares",pagina:int=1,por_pagina:int=6,solo_disponibles:bool=True):
        # Regresa los productos de la página y el total de productos que coinciden
        productos: list[dict[str,Any]]
        try:
            # SELECT productos.*, categorias.nombre FROM productos JOIN categorias ON categorias.id = productos.categoria_id
            # WHERE disponible = TRUE AND categoria_id = ? AND nombre ILIKE ? ORDER BY ? LIMIT ? OFFSET ?;
            consulta = self.supabase.table("productos").select("*, categorias(nombre)",count="exact") # type: ignore

            if solo_disponibles:
                consulta = consulta.eq("disponible",True)

            if id_categoria != "":
                id = self.validarHash(id_categoria)
                consulta = consulta.eq("categoria_id",id)

            if buscar != "":
                consulta = consulta.ilike("nombre",f"%{buscar}%")

            if orden == "precio_menor":
                consulta = consulta.order("precio")
            elif orden == "precio_mayor":
                consulta = consulta.order("precio",desc=True)
            else:
                consulta = consulta.order("id")

            inicio = (pagina - 1) * por_pagina
            fin = inicio + por_pagina - 1
            response = consulta.range(inicio,fin).execute()

            registros = response.data or []
            for registro in registros:
                registro["categoria"] = registro["categorias"]["nombre"] # type: ignore
                registro["id"] = self.generarHash(int(registro["id"])) # type: ignore
                registro["categoria_id"] = self.generarHash(int(registro["categoria_id"])) # type: ignore
            productos = cast(list[dict[str, Any]],registros)
            return productos, (response.count or 0)
        except Exception as error:
            logger.error("ERROR 101: %s", error)
            print(f"ERROR 101: {str(error)}")
            return [], 0

    def buscarProducto(self,id_producto:str):
        try:
            id = self.validarHash(id_producto)
            # SELECT productos.*, categorias.nombre FROM productos JOIN categorias ON categorias.id = productos.categoria_id WHERE productos.id = ?;
            response = self.supabase.table("productos").select("*, categorias(nombre)").eq("id",id).execute()
            registros = response.data or []
            for registro in registros:
                registro["categoria"] = registro["categorias"]["nombre"] # type: ignore
                registro["id"] = self.generarHash(int(registro["id"])) # type: ignore
                registro["categoria_id"] = self.generarHash(int(registro["categoria_id"])) # type: ignore
            return registros
        except Exception as error:
            logger.error("ERROR 102: %s", error)
            print(f"ERROR 102: {str(error)}")
            return []

    def insertarProducto(self,nombre:str,id_categoria:str,precio:float,descripcion:str|None=None,fotografia:str|None=None,sabores:str|None=None,ingredientes:str|None=None,medidas_cantidad:str|None=None,pedido_minimo:int=1,disponible:bool=True):
        try:
            id = self.validarHash(id_categoria)
            # INSERT INTO productos(nombre,categoria_id,precio,descripcion,fotografia,sabores,ingredientes,medidas_cantidad,pedido_minimo,disponible) VALUES(?,?,?,?,?,?,?,?,?,?);
            data = {
                "nombre":nombre,
                "categoria_id":id,
                "precio":precio,
                "descripcion":descripcion,
                "fotografia":fotografia,
                "sabores":sabores,
                "ingredientes":ingredientes,
                "medidas_cantidad":medidas_cantidad,
                "pedido_minimo":pedido_minimo,
                "disponible":disponible
            }
            response = self.supabase.table("productos").insert(data).execute()
            return response.data
        except Exception as error:
            logger.error("ERROR 103: %s", error)
            print(f"ERROR 103: {str(error)}")

    def borrarProducto(self,id_producto:str):
        try:
            id = self.validarHash(id_producto)
            # DELETE FROM productos WHERE id = ?;
            response = self.supabase.table("productos").delete().eq("id",id).execute()
            return response.data
        except Exception as error:
            logger.error("ERROR 104: %s", error)
            print(f"ERROR 104: {str(error)}")

    def actualizarProducto(self,id_producto:str,nombre:str,id_categoria:str,precio:float,descripcion:str|None=None,fotografia:str|None=None,sabores:str|None=None,ingredientes:str|None=None,medidas_cantidad:str|None=None,pedido_minimo:int=1,disponible:bool=True):
        try:
            id = self.validarHash(id_producto)
            id_cat = self.validarHash(id_categoria)
            # UPDATE productos SET nombre=?, categoria_id=?, precio=?, descripcion=?, fotografia=?, sabores=?, ingredientes=?, medidas_cantidad=?, pedido_minimo=?, disponible=? WHERE id=?;
            data = {
                "nombre":nombre,
                "categoria_id":id_cat,
                "precio":precio,
                "descripcion":descripcion,
                "fotografia":fotografia,
                "sabores":sabores,
                "ingredientes":ingredientes,
                "medidas_cantidad":medidas_cantidad,
                "pedido_minimo":pedido_minimo,
                "disponible":disponible
            }
            response = self.supabase.table("productos").update(data).eq("id",id).execute()
            return response.data
        except Exception as error:
            logger.error("ERROR 105: %s", error)
            print(f"ERROR 105: {str(error)}")


if __name__ == "__main__":
    model_productos = ModelProductos()
    productos, total = model_productos.obtenerProductos()
    print(total, productos)
    #print(model_productos.buscarProducto(productos[0]["id"]))
    #print(model_productos.insertarProducto("Lucas muecas",productos[0]["categoria_id"],15,pedido_minimo=20))
    #print(model_productos.actualizarProducto(productos[0]["id"],"Lucas muecas",productos[0]["categoria_id"],18))
    #print(model_productos.borrarProducto(productos[0]["id"]))
    