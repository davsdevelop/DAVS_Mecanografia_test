import reflex as rx
from .components import header, typing_area, stats_bar
from .state import TypingState


def index() -> rx.Component:
    return rx.box(
        # Script de feedback local para eliminar lag al escribir
        # Lee assets/typing_local.js y lo inyecta en el cliente
        rx.script(src="/typing_local.js"),
        header(),
        rx.box(
            rx.cond(
                TypingState.is_finished,
                rx.box(
                    rx.text("¡Test completado!", class_name="result-title"),
                    rx.text("Estos son tus resultados", class_name="result-subtitle"),
                    stats_bar(),
                    class_name="result-block",
                ),
                rx.box(),
            ),
            typing_area(),
            class_name="content",
            flex="1",
        ),
        # ==== FOOTER ====
        rx.box(
            rx.text(
                "Desarrollado por: Diego Videla Silva",
                size="2",
                color="#464649",
            ),
            rx.image("/DAVS.png", width="70px"),
            rx.text(
                "© 2026 Mecanografía TEST. Todos los derechos reservados.",
                size="2",
                color="#464649",
                text_align="center",
            ),
            width="100%",
            background_color="#c7cbd2",
            display="flex",
            # CAMBIO: Columna centrada en móvil, fila espaciada en escritorio
            flex_direction=rx.breakpoints(initial="column", sm="row"),
            justify_content="space-between",
            align_items="center",
            padding_x="4",
            padding_y=rx.breakpoints(initial="4", sm="2"),
            gap="3",
        ),
        min_height="100vh",
        display="flex",
        flex_direction="column",
    )


app = rx.App(stylesheets=["/styles.css"])
app.add_page(index, on_load=TypingState.load_data)