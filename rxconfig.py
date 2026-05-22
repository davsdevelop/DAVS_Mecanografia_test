import reflex as rx

config = rx.Config(
    app_name="DAVS_Mecanografia_test",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)