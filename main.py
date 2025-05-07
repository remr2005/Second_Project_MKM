import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, TextBox

# Начальные параметры
initial_f = 5.0
initial_d_o = 10.0
initial_h_o = 2.0


# Функция для расчета изображения и построения графика
def draw_lens_diagram(f, d_o, h_o):
    ax.clear()
    ax.axvline(0, color="black", linestyle="--")  # Линза
    ax.axhline(0, color="gray", linestyle="--")  # Оптическая ось

    # Положение изображения (d_i) по формуле тонкой линзы
    try:
        d_i = 1 / (1 / f - 1 / d_o)
    except ZeroDivisionError:
        d_i = np.inf

    # Высота изображения
    h_i = h_o * (-d_i / d_o) if np.isfinite(d_i) else 0

    # Рисуем объект слева от линзы (отрицательная координата)
    object_x = -d_o
    ax.plot([object_x, object_x], [0, h_o], color="blue", linewidth=3, label="Объект")
    ax.text(object_x, h_o + 0.5, "Объект", ha="center", color="blue")

    # Рисуем изображение
    if np.isfinite(d_i):
        image_x = (
            d_i if d_i > 0 else -abs(d_i)
        )  # справа для реального, слева для мнимого
        img_color = "red" if d_i > 0 else "orange"
        label = "Реальное изображение" if d_i > 0 else "Мнимое изображение"
        ax.plot([image_x, image_x], [0, h_i], color=img_color, linewidth=3, label=label)
        ax.text(image_x, h_i + 0.5, label, ha="center", color=img_color)

        # Главные лучи
        # Луч 1: параллельный -> через фокус
        ax.plot([object_x, 0], [h_o, h_o], "g--")
        ax.plot([0, image_x], [h_o, 0], "g--")

        # Луч 2: через центр линзы (не преломляется)
        ax.plot([object_x, image_x], [h_o, h_i], "g--")

        # Луч 3: в фокус на объектной стороне -> параллельно
        f_point = -f
        ax.plot([object_x, 0], [h_o, h_o * (0 - f_point) / (object_x - f_point)], "g--")
        ax.plot([0, image_x], [h_o * (0 - f_point) / (object_x - f_point), h_i], "g--")

    # Автоматически подбираем границы
    x_vals = [0, object_x]
    y_vals = [0, h_o]
    if np.isfinite(d_i):
        x_vals.append(image_x)
        y_vals.append(h_i)
    margin_x = 2
    margin_y = 2
    ax.set_xlim(min(x_vals) - margin_x, max(x_vals) + margin_x)
    ax.set_ylim(min(0, min(y_vals)) - margin_y, max(y_vals) + margin_y)

    ax.set_title("Собирающая линза")
    ax.legend()
    plt.draw()


# Обработчик нажатия кнопки


def submit(event=None):
    try:
        f = float(text_box_f.text)
        d_o = float(text_box_do.text)
        h_o = float(text_box_ho.text)
        draw_lens_diagram(f, d_o, h_o)
    except ValueError:
        print("Ошибка ввода! Введите числовые значения.")


# Настройка окна и виджетов
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)

axf = plt.axes([0.15, 0.2, 0.2, 0.05])
axdo = plt.axes([0.15, 0.13, 0.2, 0.05])
axho = plt.axes([0.15, 0.06, 0.2, 0.05])

text_box_f = TextBox(axf, "Фокусное f:", initial=str(initial_f))
text_box_do = TextBox(axdo, "Расстояние до объекта dₒ:", initial=str(initial_d_o))
text_box_ho = TextBox(axho, "Высота объекта hₒ:", initial=str(initial_h_o))

submit_ax = plt.axes([0.4, 0.06, 0.1, 0.1])
submit_button = Button(submit_ax, "Построить")
submit_button.on_clicked(submit)

# Первоначальный график
draw_lens_diagram(initial_f, initial_d_o, initial_h_o)
plt.show()
