"""Modules"""
import matplotlib.pyplot as plt

def make_linze(x: float,
               y: float,
                ax: plt.Axes=None) -> None: # type: ignore
    """Рисует линзу"""
    ax.plot([x, x], [-y, y], color='blue', lw=2)

    # Добавляем стрелки
    ax.annotate('', xy=(x, y), xytext=(x, y-0.5),
                arrowprops=dict(facecolor='blue', shrink=0.05))
    ax.annotate('', xy=(x, -y), xytext=(0, -y+0.5),
                arrowprops=dict(facecolor='blue', shrink=0.05))
