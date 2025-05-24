
import pandas as pd
import random
import math

# Leer datos desde Excel
df = pd.read_excel('dataset.xlsx', sheet_name = 'ExamQuestions')  # Cambia la ruta a tu archivo

dificultad = df['Difficulty'].tolist()
tiempo = df['Time_min'].tolist()
n = len(dificultad)

tiempo_max = 90
dif_min = 180
dif_max = 200

def costo(bitstring):
    tiempo_total = sum(tiempo[i] for i in range(n) if bitstring[i] == 1)
    dificultad_total = sum(dificultad[i] for i in range(n) if bitstring[i] == 1)

    if tiempo_total > tiempo_max:
        return 1e6 + (tiempo_total - tiempo_max)*1000  # Penalización fuerte
    if dificultad_total < dif_min:
        return dif_min - dificultad_total  # Penalización leve
    if dificultad_total > dif_max:
        return dificultad_total - dif_max  # Penalización leve
    # Si cumple restricciones, queremos maximizar dificultad (min costo = -dificultad)
    return -dificultad_total

def vecinos(bitstring):
    vecinos = []
    for i in range(n):
        vecino = bitstring.copy()
        vecino[i] = 1 - vecino[i]  # Voltear bit
        vecinos.append(vecino)
    return vecinos

def hill_climbing(max_iter=1000):
    while True:
        sol = [random.randint(0,1) for _ in range(n)]
        if costo(sol) < 1e6:
            break

    mejor_sol = sol
    mejor_costo = costo(sol)

    for _ in range(max_iter):
        mejor_vecino = None
        mejor_costo_vecino = float('inf')
        for v in vecinos(mejor_sol):
            c = costo(v)
            if c < mejor_costo_vecino:
                mejor_costo_vecino = c
                mejor_vecino = v
        if mejor_costo_vecino < mejor_costo:
            mejor_costo = mejor_costo_vecino
            mejor_sol = mejor_vecino
        else:
            break

    return mejor_sol, mejor_costo

# Ejecutar
sol_optima, costo_optimo = hill_climbing(1000)

# Mostrar resultados
seleccionadas = [df['QuestionID'][i] for i, b in enumerate(sol_optima) if b == 1]
tiempo_total = sum(tiempo[i] for i in range(n) if sol_optima[i] == 1)
dificultad_total = sum(dificultad[i] for i in range(n) if sol_optima[i] == 1)

print("Preguntas seleccionadas:", seleccionadas)
print(f"Tiempo total: {tiempo_total} min")
print(f"Dificultad total: {dificultad_total}")
print(f"Costo función: {costo_optimo}")
