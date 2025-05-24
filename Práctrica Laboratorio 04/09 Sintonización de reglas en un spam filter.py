import pandas as pd
import numpy as np
from deap import base, creator, tools
from sklearn.metrics import f1_score
import random
import matplotlib.pyplot as plt

# --- Cargar dataset desde Excel ---
df = pd.read_excel('dataset.xlsx', sheet_name='Emails')  # Cambia la ruta por la correcta

# Extraer features y target
features = ['Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5']
X_val = df[features].values
y_val = df['Spam'].values

# --- DEAP setup ---

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # Maximizar F1
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Genotipo: 5 pesos [0,1] + 1 umbral [0,5]
toolbox.register("attr_float_weight", random.uniform, 0.0, 1.0)
toolbox.register("attr_float_threshold", random.uniform, 0.0, 5.0)

def create_individual():
    weights = [toolbox.attr_float_weight() for _ in range(5)]
    threshold = toolbox.attr_float_threshold()
    ind = creator.Individual(weights + [threshold])
    return ind


toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Predicción usando individuo
def predict(individual, X):
    weights = np.array(individual[:5])
    threshold = individual[5]
    scores = np.dot(X, weights)
    preds = (scores >= threshold).astype(int)
    return preds

# Evaluar fitness: F1-score
def eval_fitness(individual):
    preds = predict(individual, X_val)
    return (f1_score(y_val, preds),)

toolbox.register("evaluate", eval_fitness)

# Mutación gaussiana pequeña
def mutate_individual(individual, mu=0, sigma=0.05, indpb=0.5):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] += random.gauss(mu, sigma)
            # Clamp pesos y umbral
            if i < 5:
                individual[i] = min(max(individual[i], 0.0), 1.0)
            else:
                individual[i] = min(max(individual[i], 0.0), 5.0)
    return individual,

toolbox.register("mutate", mutate_individual)

# Hill climbing local
def hill_climb_local(individual, max_iter=20):
    current = individual[:]
    current_fit = eval_fitness(current)[0]

    for _ in range(max_iter):
        neighbors = []
        for i in range(len(current)):
            neighbor = current[:]
            neighbor[i] += random.gauss(0, 0.05)
            if i < 5:
                neighbor[i] = min(max(neighbor[i], 0.0), 1.0)
            else:
                neighbor[i] = min(max(neighbor[i], 0.0), 5.0)
            neighbors.append(neighbor)
        fits = [eval_fitness(n)[0] for n in neighbors]
        max_fit = max(fits)
        if max_fit > current_fit:
            current = neighbors[fits.index(max_fit)]
            current_fit = max_fit
        else:
            break
    return current

def mutate_and_hillclimb(individual):
    toolbox.mutate(individual)
    improved = hill_climb_local(individual)
    for i in range(len(individual)):
        individual[i] = improved[i]
    del individual.fitness.values
    return individual,

toolbox.register("mutate_hc", mutate_and_hillclimb)

# --- Algoritmo principal ---

def main():
    random.seed(42)
    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    ngen = 50
    log = []

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    hof.update(pop)
    log.append(stats.compile(pop))

    for gen in range(1, ngen+1):
        offspring = []
        for ind in pop:
            mutant = toolbox.clone(ind)
            toolbox.mutate_hc(mutant)
            offspring.append(mutant)

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop = offspring
        hof.update(pop)
        record = stats.compile(pop)
        log.append(record)

        print(f"Gen {gen}: Max F1 = {record['max']:.4f}, Avg F1 = {record['avg']:.4f}")

    best = hof[0]
    print("\nMejores pesos y umbral encontrados:")
    print(f"Pesos: {best[:5]}")
    print(f"Umbral: {best[5]:.4f}")
    print(f"F1-score: {hof[0].fitness.values[0]:.4f}")

    # Graficar convergencia
    max_vals = [x['max'] for x in log]
    avg_vals = [x['avg'] for x in log]

    plt.plot(max_vals, label='Max F1-score')
    plt.plot(avg_vals, label='Avg F1-score')
    plt.xlabel('Generación')
    plt.ylabel('F1-score')
    plt.title('Convergencia F1-score Evolución Spam Filter')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
