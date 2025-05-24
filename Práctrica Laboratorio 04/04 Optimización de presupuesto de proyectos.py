import pandas as pd
import random
import math

# Paso 1: Leer datos desde Excel
df = pd.read_excel('dataset.xlsx', sheet_name = 'Projects')  # Cambia por la ruta de tu archivo

costos = df['Cost_Soles'].tolist()
beneficios = df['Benefit_Soles'].tolist()
n = len(costos)
presupuesto_max = 10000

# Función aptitud
def aptitud(bitstring):
    costo_total = sum(costos[i] for i in range(n) if bitstring[i] == 1)
    if costo_total > presupuesto_max:
        return -math.inf  # Penaliza soluciones inválidas
    beneficio_total = sum(beneficios[i] for i in range(n) if bitstring[i] == 1)
    return beneficio_total

# Generar vecinos (voltear un bit)
def vecinos(bitstring):
    vecinos = []
    for i in range(n):
        vecino = bitstring.copy()
        vecino[i] = 1 - vecino[i]
        vecinos.append(vecino)
    return vecinos

# Hill Climbing
def hill_climbing(max_iter=1000):
    while True:
        sol = [random.randint(0,1) for _ in range(n)]
        if aptitud(sol) != -math.inf:
            break

    mejor_sol = sol
    mejor_apt = aptitud(sol)

    for _ in range(max_iter):
        mejor_vecino = None
        mejor_apt_vecino = -math.inf
        for vecino in vecinos(mejor_sol):
            a = aptitud(vecino)
            if a > mejor_apt_vecino:
                mejor_apt_vecino = a
                mejor_vecino = vecino
        if mejor_apt_vecino > mejor_apt:
            mejor_sol = mejor_vecino
            mejor_apt = mejor_apt_vecino
        else:
            break

    return mejor_sol, mejor_apt

# Ejecutar
sol_optima, beneficio_optimo = hill_climbing(1000)

# Mostrar resultados
proyectos_seleccionados = df['ProjectID'][[i for i, bit in enumerate(sol_optima) if bit == 1]].tolist()
costo_total = sum(costos[i] for i in range(n) if sol_optima[i] == 1)

print("Proyectos seleccionados:", proyectos_seleccionados)
print(f"Costo total: S/ {costo_total}")
print(f"Beneficio total: S/ {beneficio_optimo}")
