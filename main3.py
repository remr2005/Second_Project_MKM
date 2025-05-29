import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.widgets import Button, TextBox

k = 8.9875517923e9  # Н·м²/Кл²
grid_dx = grid_dy = 0.1
xlim, ylim = (-5, 5), (-5, 5)


def electric_potential(x, y, charges):
    phi = 0.0
    for q, xq, yq in charges:
        r = np.hypot(x - xq, y - yq)
        if r < 1e-10:
            continue
        phi += k * q / r
    return phi


def electric_field(x, y, charges):
    Ex, Ey = 0.0, 0.0
    for q, xq, yq in charges:
        dx, dy = x - xq, y - yq
        r = np.hypot(dx, dy)
        if r < 1e-10:
            continue
        E = k * abs(q) / r**2
        Ex += np.sign(q) * E * dx / r
        Ey += np.sign(q) * E * dy / r
    return Ex, Ey


def trace_field_line(x0, y0, charges, deltaL=0.05, max_steps=1000):
    x, y = [x0], [y0]
    for _ in range(max_steps):
        Ex, Ey = electric_field(x[-1], y[-1], charges)
        E_mag = np.hypot(Ex, Ey)
        if E_mag < 1e-3:
            break
        dx = deltaL * Ex / E_mag
        dy = deltaL * Ey / E_mag
        xn, yn = x[-1] + dx, y[-1] + dy
        if not (xlim[0] < xn < xlim[1]) or not (ylim[0] < yn < ylim[1]):
            break
        if any(q < 0 and np.hypot(xn - xq, yn - yq) < 0.2 for q, xq, yq in charges):
            break
        x.append(xn)
        y.append(yn)
    return x, y


def plot_field_on_axes(ax, charges):
    ax.clear()
    x = np.arange(xlim[0], xlim[1] + grid_dx, grid_dx)
    y = np.arange(ylim[0], ylim[1] + grid_dy, grid_dy)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda x, y: electric_potential(x, y, charges))(X, Y)

    z_min, z_max = Z.min(), Z.max()
    if z_max - z_min > 1e-12:  # Проверяем, что диапазон не слишком мал
        levels = np.linspace(z_min, z_max, 10)
        ax.contour(X, Y, Z, levels=levels, colors="purple", alpha=0.6)
    else:
        # Можно пропустить контур или нарисовать один уровень (например, ноль)
        pass

    max_q = max(abs(q) for q, _, _ in charges) if charges else 1
    base_lines = 12
    for q, xq, yq in charges:
        color = "red" if q > 0 else "blue"
        ax.add_patch(Circle((xq, yq), 0.1, color=color))
        ax.text(
            xq, yq, f"{q:.1e} Кл", color="white", ha="center", va="center", fontsize=8
        )
        if q > 0:
            n_lines = max(8, int(base_lines * abs(q) / max_q))
            angles = np.linspace(0, 2 * np.pi, n_lines, endpoint=False)
            for angle in angles:
                x0 = xq + 0.2 * np.cos(angle)
                y0 = yq + 0.2 * np.sin(angle)
                x_line, y_line = trace_field_line(x0, y0, charges)
                ax.plot(x_line, y_line, "k-", lw=0.8)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")
    ax.grid(True)
    ax.set_title("Линии электрического поля и эквипотенциали")
    ax.set_xlabel("x")
    ax.set_ylabel("y")


class GUI:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.3, top=0.95)

        # Поля для ввода заряда и координат
        self.box_q = TextBox(
            plt.axes([0.1, 0.22, 0.2, 0.05]), "Заряд (Кл):", initial="1e-9"
        )
        self.box_x = TextBox(plt.axes([0.1, 0.15, 0.2, 0.05]), "X (м):", initial="0")
        self.box_y = TextBox(plt.axes([0.1, 0.08, 0.2, 0.05]), "Y (м):", initial="0")

        # Кнопки добавить +, добавить -, очистить
        ax_add_pos = plt.axes([0.35, 0.22, 0.15, 0.05])
        self.btn_add_pos = Button(ax_add_pos, "Добавить +")
        self.btn_add_pos.on_clicked(self.add_positive_charge)

        ax_add_neg = plt.axes([0.35, 0.15, 0.15, 0.05])
        self.btn_add_neg = Button(ax_add_neg, "Добавить -")
        self.btn_add_neg.on_clicked(self.add_negative_charge)

        ax_clear = plt.axes([0.35, 0.08, 0.15, 0.05])
        self.btn_clear = Button(ax_clear, "Очистить")
        self.btn_clear.on_clicked(self.clear_charges)

        self.current_charges = []
        self.plot()

    def add_positive_charge(self, event):
        try:
            q = abs(float(self.box_q.text))
            x = float(self.box_x.text)
            y = float(self.box_y.text)
            self.current_charges.append((q, x, y))
            self.plot()
        except Exception as e:
            print("Ошибка при добавлении положительного заряда:", e)

    def add_negative_charge(self, event):
        try:
            q = -abs(float(self.box_q.text))
            x = float(self.box_x.text)
            y = float(self.box_y.text)
            self.current_charges.append((q, x, y))
            self.plot()
        except Exception as e:
            print("Ошибка при добавлении отрицательного заряда:", e)

    def clear_charges(self, event):
        self.current_charges = []
        self.plot()

    def plot(self):
        plot_field_on_axes(self.ax, self.current_charges)
        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    gui = GUI()
    plt.show()
