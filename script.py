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

fitness = read_file("genetic_algorithm_log_mutation_lux_10.txt")
print(fitness)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
gen = [i for i in range(len(fitness))]
ax.plot(gen, fitness)
ax.set_xlabel("Generation")
ax.set_ylabel("Fitness")
# ax.set_yscale("log")
ax.set_title("Fitness function")
plt.show()
