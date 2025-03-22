"""Modules"""
from math import inf
import matplotlib.pyplot as plt

# Создание фигуры и осей
fig, ax = plt.subplots()
focus_length = -0.5


def make_linze(x: float=0, y: float=5, ax: plt.Axes=None):
    """"""
    # Рисуем вертикальную линию (линзу) красного цвета
    
    ax.plot([x, x], [-y, y], color='blue', lw=2)

    # Добавляем стрелки на концах красной линии
    ax.annotate('', xy=(x, y), xytext=(x, y-0.5),
                arrowprops=dict(facecolor='blue', shrink=0.05))
    ax.annotate('', xy=(x, -y), xytext=(0, -y+0.5),
                arrowprops=dict(facecolor='blue', shrink=0.05))

def add_object(x0: float, 
               y0: float,
                x1: float,
                y1: float,
                ax: plt.Axes):
    ax.plot([x0,x1],[y0, y1], color = "green", lw=1)

def draw_line_from_focus(x0: float, 
               y0: float,
                x1: float,
                y1: float,
                focus: float,
                ax: plt.Axes):
    y_pred_0 = (focus*y0)/(focus-x0)
    y_pred_1 = (focus*y1)/(focus-x1)
    ax.plot([x0,0],[y0,y_pred_0],"red")
    ax.plot([x1,0],[y1,y_pred_1],"red")

    try:
        ax.plot([x0,x0*y_pred_0/y0],[y0, y_pred_0],"red")
        ax.plot([0,x0*y_pred_0/y0],[y_pred_0,y_pred_0],color = "red")
        x_0, y_0 = x0*y_pred_0/y0, y_pred_0
    except:
        x_0, y_0 = -inf,0
    try:
        ax.plot([x1,x1*y_pred_1/y1],[y1, y_pred_1],"red")
        ax.plot([0,x1*y_pred_1/y1],[y_pred_1,y_pred_1],color = "red")
        x_1, y_1 = x1*y_pred_1/y1, y_pred_1
    except:
        x_1, y_1 = -inf,0
    x_0 = x_1 if x_0==-inf else x_0
    x_1 = x_0 if x_1==-inf else x_1
    ax.plot([x_0, x_1],[y_0,y_1],color = "green")


make_linze(0,5,ax)
add_object(*[-2,3],*[-2,-1],ax)
draw_line_from_focus(*[-2,3],*[-2,-1], focus_length, ax)

# Устанавливаем границы графика
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

# Настроим оси
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Отображаем график
plt.show()
