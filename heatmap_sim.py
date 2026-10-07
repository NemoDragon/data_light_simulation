# ...existing code...
import numpy as np
import math
import matplotlib
from matplotlib import patheffects
import os
from PIL import Image
import io

matplotlib.use('Agg')  # Use non-interactive backend for saving
import matplotlib.pyplot as plt

def get_light_sources_from_file(file_name: str):
    with open(file_name) as file:
        generation_lines = file.readlines()[14:]
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
    gen_data = get_light_sources_from_file(f'results/v4/ga4_exp016_1.txt')
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

    # List to store frames
    frames = []

    # Generate frames for each generation
    for k in keys:
        x, y, z, I, alpha, fitness = gen_data[k]
        print(f'{k}: {x}, {y}, {z}, {I}, {alpha}, {fitness}')
        E, x_centers, y_centers = compute_illuminance(x, y, z, I, alpha, size=size, x_range=x_range, y_range=y_range)

        # Create a fresh figure for each frame
        fig, ax = plt.subplots(figsize=(8, 7))
        
        # Create heatmap
        im = ax.imshow(E, origin='lower',
                       extent=(x_range[0], x_range[1], y_range[0], y_range[1]),
                       interpolation='nearest', aspect='auto')
        
        # Add scatter plot for light sources
        ax.scatter(x, y, c='red', s=100, marker='o', label='light sources', zorder=3)
        
        # Add colorbar
        cbar = fig.colorbar(im)
        cbar.set_label('Illuminance (arb. units)')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        # Add text labels for each cell
        for i in range(size):
            for j in range(size):
                ax.text(x_centers[j], y_centers[i], fmt.format(E[i, j]),
                        color='white', ha='center', va='center',
                        fontsize=fontsize, zorder=4, clip_on=False,
                        path_effects=[patheffects.withStroke(linewidth=1, foreground='black')])

        # Set title with current generation info
        title = f'Illuminance heatmap best individual (gen {k}, fitness: {fitness:.2f}):\n'
        for idx in range(len(I)):
            title += f'I{idx + 1} = {I[idx]} cd α{idx + 1}={alpha[idx]}° [{x[idx]}, {y[idx]}, {z[idx]}]\n'
        ax.set_title(title)

        # Save current frame to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        frames.append(Image.open(buf).copy())
        buf.close()
        
        # Close the figure to free memory
        plt.close(fig)

    # Create output directory if it doesn't exist
    os.makedirs('heatmaps/v5', exist_ok=True)
    
    # Save as GIF with disposal mode 2 (clear previous frame before rendering next)
    output_path = 'heatmaps/v5/heatmap_animation.gif'
    frames[0].save(output_path, save_all=True, append_images=frames[1:], 
                   duration=200, loop=0, optimize=False, disposal=2)
    
    print(f"GIF saved to {output_path}")


if __name__ == '__main__':
    main()
