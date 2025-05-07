print(""""
      
import numpy as np

# Objective function to minimize: f(x) = x^2
def objective_function(x):
    return x ** 2

# Step 1: Initialize a random population within given bounds
def initialize_population(size, lower_bound, upper_bound):
    return np.random.uniform(lower_bound, upper_bound, size)

# Step 2: Clone selected antibodies based on clone factor
def clone(antibodies, num_clones):
    return np.repeat(antibodies, num_clones)

# Step 3: Apply Gaussian noise to clones (hypermutation)
def hypermutate(clones, mutation_rate):
    noise = np.random.normal(0, mutation_rate, clones.shape)
    return clones + noise

# Step 4: Select the best individuals based on fitness
def select_best(population, num_best):
    fitness = np.array([objective_function(x) for x in population])
    sorted_indices = np.argsort(fitness)
    return population[sorted_indices[:num_best]]

# Main Clonal Selection Algorithm
def clonal_selection_algorithm(pop_size=10, generations=20, clone_factor=5,
                               mutation_rate=0.1, lower_bound=-10, upper_bound=10):
    population = initialize_population(pop_size, lower_bound, upper_bound)

    for gen in range(generations):
        # Evaluate fitness of current population
        fitness = np.array([objective_function(x) for x in population])

        # Select top individuals
        best = select_best(population, pop_size // 2)

        # Clone selected individuals
        clones = clone(best, clone_factor)

        # Apply mutation to clones
        mutated_clones = hypermutate(clones, mutation_rate)

        # Select best from mutated clones for the new generation
        new_best = select_best(mutated_clones, pop_size)

        # Replace old population
        population = new_best

        # Log current best
        best_solution = population[np.argmin([objective_function(x) for x in population])]
        print(f"Generation {gen+1}: Best Solution = {best_solution:.5f}, Fitness = {objective_function(best_solution):.5f}")

    return best_solution

# Run the algorithm
best = clonal_selection_algorithm()

print("\nFinal Best Solution:", best)

      
      
      """)