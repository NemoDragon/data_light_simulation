# ...existing code...
import numpy as np
import math
import matplotlib
from matplotlib import patheffects

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def get_light_sources_from_file(file_name: str):
    with open(file_name) as file:
        generation_lines = file.readlines()[13:]
        generation_data = {}
        for i in range(0, len(generation_lines), 4):
            gen_text, pos, I, alpha = generation_lines[i], generation_lines[i+1], generation_lines[i+2], generation_lines[i+3]
            gen = int(gen_text.split(" ")[1][:-1])
            fitness = float(gen_text.split(" ")[5])
            positions = pos.split("[")
            Is = I.strip().split(" ")
            alphas = alpha.strip().split(" ")
            x0 = []
            y0 = []
            z0 = []
            I0 = []
            alpha0 = []
            for i in range(len(positions)):
                if i > 0:
                    x0.append(int(positions[i].split(" ")[0]))
                    y0.append(int(positions[i].split(" ")[1]))
                    z0.append(int(positions[i].split(" ")[2]))
            for i in range(len(Is)):
                if i > 2:
                    I0.append(float(Is[i]))
            for i in range(len(alphas)):
                if i > 2:
                    alpha0.append(int(alphas[i]))
            generation_data[gen] = (x0, y0, z0, I0, alpha0, fitness)
    return generation_data


def compute_illuminance(x_list: list[int], y_list: list[int], z_list: list[int],
                        I_list: list[float], alpha_list: list[int],
                        size=10, x_range=(0, 99), y_range=(0, 99)):
    # grid spacing
    dx = (x_range[1] - x_range[0]) / size
    dy = (y_range[1] - y_range[0]) / size

    # centers of pixels
    x_centers = x_range[0] + (np.arange(size) + 0.5) * dx
    y_centers = y_range[0] + (np.arange(size) + 0.5) * dy
    Xc, Yc = np.meshgrid(x_centers, y_centers)

    E = np.zeros_like(Xc, dtype=float)

    for x, y, z, I, alpha_deg in zip(x_list, y_list, z_list, I_list, alpha_list):
        alpha = np.deg2rad(alpha_deg)
        dx_arr = Xc - x
        dy_arr = Yc - y
        dz = z
        r2 = dx_arr ** 2 + dy_arr ** 2 + dz ** 2
        r = np.sqrt(r2)
        r = np.maximum(r, 1e-6)
        ground_dist2 = dx_arr ** 2 + dy_arr ** 2
        radius2 = (dz * math.tan(alpha)) ** 2
        cos_theta = dz / r
        inside_cone = (ground_dist2 <= radius2) | (alpha_deg == 90)
        E += np.where(inside_cone, I * cos_theta / r2, 0)

    return E, x_centers, y_centers


def main() -> None:
    gen_data = get_light_sources_from_file(f'results/ga_exp014_1.txt')
    if not gen_data:
        print("No generation data found.")
        return

    keys = sorted(gen_data.keys())

    # plotting setup
    size = 10
    x_range = (0, 99)
    y_range = (0, 99)
    fmt = "{:.3f}"
    fontsize = 8

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 7))

    # initial frame from first generation
    first = gen_data[keys[0]]
    x, y, z, I, alpha, fitness = first
    E, x_centers, y_centers = compute_illuminance(x, y, z, I, alpha, size=size, x_range=x_range, y_range=y_range)

    im = ax.imshow(E, origin='lower',
                   extent=(x_range[0], x_range[1], y_range[0], y_range[1]),
                   interpolation='nearest', aspect='auto')
    scatter = ax.scatter(x, y, c='red', s=60, marker='x', label='light sources', zorder=3)
    cbar = fig.colorbar(im)
    cbar.set_label('Illuminance (arb. units)')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # create text labels once and update text contents each frame
    text_grid = []
    for i in range(size):
        row = []
        for j in range(size):
            t = ax.text(x_centers[j], y_centers[i], fmt.format(E[i, j]),
                        color='white', ha='center', va='center',
                        fontsize=fontsize, zorder=4, clip_on=False,
                        path_effects=[patheffects.withStroke(linewidth=1, foreground='black')])
            row.append(t)
        text_grid.append(row)

    # animate through generations
    for k in keys:
        x, y, z, I, alpha, fitness = gen_data[k]
        print(f'{k}: {x}, {y}, {z}, {I}, {alpha}, {fitness}')
        E, x_centers, y_centers = compute_illuminance(x, y, z, I, alpha, size=size, x_range=x_range, y_range=y_range)

        im.set_data(E)
        # update color limits to reflect new data range
        vmin, vmax = np.nanmin(E), np.nanmax(E)
        if vmin == vmax:
            vmax = vmin + 1e-6
        im.set_clim(vmin, vmax)
        # update scatter (positions may change between generations)
        scatter.set_offsets(np.c_[x, y])

        # update texts
        for i in range(size):
            for j in range(size):
                text_grid[i][j].set_text(fmt.format(E[i, j]))

        # update title with current generation info
        title = f'Illuminance heatmap (gen {k}, fitness: {fitness:.2f}):\n'
        for idx in range(len(I)):
            title += f'I{idx + 1} = {I[idx]} cd α{idx + 1}={alpha[idx]}° [{x[idx]}, {y[idx]}, {z[idx]}]\n'
        ax.set_title(title)

        fig.canvas.draw_idle()
        plt.pause(0.5)  # delay between frames

    plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()
