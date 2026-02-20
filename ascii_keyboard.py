from pynput import keyboard

class ASCIIKeyboard:
    def __init__(self):
        self.last_char = None
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def _on_press(self, key):
        
        try:
            # Обычные символы (буквы, цифры, знаки)
            self.last_char = key.char
        except AttributeError:
            # Спец-клавиши (Enter, Shift и т.п.)
            self.last_char = None

    def _on_release(self, key):
        self.last_char = None
        pass

    def start(self):
        self.listener.start()

    def get_char(self):
        """
        Возвращает ASCII-символ последней нажатой клавиши
        или None, если это не символ
        """
        return self.last_char

    def get_ascii_code(self):
        """
        Возвращает ASCII-код символа или None
        """
        if self.last_char is not None:
            return ord(self.last_char)
        else: return 0