import cv2
import numpy as np
import time

# Размер матрицы
W, H = 64, 64
SCALE = 12


# Пиксельная матрица (H, W, RGB)
matrix = np.zeros((H, W, 3), dtype=np.uint8)

# Координаты пикселя
x = 1
y = 1

# Устанавливаем пиксель (белый)

while x != 64:
    matrix[x, y] = (255, 255, 255)
    x =+ 1



# Увеличиваем для отображения
display = cv2.resize(
    matrix,
    (W * SCALE, H * SCALE),
    interpolation=cv2.INTER_NEAREST
)

cv2.imshow("Pixel Matrix", display)
cv2.waitKey(0)
cv2.destroyAllWindows()