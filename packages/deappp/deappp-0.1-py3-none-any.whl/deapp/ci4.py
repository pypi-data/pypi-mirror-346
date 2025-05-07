print("""
     
import random
from deap import base, creator, tools, algorithms

# 1. Objective Function (minimize sum of squares)
def eval_func(individual):
    return sum(x ** 2 for x in individual),  # Comma makes it a tuple for DEAP

# 2. Create Fitness and Individual Types
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimize objective
creator.create("Individual", list, fitness=creator.FitnessMin)

# 3. Register Components in Toolbox
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -5.0, 5.0)  # Random float between -5 and 5
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 4. Register Evolutionary Operators
toolbox.register("evaluate", eval_func)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# 5. Initialize Population
population = toolbox.population(n=50)
generations = 20

# 6. Evolutionary Process
for gen in range(generations):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

    # Evaluate fitness
    fits = list(map(toolbox.evaluate, offspring))
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    # Select the next generation
    population = toolbox.select(offspring, k=len(population))

# 7. Output the Best Result
best_ind = tools.selBest(population, k=1)[0]
print("Best individual:", best_ind)
print("Best fitness:", best_ind.fitness.values[0])




 """)