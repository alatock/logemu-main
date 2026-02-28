import pygame
import numpy as np
import threading

class PixelWindow:
    def __init__(self, width, height, scale=10, title="Pixel Window", fps=60):
        self.width = width
        self.height = height
        self.scale = scale
        self.fps = fps
        self.running = True
        self._lock = threading.Lock()
        
        # Матрица данных
        self.matrix = np.zeros((height, width), dtype=np.uint8)

        # Запускаем Pygame в главном потоке, а для управления логикой 
        # (если нужно) можно создать отдельный поток. 
        # Но отрисовку оставим здесь.
        self._init_pygame(title)

    def _init_pygame(self, title):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        pygame.display.set_caption(title)
        self.surface = pygame.Surface((self.width, self.height))
        self.clock = pygame.time.Clock()

    def set_pixel(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            with self._lock:
                self.matrix[y, x] = 1 if value else 0

    def fill(self, value):
        with self._lock:
            self.matrix[:, :] = 1 if value else 0

    def render(self):
        """Метод отрисовки — вызывается ТОЛЬКО в основном цикле"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        with self._lock:
            # Создаем RGB массив. В Pygame surfarray использует (X, Y)
            # Транспонируем матрицу, чтобы она соответствовала осям Pygame
            rgb_matrix = np.stack([self.matrix.T * 255] * 3, axis=-1)
            pygame.surfarray.blit_array(self.surface, rgb_matrix)

        # Масштабируем и выводим
        scaled = pygame.transform.scale(
            self.surface, 
            (self.width * self.scale, self.height * self.scale)
        )
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()

    def run(self):
        """Основной цикл приложения"""
        while self.running:
            self.render()
            self.clock.tick(self.fps)
        pygame.quit()

# Пример использования:
if __name__ == "__main__":
    win = PixelWindow(64, 64, scale=8)
    
    # Можно запустить поток, который будет что-то рисовать в фоне
    def background_logic():
        x = 0
        while win.running:
            win.set_pixel(x % 64, 32, 1)
            x += 1
            import time
            time.sleep(0.05)

    logic_thread = threading.Thread(target=background_logic, daemon=True)
    logic_thread.start()

    # Основной поток занят только окном
    win.run()