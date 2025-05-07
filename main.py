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
    ax.axvline(0, color="black", linestyle="-")  # Линза
    ax.axhline(0, color="gray", linestyle="-")  # Оптическая ось

    try:
        d_i = 1 / (1 / f - 1 / d_o)
    except ZeroDivisionError:
        d_i = np.inf

    h_i = h_o * (-d_i / d_o) if np.isfinite(d_i) else 0

    object_x = -d_o
    ax.plot([object_x, object_x], [0, h_o], color="blue", linewidth=3, label="Объект")

    # Добавляем стрелку
    ax.annotate(
        "",  # пустой текст, т.к. нам нужна только стрелка
        xy=(object_x, h_o),  # куда указывает стрелка (конец)
        xytext=(object_x, 0),  # откуда начинается стрелка (начало)
        arrowprops=dict(arrowstyle="->", color="blue", linewidth=3),
    )

    ax.text(object_x, h_o + 0.5, "Объект", ha="center", color="blue")

    if np.isfinite(d_i):
        # Центральный луч — от объекта через центр линзы (0,0)
        x_center = np.array([object_x, 0])
        y_center = np.array([h_o, 0])
        # Параллельный луч от объекта до линзы
        x_parallel = np.array([object_x, 0])
        y_parallel = np.array([h_o, h_o])

        # Продление луча от линзы через фокус (f, 0)
        f_x = f
        f_y = 0

        # Вычисляем уравнение луча через фокус:
        m_f = (f_y - h_o) / (f_x - 0)
        b_f = h_o

        # Вычисляем уравнение центрального луча:
        m_c = (0 - h_o) / (0 - object_x)
        b_c = h_o - m_c * object_x

        # Находим точку пересечения
        x_inter = (b_c - b_f) / (m_f - m_c)
        y_inter = m_c * x_inter + b_c

        # Строим луч от линзы через фокус до пересечения

        # Рисуем изображение в найденной точке
        image_x = x_inter
        image_y = y_inter
        img_color = "red" if image_x > 0 else "orange"
        label = "Реальное изображение" if image_x > 0 else "Мнимое изображение"
        color = "g" if image_x > 0 else "g--"
        ax.plot(x_center, y_center, "g")
        ax.plot(x_parallel, y_parallel, "g")
        ax.plot([0, x_inter], [h_o, y_inter], color)
        ax.plot(
            [image_x, image_x], [0, image_y], color=img_color, linewidth=3, label=label
        )
        ax.text(image_x, image_y + 0.5, label, ha="center", color=img_color)
        ax.annotate(
            "",  # пустой текст, т.к. нам нужна только стрелка
            xy=(image_x, image_y),  # куда указывает стрелка (конец)
            xytext=(image_x, 0),  # откуда начинается стрелка (начало)
            arrowprops=dict(arrowstyle="->", color=img_color, linewidth=3),
        )
        ax.annotate(
            "",  # пустой текст, т.к. нам нужна только стрелка
            xy=(0, 10),  # куда указывает стрелка (конец)
            xytext=(0, -10),  # откуда начинается стрелка (начало)
            arrowprops=dict(arrowstyle="<->", color="blue", linewidth=3),
        )
        ax.plot([0, x_inter], [0, y_inter], color)

    x_vals = [0, object_x]
    y_vals = [0, h_o]
    if np.isfinite(d_i):
        x_vals.append(image_x)
        y_vals.append(image_y)
    margin_x = 2
    margin_y = 2
    ax.set_xlim(min(x_vals) - margin_x, max(x_vals) + margin_x)
    ax.set_ylim(min(0, min(y_vals)) - margin_y, max(y_vals) + margin_y)

    ax.set_title("Собирающая линза")
    ax.legend()
    plt.draw()


def submit(event=None):
    try:
        f = float(text_box_f.text)
        f = f if f > 0 else -f
        d_o = float(text_box_do.text)
        d_o = d_o if d_o > 0 else -d_o
        h_o = float(text_box_ho.text)
        draw_lens_diagram(f, d_o, h_o)
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

draw_lens_diagram(initial_f, initial_d_o, initial_h_o)
plt.show()
