import reflex as rx
from ..state import TypingState

def header() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(
                rx.text("Reflex", class_name="logo-text"),
                rx.text("Type", class_name="logo-accent"),
                class_name="logo"
            ),
            rx.box(
                rx.button(
                    rx.icon("rotate-ccw", size=15),
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