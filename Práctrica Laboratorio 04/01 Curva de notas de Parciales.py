import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Paso 1: Leer archivo Excel ---
df_full = pd.read_excel('dataset.xlsx', sheet_name='Grades')
df = df_full[['Parcial1', 'Parcial2', 'Parcial3']]

# --- Paso 2: Definir función fitness ---
def fitness(df, offset):
    df_offset = df + offset
    df_offset = df_offset.clip(0, 20)
    promedios = df_offset.mean(axis=1)

    #Porcentaje de aprobados
    porcentaje_aprobados = np.mean(promedios >= 11) * 100
    promedio_clase = promedios.mean()
    if promedio_clase > 14:
        penalizacion = (promedio_clase - 14) * 10
        return porcentaje_aprobados - penalizacion
    else:
        return porcentaje_aprobados


# --- Paso 3: Hill Climbing ---
def get_neighbors(current_offset, step=0.5, min_offset=-5, max_offset=5):
    neighbors = []
    if current_offset - step >= min_offset:
        neighbors.append(current_offset - step)
    if current_offset + step <= max_offset:
        neighbors.append(current_offset + step)
    return neighbors


def hill_climbing(df, max_iter=100, step=0.5):
    current_offset = 0
    current_score = fitness(df, current_offset)
    history = [(current_offset, current_score)]

    for _ in range(max_iter):
        neighbors = get_neighbors(current_offset, step)
        scores = [(offset, fitness(df, offset)) for offset in neighbors]

        # Obtener el mejor vecino
        best_neighbor = max(scores, key=lambda x: x[1])

        if best_neighbor[1] > current_score:
            current_offset, current_score = best_neighbor
            history.append((current_offset, current_score))
        else:
            break

    return current_offset, current_score, history

# Ejecutar algoritmo
offset_optimo, score_optimo, historial = hill_climbing(df)

print(f"Offset óptimo encontrado: {offset_optimo}")
print(f"Porcentaje de aprobados con offset óptimo: {score_optimo:.2f}%")

df_final = (df + offset_optimo).clip(0, 20)
promedios_final = df_final.mean(axis=1)
print(f"Promedio de la clase tras offset: {promedios_final.mean():.2f}")
print(f"Alumnos aprobados: {(promedios_final >= 11).sum()} de {len(promedios_final)}")

# --- Paso 4: Graficar evolución ---
offsets, scores = zip(*historial)
plt.plot(offsets, scores, marker='o')
plt.xlabel('Offset aplicado')
plt.ylabel('Fitness (Porcentaje de aprobados penalizado)')
plt.title('Evolución Hill Climbing')
plt.grid(True)
plt.show()