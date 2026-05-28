import reflex as rx

config = rx.Config(
    app_name="main",
    # Permite que el frontend se comunique con este backend
    cors_allowed_origins=[
        "*"
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)