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
    dx = (x_range[1] - x_range[0]) / size
    dy = (y_range[1] - y_range[0]) / size

    x_centers = x_range[0] + (np.arange(size) + 0.5) * dx
    y_centers = y_range[0] + (np.arange(size) + 0.5) * dy
    Xc, Yc = np.meshgrid(x_centers, y_centers)

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
    im = plt.imshow(E, origin='lower',
                    extent=(x_range[0], x_range[1], y_range[0], y_range[1]),
                    interpolation='nearest', aspect='auto')

    plt.scatter(x_list, y_list, c='red', s=100, marker='o', label='light sources', zorder=3)

    if show_values:
        for i in range(size):
            for j in range(size):
                txt = fmt.format(E[i, j])
                plt.text(x_centers[j], y_centers[i], txt,
                         color='white', ha='center', va='center',
                         fontsize=fontsize, zorder=4, clip_on=False,
                         path_effects=[patheffects.withStroke(linewidth=1, foreground='black')])

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
    # # Experiment 001 - one light at (50, 50, 50), 1000 candels, 90 degrees
    # E001 = create_light_heatmap([50], [50], [50], [1000], [90])
    
    # # Experiment 002 - one light at (50, 50, 50), 10000 candels, 90 degrees
    # E002 = create_light_heatmap([50], [50], [50], [10000], [90])
    
    # # Experiment 003 - one light at (50, 50, 50), 100 candels, 90 degrees
    # E003 = create_light_heatmap([50], [50], [50], [100], [90])
    
    # # Experiment 004 - one light at (50, 50, 50), 1000 candels, 45 degrees
    # E004 = create_light_heatmap([50], [50], [50], [1000], [45])
    
    # # Experiment 005 - one light at (50, 50, 50), 1000 candels, 30 degrees
    # E005 = create_light_heatmap([50], [50], [50], [1000], [30])
    
    # # Experiment 006 - one light at (50, 50, 50), 1000 candels, 0 degrees
    # E006 = create_light_heatmap([50], [50], [50], [1000], [0])
    
    # # Experiment 007 - one light at (50, 50, 1), 1000 candels, 90 degrees (very close to ground)
    # E007 = create_light_heatmap([50], [50], [1], [1000], [90])
    
    # # Experiment 008 - one light at (50, 50, 99), 1000 candels, 90 degrees (very high)
    # E008 = create_light_heatmap([50], [50], [99], [1000], [90])
    
    # # Experiment 009 - one light at (10, 10, 10), 1000 candels, 90 degrees (corner)
    # E009 = create_light_heatmap([10], [10], [10], [1000], [90])
    
    # # Experiment 010 - one light at (90, 90, 10), 1000 candels, 90 degrees (other corner)
    # E010 = create_light_heatmap([90], [90], [10], [1000], [90])
    
    # # Experiment 011 - one light at (85, 53, 18), 1234 candels, 56 degrees (random)
    # E011 = create_light_heatmap([85], [53], [18], [1234], [56])
    
    # # Experiment 012 - two lights at (30, 30, 30) and (70, 70, 30), 1000 candels each, 90 degrees
    # E012 = create_light_heatmap([30, 70], [30, 70], [30, 30], [1000, 1000], [90, 90])
    
    # # Experiment 013 - two lights at (20, 20, 50) and (80, 80, 50), 1000 candels each, 90 degrees
    # E013 = create_light_heatmap([20, 80], [20, 80], [50, 50], [1000, 1000], [90, 90])
    
    # # Experiment 014 - three lights at (25, 25, 40), (50, 50, 40), (75, 75, 40), 1000 candels each, 90 degrees
    # E014 = create_light_heatmap([25, 50, 75], [25, 50, 75], [40, 40, 40], [1000, 1000, 1000], [90, 90, 90])
    
    # # Experiment 015 - five lights at (20,20,20), (40,40,40), (60,60,60), (80,80,80), (50,50,50), 1000 candels each, 90 degrees
    # E015 = create_light_heatmap([20, 40, 60, 80, 50], [20, 40, 60, 80, 50], [20, 40, 60, 80, 50], [1000, 1000, 1000, 1000, 1000], [90, 90, 90, 90, 90])
    
    # # Experiment 016 - ten lights in a row at (0,10,10), (10,10,10), ..., (90,10,10), 1000 candels each, 60 degrees
    # E016 = create_light_heatmap([i * 10 for i in range(10)], [10 for i in range(10)], [10 for i in range(10)], [1000 for i in range(10)], [60 for i in range(10)])
    
    # # Experiment 017 - ten lights in a column at (90, 0, 10), (90, 10, 10), ..., (90, 90, 10), 1000 candels each, 60 degrees
    # E017 = create_light_heatmap([90 for i in range(10)], [i * 10 for i in range(10)], [10 for i in range(10)], [1000 for i in range(10)], [60 for i in range(10)])
    
    # # Experiment 018 - four lights at the corners at (0,0,20), (0,99,20), (99,0,20), (99,99,20), 1000 candels each, 45 degrees
    # E018 = create_light_heatmap([0, 0, 99, 99], [0, 99, 0, 99], [20, 20, 20, 20], [1000, 1000, 1000, 1000], [45, 45, 45, 45])



    # Loop through experiments 001-018 and read from files
    for i in [1, 16]:
        exp_num = f'{i:03d}'
        try:
            x, y, z, I, alpha = get_light_sources_from_file(f'results/v4/ga4_expr{exp_num}_1.txt')
            print(f'Processing results/v4/ga4_exp{exp_num}_1.txt')
            E = create_light_heatmap(x, y, z, I, alpha,
                                    size=10, x_range=(0, 99), y_range=(0, 99),
                                    show_values=True, fmt="{:.3f}", fontsize=10)
        except FileNotFoundError:
            print(f'File results/v4/ga4_exp{exp_num}_1.txt not found, skipping...')
    
    # E1 = create_light_heatmap([38, 38, 46, 46, 3, 3], [46, 3, 38, 3, 38, 46], [3, 46, 3, 38, 46, 38], [9535, 6448, 13154, 3726, 13138, 19226], [74, 89, 15, 85, 11, 79],
    #                          size=10, x_range=(0, 99), y_range=(0, 99),
    #                          show_values=True, fmt="{:.3f}", fontsize=10)



if __name__ == '__main__':
    main()