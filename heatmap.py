import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def get_light_sources_from_file(file_name: str):
    with open(file_name) as file:
        pos, I = file.readlines()[-2:]
        positions = pos.split("[")
        Is = I.strip().split(" ")
        x0 = []
        y0 = []
        z0 = []
        I0 = []
        for i in range(len(positions)):
            if i > 0:
                x0.append(int(positions[i].split(" ")[0]))
                y0.append(int(positions[i].split(" ")[1]))
                z0.append(int(positions[i].split(" ")[2]))
        for i in range(len(Is)):
            if i > 2:
                I0.append(float(Is[i]))
    return x0, y0, z0, I0


def create_light_heatmap(x_list: list[int], y_list: list[int], z_list: list[int], I_list: list[float], size=100, x_range=(0, 99), y_range=(0, 99)):
    xs = np.linspace(x_range[0], x_range[1], size)
    ys = np.linspace(y_range[0], y_range[1], size)
    X, Y = np.meshgrid(xs, ys)
    E = np.zeros_like(X, dtype=float)

    for x, y, z, I in zip(x_list, y_list, z_list, I_list):
        dx = X - x
        dy = Y - y
        dz = -z

        r = np.sqrt(dx**2 + dy**2 + dz**2)
        r = np.maximum(r, 1e-6)

        E += I * z / (r**3)
    plt.figure(figsize=(6, 5))
    im = plt.imshow(E, origin='lower',
                    extent=(x_range[0], x_range[1], y_range[0], y_range[1]))
    plt.scatter(x_list, y_list, c='cyan', s=50, marker='x', label='light sources')
    title = 'Illuminance heatmap:\n'
    for i in range(len(I_list)):
        title += f'I{i + 1} = {I_list[i]} cd [{x_list[0]}, {y_list[i]}, {z_list[i]}]\n'
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    cbar = plt.colorbar(im)
    cbar.set_label('Illuminance (arb. units)')
    plt.legend(loc='upper right')
    plt.show()

    return E


def main() -> None:
    """
        for i in range(11, 31):
        x, y, z, I = get_light_sources_from_file(f'results/genetic_algorithm_{i}.txt')
        print(f'{i}: {x}, {y}, {z}, {I}')
        E = create_light_heatmap(x, y, z, I)
    """
    E = create_light_heatmap([50, 10], [50, 10], [50, 50], [1000, 1000])



if __name__ == '__main__':
    main()