import reflex as rx
from ..state import TypingState


def _render_char(item: list) -> rx.Component:
    return rx.el.span(item[0], class_name=item[1])


def typing_area() -> rx.Component:
    return rx.box(
        # Barra de progreso
        rx.box(
            rx.box(class_name="progress-fill", width=TypingState.progress_bar),
            class_name="progress-bar",
        ),
        # Texto con colores por carácter
        rx.box(
            rx.foreach(TypingState.display_chars, _render_char),
            class_name="text-display",
            display="inline-block",
        ),
        # Input de escritura
        # NOTA: on_change envía al servidor en cada tecla (causa del lag).
        # Se usa debounce_timeout=0 para que sea inmediato, pero el lag
        # viene del round-trip WebSocket a Render.
        # La solución real es mover la lógica al cliente con rx.script +
        # custom JS si se necesita eliminar el lag completamente.
        # Por ahora, el mayor impacto viene de reducir el tamaño del payload
        # (stats solo al finalizar) y simplificar display_chars.
        rx.input(
            value=TypingState.current_input,
            on_change=TypingState.key_input,
            auto_focus=True,
            disabled=TypingState.is_finished,
            class_name="typing-input",
            debounce_timeout=0,
            on_key_down=TypingState.handle_key_down,
            # Prevenir comportamientos del browser que agregan lag
            spell_check=False,
            auto_complete=False,
        ),
    )