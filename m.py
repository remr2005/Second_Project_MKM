import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Создание фигуры и осей
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

focus_length = -0.5

# Исходные точки
x0, y0, x1, y1 = -2, 3, -2, -1
y_pred_0 = (focus_length * y0) / (focus_length - x0)
y_pred_1 = (focus_length * y1) / (focus_length - x1)

# Линии, которые будем анимировать
object_line, = ax.plot([], [], color="green", lw=2)
focus_line_1, = ax.plot([], [], color="red")
focus_line_2, = ax.plot([], [], color="red")

# Функция инициализации (очищаем график перед стартом)
def init():
    object_line.set_data([], [])
    focus_line_1.set_data([], [])
    focus_line_2.set_data([], [])
    return object_line, focus_line_1, focus_line_2

# Функция обновления кадров
def update(frame):
    t = frame / 20  # Нормализация

    # Обновляем объект (зеленая линия)
    object_line.set_data([-2, -2], [3 * t, -1 * t])

    # Обновляем линии к фокусу (красные)
    focus_line_1.set_data([-2, 0], [3 * t, y_pred_0 * t])
    focus_line_2.set_data([-2, 0], [-1 * t, y_pred_1 * t])

    return object_line, focus_line_1, focus_line_2

# Запускаем анимацию
ani = animation.FuncAnimation(fig, update, frames=20, init_func=init, blit=False, interval=100)

# Отображаем график
plt.show()
