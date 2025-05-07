print('''
import random
from deap import base, creator, tools, algorithms

def eval_func(individual):
    # Example evaluation function (minimize a quadratic function)
    return sum(x ** 2 for x in individual),

# Define the fitness and individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# Setup toolbox
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -5.0, 5.0)  # Float values between -5 and 5
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=3)  # 3-dimensional individual
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_func)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Create population
population = toolbox.population(n=50)
generations = 20

# Evolutionary loop
for gen in range(generations):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    
    # Evaluate offspring
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    # Select the next generation population
    population = toolbox.select(offspring, k=len(population))

# Final best individual
best_ind = tools.selBest(population, k=1)[0]
best_fitness = best_ind.fitness.values[0]
print("Best individual:", best_ind)
print("Best fitness:", best_fitness)

      ''')
