import matplotlib.pyplot as plt  # Импортируем как plt для вызова plt.show()
from matplotlib.pyplot import imshow
from PIL import Image
import numpy as np

# Функция для рисования отрезка между двумя точками
def draw_line(img, x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        img.putpixel((x0, y0), color)
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# Функция для рисования сетки
def draw_grid(img, step, color):
    width, height = img.size
    # Вертикальные линии
    for x in range(0, width, step):
        draw_line(img, x, 0, x, height-1, color)
    # Горизонтальные линии
    for y in range(0, height, step):
        draw_line(img, 0, y, width-1, y, color)

# Получаем координаты от пользователя
x0 = int(input("Input first x0-coordinate: "))
y0 = int(input("Input first y0-coordinate: "))
x1 = int(input("Input second x1-coordinate: "))
y1 = int(input("Input second y1-coordinate: "))

# Создаём пустое изображение
img = Image.new('RGB', (1000, 900), 'white')

# Рисуем сетку с шагом 50 пикселей 
draw_grid(img, 50, (200, 200, 200))  # Серая сетка

# Рисуем линию на основе введённых пользователем координат
draw_line(img, x0, y0, x1, y1, (0, 0, 0))

# Показываем изображение
imshow(np.asarray(img))

# Явно отображаем изображение
plt.show()

# Сохраняем изображение
img.save('Linia.png')