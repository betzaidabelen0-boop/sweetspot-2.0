import web
from mvc.models.model_productos import ModelProductos
from mvc.controllers.publico.carrito import dinero, minimo_de

render = web.template.render('mvc/views/publico', base='template')


class Producto:
    """Ficha de producto: /producto?id=<id con hash>"""

    def GET(self):
        entrada = web.input(id="")
        if not entrada.id:
            raise web.seeother('/productos')

        registros = ModelProductos().buscarProducto(entrada.id)
        if not registros or not registros[0].get("disponible", True):
            raise web.notfound()

        producto = registros[0]
        precio = float(producto["precio"])
        minimo = minimo_de(producto)

        producto["imagen"] = producto.get("fotografia") or ""
        producto["descripcion"] = producto.get("descripcion") or ""
        producto["minimo"] = minimo
        producto["precio_num"] = precio
        producto["precio_texto"] = dinero(precio)
        producto["subtotal_texto"] = dinero(precio * minimo)

        return render.producto(producto) # type: ignore
