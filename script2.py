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


def plot_hyperparameter(exp_num, param_type, param_values, param_labels, title):
    """
    Plot fitness evolution for a specific hyperparameter optimization
    
    Args:
        exp_num: experiment number (001 or 016)
        param_type: type of parameter (mut, cross, tourn, pop)
        param_values: list of parameter values to plot
        param_labels: list of labels for legend
        title: plot title
    """
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    
    for param_val, label in zip(param_values, param_labels):
        # Read all 4 trials for this configuration
        all_fitness = []
        for trial in range(1, 5):
            file_name = f'results/v4_par/ga4_exp{param_type}{exp_num}_{param_val}_{trial}.txt'
            fitness = read_file(file_name)
            all_fitness.append(fitness)
        
        # Find the best trial (lowest final fitness)
        best_trial_idx = min(range(len(all_fitness)), key=lambda i: all_fitness[i][-1])
        best_fitness = all_fitness[best_trial_idx]
        
        # Plot the best trial
        gen = [i for i in range(len(best_fitness))]
        ax.plot(gen, best_fitness, label=label, linewidth=2)
    
    ax.set_xlabel("Epoka")
    ax.set_ylabel("Dopasowanie najlepszego osobnika")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main() -> None:
    # 1. Mutation probability - Experiment 001
    plot_hyperparameter(
        exp_num='001',
        param_type='mut',
        param_values=['5', '10', '20', '30'],
        param_labels=['5%', '10%', '20%', '30%'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja prawdopodobieństwa mutacji - Eksperyment 1)'
    )
    
    # 2. Mutation probability - Experiment 016
    plot_hyperparameter(
        exp_num='016',
        param_type='mut',
        param_values=['5', '10', '20', '30'],
        param_labels=['5%', '10%', '20%', '30%'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja prawdopodobieństwa mutacji - Eksperyment 16)'
    )
    
    # 3. Crossover probability - Experiment 001
    plot_hyperparameter(
        exp_num='001',
        param_type='cross',
        param_values=['50', '70', '90'],
        param_labels=['50%', '70%', '90%'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja prawdopodobieństwa krzyżowania - Eksperyment 1)'
    )
    
    # 4. Crossover probability - Experiment 016
    plot_hyperparameter(
        exp_num='016',
        param_type='cross',
        param_values=['50', '70', '90'],
        param_labels=['50%', '70%', '90%'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja prawdopodobieństwa krzyżowania - Eksperyment 16)'
    )
    
    # 5. Tournament size - Experiment 001
    plot_hyperparameter(
        exp_num='001',
        param_type='tourn',
        param_values=['5', '10', '20', '40'],
        param_labels=['5', '10', '20', '40'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja rozmiaru turnieju - Eksperyment 1)'
    )
    
    # 6. Tournament size - Experiment 016
    plot_hyperparameter(
        exp_num='016',
        param_type='tourn',
        param_values=['5', '10', '20', '40'],
        param_labels=['5', '10', '20', '40'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja rozmiaru turnieju - Eksperyment 16)'
    )
    
    # 7. Population size - Experiment 001
    plot_hyperparameter(
        exp_num='001',
        param_type='pop',
        param_values=['500', '1000', '2000', '4000'],
        param_labels=['500', '1000', '2000', '4000'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja rozmiaru populacji - Eksperyment 1)'
    )
    
    # 8. Population size - Experiment 016
    plot_hyperparameter(
        exp_num='016',
        param_type='pop',
        param_values=['500', '1000', '2000', '4000'],
        param_labels=['500', '1000', '2000', '4000'],
        title='Wartość funkcji dopasowania najlepszego osobnika w zależności od epoki\n(Optymalizacja rozmiaru populacji - Eksperyment 16)'
    )


if __name__ == "__main__":
    main()