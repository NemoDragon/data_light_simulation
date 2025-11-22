#include "include/individual.h"
#include "include/genetic_algorithm.h"
#include "include/utils.h"
#include <iostream>
#include <map>
#include <cstddef>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>

int main()
{
    srand(static_cast<unsigned int>(time(nullptr)));

    Individual target({
                          {0, 0, 0},
                          {0, 10, 0},
                          {0, 20, 0},
                          {0, 30, 0},
                          {0, 40, 0},
                          {0, 50, 0},
                          {0, 60, 0},
                          {0, 70, 0},
                          {0, 80, 0},
                          {0, 90, 0},
                          {10, 0, 0},
                          {10, 10, 0},
                          {10, 20, 0},
                          {10, 30, 0},
                          {10, 40, 0},
                          {10, 50, 0},
                          {10, 60, 0},
                          {10, 70, 0},
                          {10, 80, 0},
                          {10, 90, 0},
                          {20, 0, 0},
                          {20, 10, 0},
                          {20, 20, 0},
                          {20, 30, 0},
                          {20, 40, 0},
                          {20, 50, 0},
                          {20, 60, 0},
                          {20, 70, 0},
                          {20, 80, 0},
                          {20, 90, 0},
                          {30, 0, 0},
                          {30, 10, 0},
                          {30, 20, 0},
                          {30, 30, 0},
                          {30, 40, 0},
                          {30, 50, 0},
                          {30, 60, 0},
                          {30, 70, 0},
                          {30, 80, 0},
                          {30, 90, 0},
                          {40, 0, 0},
                          {40, 10, 0},
                          {40, 20, 0},
                          {40, 30, 0},
                          {40, 40, 0},
                          {40, 50, 0},
                          {40, 60, 0},
                          {40, 70, 0},
                          {40, 80, 0},
                          {40, 90, 0},
                          {50, 0, 0},
                          {50, 10, 0},
                          {50, 20, 0},
                          {50, 30, 0},
                          {50, 40, 0},
                          {50, 50, 0},
                          {50, 60, 0},
                          {50, 70, 0},
                          {50, 80, 0},
                          {50, 90, 0},
                          {60, 0, 0},
                          {60, 10, 0},
                          {60, 20, 0},
                          {60, 30, 0},
                          {60, 40, 0},
                          {60, 50, 0},
                          {60, 60, 0},
                          {60, 70, 0},
                          {60, 80, 0},
                          {60, 90, 0},
                          {70, 0, 0},
                          {70, 10, 0},
                          {70, 20, 0},
                          {70, 30, 0},
                          {70, 40, 0},
                          {70, 50, 0},
                          {70, 60, 0},
                          {70, 70, 0},
                          {70, 80, 0},
                          {70, 90, 0},
                          {80, 0, 0},
                          {80, 10, 0},
                          {80, 20, 0},
                          {80, 30, 0},
                          {80, 40, 0},
                          {80, 50, 0},
                          {80, 60, 0},
                          {80, 70, 0},
                          {80, 80, 0},
                          {80, 90, 0},
                          {90, 0, 0},
                          {90, 10, 0},
                          {90, 20, 0},
                          {90, 30, 0},
                          {90, 40, 0},
                          {90, 50, 0},
                          {90, 60, 0},
                          {90, 70, 0},
                          {90, 80, 0},
                          {90, 90, 0},
                      },
                      {
                          5.46003480323149,
                          13.535533905932738,
                          5.46003480323149,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          7.384535700530241,
                          17.071067811865476,
                          7.384535700530241,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          5.46003480323149,
                          13.535533905932738,
                          5.46003480323149,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                      },
                      true);
    // Individual target2({{0.3, 0.3, 0.3}, {0.7, 0.1, 0.05}, {0.7, 0.1, 0.05}, {0.7, 0.1, 0.05}, {0.7, 0.1, 0.05}, {0.7, 0.1, 0.05}});
    Individual answer({{0, 10, 10}, {10, 10, 10}, {20, 10, 10}, {30, 10, 10}, {40, 10, 10}, {50, 10, 10}, {60, 10, 10}, {70, 10, 10}, {80, 10, 10}, {90, 10, 10}},
                      {1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000}, true, {60, 60, 60, 60, 60, 60, 60, 60, 60, 60});
    answer.calculate_fitness(target.get_positions(), target.get_candel_values());
    std::cout << "Answer fitness: " << answer.get_fitness() << std::endl;

    size_t mutation_probability = 10;
    size_t crossover_probability = 70;
    size_t parent_ratio = 1;
    size_t tournament_size = 20;
    size_t population_size = 2000;
    size_t max_positions = 20;
    size_t dimensions = 3;
    size_t min = 0;
    size_t max = 100;
    bool roulette_selection_used = false;
    bool individual_angle_included = true;

    for (int i = 0; i < 4; i++)
    {
        std::string log_file_name = "ga3_exp016_" + std::to_string(i + 1) + ".txt";
        GeneticAlgorithm ga(target,
                            mutation_probability,
                            crossover_probability,
                            parent_ratio,
                            tournament_size,
                            population_size,
                            max_positions,
                            dimensions,
                            min,
                            max,
                            roulette_selection_used,
                            individual_angle_included,
                            log_file_name);
        ga.run(300);
    }

    // mutate and crossover examples
    // target.print();
    // target2.print();
    // Individual ind = ga.crossover(target, target2);
    // ind.print();

    // ga.mutate(ind);
    // ind.print();

    // tournament example
    // Individual tournament_winner = ga.tournament();
    // std::cout << "Tournament winner: " << std::endl;
    // tournament_winner.print();

    // Run the genetic algorithm
}