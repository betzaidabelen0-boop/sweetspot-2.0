# sweetspot-2.0
se me acabaron mis horas de codespace jaja, sorry

sweetspot/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── database/
│   └── schema.sql
│
├── mvc/ 
│     models/
│   ├── conexion.py
│   ├── usuarios.py
│   ├── productos.py
│   ├── paquetes.py
│   ├── calendario.py
│   └── reservaciones.py
│
├── controllers/
│   ├── publico/
│   │   ├── inicio.py
│   │   ├── productos.py
│   │   ├── paquetes.py
│   │   ├── carrito.py
│   │   └── agendamiento.py
│   └── admin/
│       ├── acceso.py
│       ├── productos.py
│       ├── paquetes.py
│       ├── calendario.py
│       └── solicitudes.py
│
├── utils/
│   ├── seguridad.py
│   ├── validaciones.py
│   └── carrito.py
│
├── views/
│   ├── layout.html
│   ├── layout_admin.html
│   ├── publico/
│   │   ├── inicio.html
│   │   ├── productos.html
│   │   ├── producto.html
│   │   ├── paquetes.html
│   │   ├── paquete.html
│   │   ├── carrito.html
│   │   ├── agendamiento.html
│   │   ├── solicitud_enviada.html
│   │   └── error.html
│   └── admin/
│       ├── login.html
│       ├── productos.html
│       ├── producto_form.html
│       ├── paquetes.html
│       ├── paquete_form.html
│       ├── calendario.html
│       └── solicitud.html
│
└── static/
    ├── css/
    │   ├── variables.css
    │   ├── estilo.css
    │   └── admin.css
    ├── js/
    │   ├── calendario.js
    │   ├── cantidad.js
    │   └── confirmar.js
    └── img/
    