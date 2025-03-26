"""Modules"""
import matplotlib.pyplot as plt

def add_object(x0: float,
               y0: float,
                x1: float,
                y1: float,
               ax: plt.Axes) -> None: # type: ignore
    """Рисует объект"""
    ax.plot([x0, x1], [y0, y1], color="green", lw=1,label="Объект")
    ax.scatter([x0, x1], [y0, y1], color="green")
