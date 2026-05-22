import reflex as rx

config = rx.Config(
    app_name="main",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)