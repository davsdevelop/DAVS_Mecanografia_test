import reflex as rx
from ..state import TypingState

def header() -> rx.Component:
    return rx.box(
        rx.box(
            rx.image("/mecanografia_test.png", width="120px"),
        rx.box(
            rx.text("Mecanografía TEST", class_name="logo-text", width="100%", text_align="center"),
            rx.text("Optimiza tu velocidad, eleva tu precisión.", class_name="logo-accent", width="100%", text_align="center"),
            class_name="logo-texts",
        ),
            rx.box(
                rx.button(
                    rx.icon("rotate-ccw", size=25),
                    "Reiniciar",
                    on_click=TypingState.reset_text,
                    variant="soft",
                    class_name="btn",
                ),
                class_name="header-controls",
            ),
            class_name="header-inner",
        ),
        class_name="header",
    )