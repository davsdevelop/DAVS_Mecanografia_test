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
    is_finished: bool =False
    start_time: float = 0.0
    end_time: float = 0.0



    @rx.event
    def load_data(self):
        path = Path(__file__).parent / "paragraphs.json"
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.paragraph_text = [p["text"] for p in data["paragraphs"]]
        self.target_text = random.choice(self.paragraph_text)


    @rx.var
    def display_chars(self) -> list[list[str]]:
        cursor = len(self.typed_text)
        result = []
        for i, char in enumerate(self.target_text):
            #Determinar el estado
            if i < cursor:
                state = "correct" if self.typed_text[i] == char else "wrong"
            elif i == cursor:
                state = "cursor"
            else:
                state = "pending"

            #Contruir el css
            suffix = "-space" if char == " " and state in ("wrong", "cursor") else ""
            css = f"char-{state}{suffix}"
            result.append([char, css])

        return result
    

    @rx.event
    def key_input(self, value: str):
        if self.is_finished:
            return
        
        # Bloquear paste: si el salto es mayor a 2 caracteres, ignorar
        if len(value) - len(self.typed_text) > 2:
            return

        value = value[:len(self.target_text)]

        if not self.is_started and value:
            self.is_started = True
            self.start_time = time.time()

        self.current_input = value
        self.typed_text = value

        if len(value) == len(self.target_text):
            self.is_finished = True
            self.end_time = time.time()


    @rx.var
    def progress_bar(self) -> str:
        if not self.target_text:
            return "0%"

        pct = min(len(self.typed_text) / len(self.target_text) * 100, 100.0)
        return f"{pct:.1f}%"
    


    def _time_elapsed(self) -> float:
        if not self.is_started:
            return 0.0

        if self.is_finished:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    

    def _correct_count(self) -> int:
        contador = 0

        for typed_char, target_char in zip(self.typed_text, self.target_text):
            if typed_char == target_char:
                contador += 1
        return contador
    
    @rx.event
    def handle_key_down(self, key: str):
        if key == "Tab":
            return TypingState.reset_text()

    @rx.var
    def wpm(self) -> str:
        elapsed = self._time_elapsed()
        if elapsed == 0 or not self.is_started:
            return "0"
        wpm = (self._correct_count() / 5.0) / (elapsed / 60.0)
        return str(int(wpm))


    @rx.var
    def accuracy(self) -> str:
        if not self.typed_text:
            return "100"
        pct = self._correct_count() / len(self.typed_text) * 100
        return str(round(pct, 1))
    

    @rx.var
    def error_chars(self) -> int:
        return len(self.typed_text) - self._correct_count()
    
    @rx.var
    def correct_chars(self) -> int:
        return self._correct_count()
    
    @rx.var
    def time_str(self) -> str:
        return str(round(self._time_elapsed(), 1))
    


    @rx.event
    def reset_text(self):
        self.typed_text = ""
        self.current_input = ""
        self.is_started = False
        self.is_finished = False
        self.start_time = 0.0
        self.end_time = 0.0
        if self.paragraph_text:
            self.target_text = random.choice(self.paragraph_text)


    @rx.var
    def streak(self) -> int:
        count = 0
        for typed_char, target_char in zip(self.typed_text, self.target_text):
            if typed_char == target_char:
                count += 1
            else:
                count = 0 
        return count