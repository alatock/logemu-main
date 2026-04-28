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
        
        # Внутренняя матрица по умолчанию
        self.matrix = np.zeros((height, width), dtype=np.uint8)

        self._init_pygame(title)

    def _init_pygame(self, title):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        pygame.display.set_caption(title)
        self.surface = pygame.Surface((self.width, self.height))
        self.clock = pygame.time.Clock()
    def render(self, external_matrix=None):
        """
        Метод отрисовки. 
        Если передана external_matrix, она копируется во внутренний буфер.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        with self._lock:
            # Если пришла новая матрица из вызывающего файла — обновляем внутреннюю
            if external_matrix is not None:
                # Важно: приводим к типу uint8, если переданы bool или float
                self.matrix = np.array(external_matrix, dtype=np.uint8)

            # Превращаем 0/1 в 0/255 и создаем RGB (3 канала)
            # .T нужен, так как surfarray ожидает (width, height)
            rgb_matrix = np.stack([self.matrix.T * 255] * 3, axis=-1)
            pygame.surfarray.blit_array(self.surface, rgb_matrix)

        # Масштабирование и вывод на экран
        scaled = pygame.transform.scale(
            self.surface, 
            (self.width * self.scale, self.height * self.scale)
        )
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()

    def run(self):
        """Стандартный цикл, если не передаем матрицу извне вручную"""
        while self.running:
            self.render()
            self.clock.tick(self.fps)
        pygame.quit()


