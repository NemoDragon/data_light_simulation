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
    for i in range(11, 31):
        fitness = read_file(f'results/genetic_algorithm_{i}.txt')
        print(fitness)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        gen = [i for i in range(len(fitness))]
        ax.plot(gen, fitness)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness")
        # ax.set_yscale("log")
        ax.set_title(f"Fitness function: GA with 1 position, run {i - 10} " if i < 21 else f"Fitness function: GA with 3 positions, run {i % 20} ")
        plt.show()

if __name__ == "__main__":
    main()
