import reflex as rx
import json
import random
import time
from pathlib import Path


class TypingState(rx.State):
    paragraph_text: list[str] = []
    target_text: str = ""
    current_input: str = ""
    typed_text: str = ""
    is_started: bool = False
    is_finished: bool = False
    start_time: float = 0.0
    end_time: float = 0.0

    # Stats calculadas solo al finalizar (no son @rx.var en tiempo real)
    final_wpm: str = "0"
    final_accuracy: str = "100"
    final_correct_chars: int = 0
    final_error_chars: int = 0
    final_time_str: str = "0"
    final_streak: int = 0

    @rx.event
    def load_data(self):
        path = Path(__file__).parent / "paragraphs.json"
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.paragraph_text = [p["text"] for p in data["paragraphs"]]
        self.target_text = random.choice(self.paragraph_text)

    # ── display_chars: solo re-serializa cuando typed_text cambia ──────────
    # Se mantiene como @rx.var pero ahora las stats NO se recalculan aquí.
    @rx.var
    def display_chars(self) -> list[list[str]]:
        cursor = len(self.typed_text)
        result = []
        for i, char in enumerate(self.target_text):
            if i < cursor:
                state = "correct" if self.typed_text[i] == char else "wrong"
            elif i == cursor:
                state = "cursor"
            else:
                state = "pending"
            suffix = "-space" if char == " " and state in ("wrong", "cursor") else ""
            css = f"char-{state}{suffix}"
            result.append([char, css])
        return result

    @rx.var
    def progress_bar(self) -> str:
        if not self.target_text:
            return "0%"
        pct = min(len(self.typed_text) / len(self.target_text) * 100, 100.0)
        return f"{pct:.1f}%"

    # ── Helpers internos (no son @rx.var, no se serializan) ────────────────
    def _time_elapsed(self) -> float:
        if not self.is_started:
            return 0.0
        if self.is_finished:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    def _correct_count(self) -> int:
        return sum(
            1 for t, c in zip(self.typed_text, self.target_text) if t == c
        )

    def _max_streak(self) -> int:
        """Racha máxima de caracteres correctos consecutivos (bug fix)."""
        max_s = 0
        current = 0
        for typed_char, target_char in zip(self.typed_text, self.target_text):
            if typed_char == target_char:
                current += 1
                max_s = max(max_s, current)
            else:
                current = 0
        return max_s

    def _compute_final_stats(self):
        """Calcula y guarda las stats solo al finalizar el test."""
        elapsed = self._time_elapsed()
        correct = self._correct_count()

        if elapsed > 0:
            wpm = (correct / 5.0) / (elapsed / 60.0)
            self.final_wpm = str(int(wpm))
        else:
            self.final_wpm = "0"

        total_typed = len(self.typed_text)
        if total_typed > 0:
            pct = correct / total_typed * 100
            self.final_accuracy = str(round(pct, 1))
        else:
            self.final_accuracy = "100"

        self.final_correct_chars = correct
        self.final_error_chars = total_typed - correct
        self.final_time_str = str(round(elapsed, 1))
        self.final_streak = self._max_streak()

    # ── Evento principal: se dispara en cada tecla ──────────────────────────
    @rx.event
    def key_input(self, value: str):
        if self.is_finished:
            return

        # Anti-paste corregido: solo permite diferencia de 1 carácter (bug fix)
        if len(value) - len(self.typed_text) > 1:
            return

        value = value[: len(self.target_text)]

        if not self.is_started and value:
            self.is_started = True
            self.start_time = time.time()

        self.current_input = value
        self.typed_text = value

        if len(value) == len(self.target_text):
            self.is_finished = True
            self.end_time = time.time()
            # Solo calculamos stats al terminar, no en cada tecla
            self._compute_final_stats()

    @rx.event
    def handle_key_down(self, key: str):
        if key == "Tab":
            return TypingState.reset_text()

    @rx.event
    def reset_text(self):
        self.typed_text = ""
        self.current_input = ""
        self.is_started = False
        self.is_finished = False
        self.start_time = 0.0
        self.end_time = 0.0
        self.final_wpm = "0"
        self.final_accuracy = "100"
        self.final_correct_chars = 0
        self.final_error_chars = 0
        self.final_time_str = "0"
        self.final_streak = 0
        if self.paragraph_text:
            self.target_text = random.choice(self.paragraph_text)

    # ── vars de stats: ahora apuntan a los valores finales pre-calculados ──
    @rx.var
    def wpm(self) -> str:
        return self.final_wpm

    @rx.var
    def accuracy(self) -> str:
        return self.final_accuracy

    @rx.var
    def correct_chars(self) -> int:
        return self.final_correct_chars

    @rx.var
    def error_chars(self) -> int:
        return self.final_error_chars

    @rx.var
    def time_str(self) -> str:
        return self.final_time_str

    @rx.var
    def streak(self) -> int:
        return self.final_streak