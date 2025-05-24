import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from deap import base, creator, tools
import random
import matplotlib.pyplot as plt

# --- Carga y preparación de datos ---
# Cambia la ruta y nombre del archivo si es necesario
df = pd.read_excel('dataset.xlsx', sheet_name='HousePrices')

# Se asume que la columna 'price' es el target y el resto las features
# Features: Rooms, Area_m2
X = df[['Rooms', 'Area_m2']].values
# Target: Price_Soles
y = df['Price_Soles'].values

# División en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Configuración DEAP ---

# Crear clase de fitness para minimizar RMSE
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Crear clase individuo, que es una lista con fitness asociado
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Definir atributo individual: float entre 0.001 y 10 (alpha de Ridge)
toolbox.register("attr_float", random.uniform, 0.001, 10.0)
# Individual de un solo valor (alpha)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=1)
# Población: lista de individuos
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función para evaluar un individuo (modelo Ridge con alpha)
def evalRidge(individual):
    alpha = individual[0]
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    return (rmse,)

toolbox.register("evaluate", evalRidge)

# Mutación gaussiana pequeña (sigma=0.1), sin cruce
def mutate_individual(individual, mu=0, sigma=0.1, indpb=1.0):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] += random.gauss(mu, sigma)
            # Limitar alpha al rango válido
            if individual[i] < 0.001:
                individual[i] = 0.001
            elif individual[i] > 10.0:
                individual[i] = 10.0
    return individual,

toolbox.register("mutate", mutate_individual)

# --- Algoritmo principal ---

def main():
    random.seed(42)

    # Crear población inicial
    pop = toolbox.population(n=20)

    # Hall of Fame para guardar el mejor individuo
    hof = tools.HallOfFame(1)

    # Estadísticas para seguimiento
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    ngen = 50  # Número de generaciones
    log = []

    # Evaluar población inicial
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    hof.update(pop)
    record = stats.compile(pop)
    log.append(record)

    for gen in range(1, ngen + 1):
        offspring = []

        # Mutar individuos actuales (sin cruce)
        for ind in pop:
            mutant = toolbox.clone(ind)
            toolbox.mutate(mutant)
            del mutant.fitness.values
            offspring.append(mutant)

        # Evaluar mutantes
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Combinar padres y mutantes
        combined = pop + offspring

        # Selección greedy: tomar los mejores 20 individuos
        combined.sort(key=lambda ind: ind.fitness.values)
        pop = combined[:20]

        hof.update(pop)
        record = stats.compile(pop)
        log.append(record)

        print(f"Gen {gen}: Min RMSE = {record['min']:.4f}, Avg RMSE = {record['avg']:.4f}")

    # Mostrar mejor resultado
    mejor_ind = hof[0]
    print(f"\nMejor alpha encontrado: {mejor_ind[0]:.4f}")
    print(f"Mejor RMSE: {mejor_ind.fitness.values[0]:.4f}")

    # Graficar curva de convergencia
    min_vals = [x['min'] for x in log]
    avg_vals = [x['avg'] for x in log]

    plt.plot(min_vals, label='Min RMSE')
    plt.plot(avg_vals, label='Avg RMSE')
    plt.xlabel('Generación')
    plt.ylabel('RMSE')
    plt.title('Curva de convergencia Hill Climbing + Población (DEAP)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
