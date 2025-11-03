import numpy as np
import math
import matplotlib
from matplotlib import patheffects

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def get_light_sources_from_file(file_name: str):
    with open(file_name) as file:
        pos, I, alpha = file.readlines()[-3:]
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
    return x0, y0, z0, I0, alpha0


def create_light_heatmap(x_list: list[int], y_list: list[int], z_list: list[int], I_list: list[float], alpha_list: list[int],
                         size=10, x_range=(0, 99), y_range=(0, 99),
                         show_values=True, fmt="{:.3f}", fontsize=8):
    # grid spacing
    dx = (x_range[1] - x_range[0]) / size
    dy = (y_range[1] - y_range[0]) / size

    # centers of pixels (important!)
    x_centers = x_range[0] + (np.arange(size) + 0.5) * dx
    y_centers = y_range[0] + (np.arange(size) + 0.5) * dy
    Xc, Yc = np.meshgrid(x_centers, y_centers)

    # for computation we can still use meshgrid of centers
    X, Y = Xc, Yc
    E = np.zeros_like(X, dtype=float)

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

    plt.figure(figsize=(8, 7))
    # imshow wants array shape (ny, nx); extent maps edges (xmin, xmax, ymin, ymax)
    im = plt.imshow(E, origin='lower',
                    extent=(x_range[0], x_range[1], y_range[0], y_range[1]),
                    interpolation='nearest', aspect='auto')

    # plot sources
    plt.scatter(x_list, y_list, c='red', s=60, marker='x', label='light sources', zorder=3)

    # draw values centered in pixels
    if show_values:
        for i in range(size):
            for j in range(size):
                txt = fmt.format(E[i, j])
                plt.text(x_centers[j], y_centers[i], txt,
                         color='white', ha='center', va='center',
                         fontsize=fontsize, zorder=4, clip_on=False,
                         path_effects=[patheffects.withStroke(linewidth=1, foreground='black')])

    # title: correct indices
    title = 'Illuminance heatmap:\n'
    for i in range(len(I_list)):
        title += f'I{i + 1} = {I_list[i]} cd α{i + 1}={alpha_list[i]}° [{x_list[i]}, {y_list[i]}, {z_list[i]}]\n'
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    cbar = plt.colorbar(im)
    cbar.set_label('Illuminance (arb. units)')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    return E


def main() -> None:
    """
        for i in range(11, 31):
        x, y, z, I = get_light_sources_from_file(f'results/genetic_algorithm_{i}.txt')
        print(f'{i}: {x}, {y}, {z}, {I}')
        E = create_light_heatmap(x, y, z, I)
    """
    x, y, z, I, alpha = get_light_sources_from_file(f'results/ga2_exp001_1.txt')
    E = create_light_heatmap(x, y, z, I, alpha,
                             size=10, x_range=(0, 99), y_range=(0, 99),
                             show_values=True, fmt="{:.3f}", fontsize=10)
    E = create_light_heatmap([50], [50], [50], [1000], [90],
                             size=10, x_range=(0, 99), y_range=(0, 99),
                             show_values=True, fmt="{:.3f}", fontsize=10)
    # E1 = create_light_heatmap([38, 38, 46, 46, 3, 3], [46, 3, 38, 3, 38, 46], [3, 46, 3, 38, 46, 38], [9535, 6448, 13154, 3726, 13138, 19226], [74, 89, 15, 85, 11, 79],
    #                          size=10, x_range=(0, 99), y_range=(0, 99),
    #                          show_values=True, fmt="{:.3f}", fontsize=10)



if __name__ == '__main__':
    main()