import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
import imageio 

# Параметры GIF
gif_filename = 'kruchu.gif'
frames = []
num_frames = 240  # Количество кадров для 1 секунды анимации

# Функция для поворота точки в 3D
def rotate(point, angle_x, angle_y, angle_z):
    ax, ay, az = np.radians(angle_x), np.radians(angle_y), np.radians(angle_z)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(ax), -np.sin(ax)],
                   [0, np.sin(ax), np.cos(ax)]])
    Ry = np.array([[np.cos(ay), 0, np.sin(ay)],
                   [0, 1, 0],
                   [-np.sin(ay), 0, np.cos(ay)]])
    Rz = np.array([[np.cos(az), -np.sin(az), 0],
                   [np.sin(az), np.cos(az), 0],
                   [0, 0, 1]])
    return Rz @ Ry @ Rx @ point

# Генерация случайных точек и создание выпуклой оболочки
num_points = 50
points = np.random.uniform(-1, 1, (num_points, 3))
hull = ConvexHull(points)

# Цвета для граней
colors = np.random.rand(len(hull.simplices), 3)

# Случайное расположение источника света
light_position = np.random.uniform(-2, 2, 3)

# Создание фигуры
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Генерация анимации вращения
for i in range(num_frames):
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.axis('on')

    # Углы поворота
    angle_x = i * 1.5  # Скорость вращения по X
    angle_y = i * 0.75  # Скорость вращения по Y
    angle_z = i * 0.5  # Скорость вращения по Z

    # Поворачиваем точки
    rotated_points = np.array([rotate(p, angle_x, angle_y, angle_z) for p in points])

    # Отрисовка передних граней с учетом источника света
    for idx, simplex in enumerate(hull.simplices):
        triangle = rotated_points[simplex]
        # Вычисление нормалей для граней
        v0 = triangle[1] - triangle[0]
        v1 = triangle[2] - triangle[0]
        normal = np.cross(v0, v1)
        normal = normal / np.linalg.norm(normal)  # Нормализация

        # Вычисление вектора от источника света к центру грани
        face_center = np.mean(triangle, axis=0)
        light_direction = light_position - face_center
        light_direction = light_direction / np.linalg.norm(light_direction)  # Нормализация

        # Вычисление интенсивности освещения
        intensity = np.dot(normal, light_direction)
        intensity = np.clip(intensity, 0, 1)  # Ограничение значений

        # Добавление базового освещения
        base_intensity = 0.2  # Минимальный уровень освещения
        final_intensity = np.clip(intensity + base_intensity, 0, 1)  # Ограничение значений

        # Применение освещения
        face_color = colors[idx] * final_intensity

        # Визуализация грани с улучшенной освещенностью
        ax.plot_trisurf(triangle[:, 0], triangle[:, 1], triangle[:, 2],
                        color=face_color, edgecolor='k', alpha=1.0, shade=False)

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)

# Сохранение в GIF с 240 fps
imageio.mimsave(gif_filename, frames, fps=240)
print(f'GIF сохранен в файл: {gif_filename}')