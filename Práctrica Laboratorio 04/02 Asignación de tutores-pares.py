import pandas as pd
import random

# Paso 1: Leer Excel
df = pd.read_excel('dataset.xlsx', sheet_name='MentorAvailability')  # cambia el nombre al archivo correcto

# Convertimos la disponibilidad a un DataFrame booleano (sin la columna MentorID)
mentores = df['MentorID'].tolist()
disponibilidad = df.drop(columns=['MentorID']).astype(int).values  # matriz numpy 0/1

num_mentores, num_slots = disponibilidad.shape

# Función para obtener bloques de 2h disponibles para mentor m
def bloques_disponibles(disponibilidad, m):
    bloques = []
    for h in range(num_slots - 1):
        if disponibilidad[m][h] == 1 and disponibilidad[m][h+1] == 1:
            bloques.append(h)
    return bloques

# Función costo: cuenta choques entre mentores (bloques horarios que se solapan)
def choques(sol):
    choques_totales = 0
    for i in range(len(sol)):
        for j in range(i+1, len(sol)):
            if sol[i] == -1 or sol[j] == -1:
                continue
            bloque_i = {sol[i], sol[i]+1}
            bloque_j = {sol[j], sol[j]+1}
            if bloque_i.intersection(bloque_j):
                choques_totales += 1
    return choques_totales

# Asignación inicial aleatoria válida
def asignacion_inicial():
    sol = []
    for m in range(num_mentores):
        opciones = bloques_disponibles(disponibilidad, m)
        sol.append(random.choice(opciones) if opciones else -1)
    return sol

# Generar vecinos modificando asignación de un mentor
def vecinos(sol, mentor):
    opciones = bloques_disponibles(disponibilidad, mentor)
    return [sol[:mentor] + [h] + sol[mentor+1:] for h in opciones if h != sol[mentor]]

# Buscar mejor vecino con menor número de choques
def buscar_mejor_vecino(sol):
    mejor_sol = sol
    mejor_costo = choques(sol)
    for m in range(num_mentores):
        for vecino in vecinos(sol, m):
            c = choques(vecino)
            if c < mejor_costo:
                mejor_costo = c
                mejor_sol = vecino
    return mejor_sol, mejor_costo

# Algoritmo búsqueda local
def asignar_tutores(max_iter=1000):
    sol = asignacion_inicial()
    costo = choques(sol)
    iter = 0
    while costo > 0 and iter < max_iter:
        sol, costo = buscar_mejor_vecino(sol)
        iter += 1
    return sol, costo

# Ejecutar
sol_final, choques_final = asignar_tutores()

# Mostrar resultados
print("Asignación final:")
for m, slot in enumerate(sol_final):
    if slot == -1:
        print(f"{mentores[m]}: No tiene bloque disponible")
    else:
        print(f"{mentores[m]}: Bloque horarios {slot} y {slot+1}")

print(f"Número total de choques: {choques_final}")
