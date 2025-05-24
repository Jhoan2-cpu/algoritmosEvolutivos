import pandas as pd
import random

# Paso 1: Leer matriz de distancias desde Excel
df = pd.read_excel('dataset.xlsx', sheet_name='LabDistances', index_col=0)  # Cambia por el nombre correcto

# Convertimos el DataFrame a numpy array para mayor velocidad
distancias = df.values
num_labs = distancias.shape[0]

def distancia_total(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancias[ruta[i], ruta[i+1]]
    # Cerrar el ciclo (volver al inicio)
    total += distancias[ruta[-1], ruta[0]]
    return total

def generar_vecinos(ruta):
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i+1, len(ruta)):
            vecino = ruta.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

def hill_climbing(max_iter=1000):
    ruta = list(range(num_labs))
    random.shuffle(ruta)
    mejor_ruta = ruta
    mejor_distancia = distancia_total(ruta)

    for _ in range(max_iter):
        vecinos = generar_vecinos(mejor_ruta)
        mejor_vecino = None
        mejor_dist_vecino = float('inf')
        for vecino in vecinos:
            dist = distancia_total(vecino)
            if dist < mejor_dist_vecino:
                mejor_dist_vecino = dist
                mejor_vecino = vecino
        if mejor_dist_vecino < mejor_distancia:
            mejor_ruta = mejor_vecino
            mejor_distancia = mejor_dist_vecino
        else:
            break

    return mejor_ruta, mejor_distancia

ruta_optima, distancia_optima = hill_climbing(1000)

print("Ruta óptima encontrada (índices de laboratorios):")
print(ruta_optima)
print(f"Distancia total mínima: {distancia_optima:.2f} metros")

# Opcional: mostrar nombres de laboratorios
nombres = df.index.tolist()
ruta_nombres = [nombres[i] for i in ruta_optima]
print("Ruta óptima (nombres):")
print(" -> ".join(ruta_nombres))
