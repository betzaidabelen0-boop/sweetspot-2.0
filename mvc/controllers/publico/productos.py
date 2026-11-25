import web
from urllib.parse import urlencode
from mvc.models.model_productos import ModelProductos
from mvc.models.model_categorias import ModelCategorias

render = web.template.render('mvc/views/publico', base='template')

class Productos:

    def GET(self):

        # Lee lo que llega en la URL: /productos?q=...&categoria=...&orden=...&pagina=...
        entrada = web.input(q="", categoria="", orden="recientes", pagina="1")
        buscar = entrada.q.strip()
        id_categoria = entrada.categoria
        orden = entrada.orden
        pagina = int(entrada.pagina) if entrada.pagina.isdigit() else 1
        if pagina < 1:
            pagina = 1

        por_pagina = 6

        model_productos = ModelProductos()
        model_categorias = ModelCategorias()

        # Almacena en productos los registros recibidos de Supabase
        productos, total = model_productos.obtenerProductos(id_categoria, buscar, orden, pagina, por_pagina)

        # Si la página pedida ya no existe, se regresa a la primera
        if len(productos) == 0 and pagina > 1:
            pagina = 1
            productos, total = model_productos.obtenerProductos(id_categoria, buscar, orden, pagina, por_pagina)

        categorias = model_categorias.obtenerCategoriasConTotal()

        # Total de productos disponibles (opción "Todos los productos")
        total_general = 0
        for categoria in categorias:
            total_general = total_general + categoria["total"]

        # Total de páginas del catálogo
        total_paginas = (total + por_pagina - 1) // por_pagina
        if total_paginas < 1:
            total_paginas = 1

        # Precio listo para mostrar: $15 o $15.50
        for producto in productos:
            precio = float(producto["precio"])
            if precio == int(precio):
                producto["precio_texto"] = f"${int(precio)}"
            else:
                producto["precio_texto"] = f"${precio:.2f}"

        # Filtros actuales para los enlaces de la paginación
        filtros = urlencode({"q": buscar, "categoria": id_categoria, "orden": orden})

        datos = {
            "productos": productos,
            "categorias": categorias,
            "total_general": total_general,
            "buscar": buscar,
            "id_categoria": id_categoria,
            "orden": orden,
            "pagina": pagina,
            "total_paginas": total_paginas,
            "filtros": filtros,
        }

        # Envia a productos.html los datos de supabase
        return render.productos(datos) # type: ignore
    