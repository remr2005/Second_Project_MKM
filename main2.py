import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, TextBox

# Начальные параметры
initial_f = -15  # Отрицательное фокусное расстояние для рассеивающей линзы
initial_d_o = 10.0
initial_h_o = 2.0


def draw_diverging_lens_diagram(f, d_o, h_o):
    ax.clear()
    ax.axvline(0, color="black", linestyle="-")  # Линза
    ax.axhline(0, color="gray", linestyle="-")  # Оптическая ось

    try:
        d_i = 1 / (1 / f - 1 / d_o)
    except ZeroDivisionError:
        d_i = np.inf

    h_i = h_o * (-d_i / d_o) if np.isfinite(d_i) else 0

    object_x = -d_o
    ax.plot([object_x, object_x], [0, h_o], color="blue", linewidth=3, label="Объект")
    ax.annotate(
        "",
        xy=(0, -h_o - 1),
        xytext=(0, h_o + 1),
        arrowprops=dict(arrowstyle="<->", color="yellow", linewidth=3),
    )

    ax.plot([0, 0], [-h_o - 1, h_o + 1], color="yellow", linewidth=3, label="Линза")
    ax.annotate(
        "",
        xy=(object_x, h_o),
        xytext=(object_x, 0),
        arrowprops=dict(arrowstyle="->", color="blue", linewidth=3),
    )
    ax.text(object_x, h_o + 0.5, "Объект", ha="center", color="blue")

    # Фокусные точки
    ax.plot(f, 0, "o", color="purple", label="Фокус")  # Фокус справа
    ax.plot(-f, 0, "o", color="purple")  # Фокус слева
    ax.text(f, 0.5, "F", color="purple", ha="center", fontsize=10)
    ax.text(-f, 0.5, "F'", color="purple", ha="center", fontsize=10)

    if np.isfinite(d_i):
        # Центральный луч: от объекта через центр линзы
        # Центральный луч: от объекта через центр линзы, продлеваем вправо
        x_center = np.linspace(object_x, 20, 500)
        m_center = h_o / object_x  # наклон прямой
        y_center = m_center * x_center

        # Луч, идущий параллельно оптической оси, отклоняется как будто из фокуса
        x_parallel = [object_x, 0]
        y_parallel = [h_o, h_o]

        # После линзы — уходит вниз, продолжение уходит в фокус
        m_virtual = (0 - h_o) / (f - 0)
        b_virtual = h_o

        # Продление луча к пересечению
        x_virtual = np.linspace(0, 20, 100)
        y_virtual = m_virtual * x_virtual + b_virtual

        # Пунктирное продолжение назад (мнимое изображение)
        x_back = np.linspace(-20, 0, 100)
        y_back = m_virtual * x_back + b_virtual

        # Пересечение — мнимое изображение
        image_x = d_i
        image_y = h_i
        img_color = "orange"
        label = "Мнимое изображение"

        # Рисуем
        ax.plot(x_center, y_center, "g", label="Лучи")
        ax.plot(x_parallel, y_parallel, "g")
        ax.plot(x_virtual, y_virtual, "g")
        ax.plot(x_back, y_back, linestyle="--", color="green")
        ax.plot(
            [image_x, image_x], [0, image_y], color=img_color, linewidth=3, label=label
        )
        ax.annotate(
            "",
            xy=(image_x, image_y),
            xytext=(image_x, 0),
            arrowprops=dict(arrowstyle="->", color=img_color, linewidth=3),
        )
        ax.text(image_x, image_y + 0.5, label, ha="center", color=img_color)
        ax.plot([image_x, image_x], [image_y, 0], linestyle="--", color="gray")

        # Настройка границ
        x_vals = [0, object_x]
    y_vals = [0, h_o]
    if np.isfinite(d_i):
        x_vals.append(image_x)
        y_vals.append(image_y)

    margin_x = 2
    margin_y = 2

    x_min = min(x_vals) - margin_x
    x_max = max(x_vals) + margin_x

    # Гарантируем, что линза (x=0) входит в диапазон
    if x_min > 0:
        x_min = -margin_x
    if x_max < 0:
        x_max = margin_x

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(min(0, min(y_vals)) - margin_y, max(y_vals) + margin_y)

    ax.set_title("Рассеивающая линза")
    ax.legend()
    plt.draw()


def submit(event=None):
    try:
        f = float(text_box_f.text)
        f = f if f < 0 else -f  # Рассеивающая линза — отрицательное фокусное
        d_o = float(text_box_do.text)
        d_o = d_o if d_o > 0 else -d_o
        h_o = float(text_box_ho.text)
        draw_diverging_lens_diagram(f, d_o, h_o)
    except ValueError:
        print("Ошибка ввода! Введите числовые значения.")


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

draw_diverging_lens_diagram(initial_f, initial_d_o, initial_h_o)
plt.show()
