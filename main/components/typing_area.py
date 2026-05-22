import reflex as rx
from ..state import TypingState


def _render_char(item: list) -> rx.Component:
    return rx.el.span(item[0], class_name=item[1])

def typing_area() -> rx.Component:
    return rx.box(
        #Barra de progreso
        rx.box(
            rx.box(class_name="progress-fill", width=TypingState.progress_bar),
            class_name="progress-bar",
        ),
        #Texto con colores por caracter
        rx.box(
            rx.foreach(TypingState.display_chars, _render_char),
            class_name="text-display",
            display="inline-block"
        ),
        #Input de escritura
        rx.input(
            value=TypingState.current_input,
            on_change=TypingState.key_input,
            auto_focus=True,
            disabled=TypingState.is_finished,
            class_name="typing-input",
            debounce_timeout=0,
            on_key_down=TypingState.handle_key_down,
        )
    )