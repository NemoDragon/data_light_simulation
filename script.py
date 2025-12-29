import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def read_file(file_name: str):
    best_fitness = []
    with open(file_name) as file:
        for line in file.readlines():
            if line.startswith("Generation"):
                best_fitness.append(float(line.split(" ")[5]))
    return best_fitness


def main() -> None:
    # Loop through experiments 001-018 and read from files
    for i in range(1, 19):
        exp_num = f'{i:03d}'
        
        fitness = read_file(f'results/v4/ga4_exp{exp_num}_1.txt')
        print(fitness)
        print(f'Processing results/v4/ga4_exp{exp_num}_1.txt')

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        gen = [i for i in range(len(fitness))]
        ax.plot(gen, fitness)
        ax.set_xlabel("Epoka")
        ax.set_ylabel("Dopasowanie najlepszego osobnika")
        # ax.set_yscale("log")
        ax.set_title(f"Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki")
        plt.show()

if __name__ == "__main__":
    main()
