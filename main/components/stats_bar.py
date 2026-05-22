import reflex as rx

from ..state import TypingState


def _stat(label: str, value, unit: str = "") -> rx.Component:
    return rx.box(
        rx.text(label, class_name="stat-label"),
        rx.box(
            rx.text(value, class_name="stat-value"),
            rx.text(unit, class_name="stat-unit"),
            class_name="stat-value-row",
        ),
        class_name="stat-card",
    )


def stats_bar() -> rx.Component:
    return rx.box(
        _stat("wpm", TypingState.wpm, "wpm"),
        _stat("precisión", TypingState.accuracy, "%"),
        _stat("correctos", TypingState.correct_chars, ""),
        _stat("errores", TypingState.error_chars, ""),
        _stat("tiempo", TypingState.time_str, "s"),
        _stat("racha", TypingState.streak, ""),

        class_name="stats-bar"
    )