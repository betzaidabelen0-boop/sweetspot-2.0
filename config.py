import os
from dotenv import load_dotenv

load_dotenv()

# Nombre del negocio (se usa en las vistas)
NOMBRE_SITIO = "SweetsPot"

# Carpetas de vistas (web.py las lee desde la raíz del proyecto)
VISTAS_PUBLICO = "mvc/views/publico"
VISTAS_ADMIN = "mvc/views/admin"

# Supabase: se leen del archivo .env (nunca se suben a GitHub)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Clave para firmar los id que viajan en las URL (ponla también en el .env)
SECRET_KEY = os.environ.get("SECRET_KEY", "cambiar-esta-clave").encode("utf-8")

# Catálogo
PRODUCTOS_POR_PAGINA = 6
