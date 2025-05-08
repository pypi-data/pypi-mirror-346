import random
from deap import base, creator, tools, algorithms


def run_ga():
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("bit", random.randint, 0, 1)
    toolbox.register(
        "individual", tools.initRepeat, creator.Individual, toolbox.bit, 10
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: (sum(ind),))
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=20)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, verbose=False)

    best = tools.selBest(pop, 1)[0]
    return best, sum(best)


# === 5. Hybrid GA   ==
# import numpy as np
# from sklearn.neural_network import MLPRegressor
# import random

# # Fake data: [Temp, FeedRate] → Yield
# X = np.random.rand(50, 2) * 100
# y = X[:, 0] * 0.5 + X[:, 1] * 0.3  # Simple target function

# # Train ANN
# model = MLPRegressor(hidden_layer_sizes=(5,), max_iter=300)
# model.fit(X, y)

# # GA Functions
# def fitness(p):
#     return model.predict([p])[0]
# def mutate(p):
#     return [v + random.uniform(-5, 5) for v in p]

# # GA Loop
# pop = [list(np.random.rand(2) * 100) for _ in range(6)]
# for _ in range(5):
#     pop = sorted(pop, key=fitness, reverse=True)
#     pop += [mutate(random.choice(pop[:3])) for _ in range(3)]
#     pop = pop[:6]

# # Best result
# best = max(pop, key=fitness)
# print("Best Parameters:", best)

# =================================================================
# 6. Clonal selection algorithm using Python.
# import numpy as np
# import random

# # Fitness function (example: maximize this)
# def fitness(x):
#     return -x**2 + 10  # Peak at x = 0

# # Generate random antibodies (solutions)
# population = [random.uniform(-5, 5) for _ in range(6)]

# # Clonal Selection Algorithm
# for _ in range(5):  # 5 generations
#     clones = []
#     for ab in population:
#         clones += [ab + random.uniform(-1, 1) for _ in range(2)]  # clone + mutate
#     population += clones
#     population = sorted(population, key=fitness, reverse=True)[:6]  # select best

# # Best antibody
# best = max(population, key=fitness)
# print("Best solution:", best)

# import matplotlib.pyplot as plt

# x = np.linspace(-5, 5, 100)
# y = -x**2 + 10
# plt.plot(x, y, label='Fitness Function')
# plt.scatter(best, fitness(best), color='red', label='Best Solution')
# plt.title('Clonal Selection Algorithm')
# plt.xlabel('x')
# plt.ylabel('Fitness')
# plt.legend()
# plt.grid()
# plt.show()
