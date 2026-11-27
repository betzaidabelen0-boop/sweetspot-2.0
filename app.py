import web
import logging

# Controladores públicos (lo que ve el cliente)
from mvc.controllers.publico.index import Index
from mvc.controllers.publico.productos import Productos
from mvc.controllers.publico.producto import Producto
# Carrito (Kim): Carrito pinta la página, CarritoAgregar recibe el botón "Agregar a mi carrito"
from mvc.controllers.publico.carrito import Carrito, CarritoAgregar

#ALEEEEEEEE (vistas de los paquetes)
render = web.template.render('mvc/views/paquetes/')

class Paquetes:
    def GET(self):
        return render.paquetes()
    
class DetallePaquete:
    def GET(self):
        return render.detalle_paquete()


# Controladores del administrador: se importan aquí cuando existan
# from mvc.controllers.admin.login import Login

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",  # Evita errores con tildes o caracteres especiales
)

web.config.debug = False

urls = (
    # Público
    '/', 'Index',
    '/productos', 'Productos',
    '/producto', 'Producto',
    
    # url de ALEEEEE (paquetes)
    '/paquetes', 'Paquetes',
    '/detalle_paquete', 'DetallePaquete',

    # Carrito (Kim)
    '/carrito', 'Carrito',
    '/carrito/agregar', 'CarritoAgregar', 


    # Admin (pendiente)

)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
    