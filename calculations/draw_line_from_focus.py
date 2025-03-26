"""Modules"""
from math import inf
import matplotlib.pyplot as plt

def draw_line_from_focus(x0: float,
                        y0: float,
                        x1: float,
                        y1: float,
                        focus: float,
                        ax: plt.Axes) -> None: # type: ignore
    """Рисует объект за линзой, а также путь его нахождения"""
    y_pred_0 = (focus * y0) / (focus - x0)
    y_pred_1 = (focus * y1) / (focus - x1)
    ax.plot([x0, 0], [y0, y_pred_0], "red")
    ax.plot([x1, 0], [y1, y_pred_1], "red")

    try:
        ax.plot([x0, x0 * y_pred_0 / y0], [y0, y_pred_0], "red")
        ax.plot([0, x0 * y_pred_0 / y0], [y_pred_0, y_pred_0], color="red")
        x_0, y_0 = x0 * y_pred_0 / y0, y_pred_0
    except:
        x_0, y_0 = -inf, 0

    try:
        ax.plot([x1, x1 * y_pred_1 / y1], [y1, y_pred_1], "red")
        ax.plot([0, x1 * y_pred_1 / y1], [y_pred_1, y_pred_1], color="red")
        x_1, y_1 = x1 * y_pred_1 / y1, y_pred_1
    except:
        x_1, y_1 = -inf, 0

    x_0 = x_1 if x_0 == -inf else x_0
    x_1 = x_0 if x_1 == -inf else x_1

    # Рисуем изображение за линзой
    ax.plot([x_0, x_1], [y_0, y_1], color="green", linestyle="dashed", label="Изображение в линзе")
    ax.scatter([x_0, x_1], [y_0, y_1], color="blue")
