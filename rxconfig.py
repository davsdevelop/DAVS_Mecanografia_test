import reflex as rx

config = rx.Config(
    app_name="main",
    # 1. FORZAMOS A QUE EL FRONTEND APUNTE AL BACKEND CORRECTO
    api_url="https://davs-mecanografia-test.onrender.com", 
    # 2. PERMITIMOS QUE EL BACKEND RECIBA LA CONEXIÓN
    cors_allowed_origins=[
        "*"
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)