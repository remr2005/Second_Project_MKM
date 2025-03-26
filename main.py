"""Modules"""
import matplotlib.pyplot as plt
from calculations import add_object, draw_line_from_focus, make_linze
from matplotlib.widgets import Button

# Создание фигуры и осей
fig, ax = plt.subplots()
FOCUS_LENGHT = -0.5

make_linze(0, 5, ax)
# add_object(*[-2, 3], *[-2, -1], ax)
# draw_line_from_focus(*[-2, 3], *[-2, -1], FOCUS_LENGHT, ax)

# Устанавливаем границы графика
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

# Настроим оси
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

ax_button = plt.axes([0.8, 0.01, 0.1, 0.075])  # Расположение кнопки
button = Button(ax_button, 'Start')

# Функция для обновления графика при нажатии кнопки
def on_button_click(event):
    add_object(*[-2, 3], *[-2, -1], ax)
    fig.canvas.draw()  # Обновляем график
button.on_clicked(on_button_click)

# Добавляем легенду
ax.legend()

# Отображаем график
plt.show()
