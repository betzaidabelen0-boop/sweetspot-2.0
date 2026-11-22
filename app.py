import web
import logging

# Controladores públicos (lo que ve el cliente)
from mvc.controllers.publico.index import Index
from mvc.controllers.publico.productos import Productos

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
    # Admin (pendiente)
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
    