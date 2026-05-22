import reflex as rx

from .components import header, typing_area, stats_bar
from .state import TypingState


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
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
        ),
    )


app = rx.App(stylesheets=["/styles.css"])
app.add_page(index, on_load=TypingState.load_data)
