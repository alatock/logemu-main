from pynput import keyboard

class ASCIIKeyboard:
    def __init__(self):
        self.last_char = None
        self.rel_char = None
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def _on_press(self, key):
        try:
            self.last_char = key.char
        except AttributeError:
            self.last_char = None

    def _on_release(self, key):
        try:
            self.rel_char = key.char
        except AttributeError:
            self.rel_char = None

    def start(self):
        self.listener.start()

    def get_char(self):
        """Возвращает символ и ОБНУЛЯЕТ его в памяти класса"""
        temp = self.last_char
        self.last_char = None  # Обнуляем данные
        return temp

    def get_ascii_code(self):
        """Возвращает ASCII-код и ОБНУЛЯЕТ данные о нажатии"""
        if self.last_char:
            code = ord(self.last_char)
            self.last_char = None  # Обнуляем после получения кода
            return code
        return 0

    def get_ascii_rel(self):
        """Возвращает ASCII-код отпущенной клавиши и ОБНУЛЯЕТ его"""
        if self.rel_char:
            code = ord(self.rel_char)
            self.rel_char = None  # Обнуляем после получения кода
            return code
        return 0