import json
import web
from mvc.models.model_productos import ModelProductos

render = web.template.render('mvc/views/publico', base='template')

EVENTO = {"nombre": "Mi evento", "invitados": 80, "estilo": "romántico",
          "fecha": "12 dic 2026", "ciudad": "Ciudad de México"}
MONTAJE = 1200
MINIMO = 20


def leer():
    try:
        carrito = json.loads(web.cookies().get("carrito", "{}"))
    except ValueError:
        return {}
    return carrito if isinstance(carrito, dict) else {}


def guardar(carrito):
    web.setcookie("carrito", json.dumps(carrito), 604800, path="/")


def dinero(n):
    return f"{n:,.0f}" if n == int(n) else f"{n:,.2f}"


def traer(modelo, id_producto):
    registros = modelo.buscarProducto(id_producto)
    return registros[0] if registros else None


def minimo_de(producto):
    return producto.get("pedido_minimo") or MINIMO


class Carrito:

    def GET(self):
        modelo = ModelProductos()
        productos, total_piezas, subtotal = [], 0, 0

        for id_producto, cantidad in leer().items():
            producto = traer(modelo, id_producto)
            if not producto:
                continue

            precio = float(producto["precio"])
            producto["imagen"] = producto.get("fotografia")
            producto["minimo"] = minimo_de(producto)
            producto["cantidad"] = cantidad
            producto["precio_texto"] = dinero(precio)
            producto["subtotal_texto"] = dinero(precio * cantidad)

            productos.append(producto)
            total_piezas += cantidad
            subtotal += precio * cantidad

        datos = web.storage({
            "productos": productos,
            "evento": EVENTO,
            "total_piezas": total_piezas,
            "subtotal_texto": dinero(subtotal),
            "montaje_texto": dinero(MONTAJE),
            "total_texto": dinero(subtotal + MONTAJE),
        })

        return render.carrito(datos) # type: ignore

    def POST(self):
        entrada = web.input(id_producto="", accion="")
        id_producto = entrada.id_producto
        carrito = leer()

        if id_producto in carrito:
            producto = traer(ModelProductos(), id_producto)
            minimo = minimo_de(producto) if producto else MINIMO

            if entrada.accion == "sumar":
                carrito[id_producto] += 1
            elif entrada.accion == "restar" and carrito[id_producto] > minimo:
                carrito[id_producto] -= 1
            elif entrada.accion == "quitar":
                del carrito[id_producto]

        guardar(carrito)
        raise web.seeother('/carrito')


class CarritoAgregar:

    def POST(self):
        entrada = web.input(id="", cantidad="")
        if not entrada.id:
            raise web.badrequest()

        producto = traer(ModelProductos(), entrada.id)
        if not producto:
            raise web.notfound()

        minimo = minimo_de(producto)
        cantidad = int(entrada.cantidad) if entrada.cantidad.isdigit() else minimo

        carrito = leer()
        carrito[entrada.id] = max(cantidad, minimo)
        guardar(carrito)
        return "ok"