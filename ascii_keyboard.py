from pynput import keyboard

class ASCIIKeyboard:
    def __init__(self):
        self.last_char = None
        self.last_code = 0  # Добавляем хранение кода напрямую
        self.rel_code = 0
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def _convert_to_ascii(self, key):
        """Вспомогательный метод для конвертации клавиши в ASCII-код"""
        try:
            # Для обычных букв и цифр
            if hasattr(key, 'char') and key.char is not None:
                return ord(key.char)
            
            # Словарь соответствия для служебных клавиш
            special_keys = {
                keyboard.Key.enter: 13,
                keyboard.Key.backspace: 8,
                keyboard.Key.tab: 9,
                keyboard.Key.esc: 27,
                keyboard.Key.space: 32,
                keyboard.Key.delete: 127,
                keyboard.Key.up: 38,
                keyboard.Key.down: 40,
                keyboard.Key.left: 37,
                keyboard.Key.right: 39,
            }
            return special_keys.get(key, 0) # Возвращает 0, если клавиша не в списке
        except Exception:
            return 0

    def _on_press(self, key):
        self.last_code = self._convert_to_ascii(key)
        # Сохраняем символ для метода get_char, если это возможно
        self.last_char = key.char if hasattr(key, 'char') else None

    def _on_release(self, key):
        self.rel_code = self._convert_to_ascii(key)

    def start(self):
        self.listener.start()

    def get_char(self):
        temp = self.last_char
        self.last_char = None
        return temp

    def get_ascii_code(self):
        """Возвращает ASCII-код (включая служебные) и обнуляет данные"""
        temp = self.last_code
        self.last_code = 0
        return temp

    def get_ascii_rel(self):
        """Возвращает ASCII-код отпущенной клавиши и обнуляет данные"""
        temp = self.rel_code
        self.rel_code = 0
        return temp