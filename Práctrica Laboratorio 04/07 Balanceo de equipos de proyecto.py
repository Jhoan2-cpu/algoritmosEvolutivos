import pandas as pd
import random
import numpy as np

# Leer dataset
df = pd.read_excel('dataset.xlsx', sheet_name= "Students")  # Cambia la ruta

# Datos
gpas = df['GPA'].tolist()
skills = df['Skill'].tolist()
students = df['StudentID'].tolist()

num_alumnos = len(df)
num_equipos = 5
tam_equipo = 4

# Crear mapa de habilidades únicas a índices
habilidades_unicas = list(df['Skill'].unique())
habilidades_map = {h: i for i, h in enumerate(habilidades_unicas)}

# Vectorizar habilidades como one-hot
habilidades_vect = []
for h in skills:
    vec = [0]*len(habilidades_unicas)
    vec[habilidades_map[h]] = 1
    habilidades_vect.append(vec)

# Función varianza GPA
def varianza_gpa(equipos):
    varianzas = []
    for equipo in equipos:
        gpas_equipo = [gpas[i] for i in equipo]
        varianzas.append(np.var(gpas_equipo))
    return sum(varianzas)

# Penalización por desequilibrio habilidades (varianza conteos)
def penalizacion_habilidades(equipos):
    conteos = []
    for equipo in equipos:
        suma_cat = np.sum([habilidades_vect[i] for i in equipo], axis=0)
        conteos.append(suma_cat)
    conteos = np.array(conteos)
    varianzas_cat = np.var(conteos, axis=0)
    return np.sum(varianzas_cat)

# Aptitud combinada
def aptitud(equipos):
    return varianza_gpa(equipos) + penalizacion_habilidades(equipos)

# Vecino: swap dos alumnos de equipos distintos
def generar_vecino(equipos):
    vecino = [list(e) for e in equipos]
    eq1, eq2 = random.sample(range(num_equipos), 2)
    a1 = random.choice(vecino[eq1])
    a2 = random.choice(vecino[eq2])
    vecino[eq1].remove(a1)
    vecino[eq1].append(a2)
    vecino[eq2].remove(a2)
    vecino[eq2].append(a1)
    return vecino

# Inicializar solución aleatoria
def inicializar_solucion():
    alumnos = list(range(num_alumnos))
    random.shuffle(alumnos)
    equipos = []
    for i in range(num_equipos):
        equipos.append(alumnos[i*tam_equipo:(i+1)*tam_equipo])
    return equipos

# Hill Climbing
def hill_climbing(max_iter=10000):
    mejor_sol = inicializar_solucion()
    mejor_apt = aptitud(mejor_sol)

    for _ in range(max_iter):
        vecino = generar_vecino(mejor_sol)
        apt = aptitud(vecino)
        if apt < mejor_apt:
            mejor_apt = apt
            mejor_sol = vecino

    return mejor_sol, mejor_apt

# Ejecutar
equipos_opt, aptitud_opt = hill_climbing()

print("Equipos formados:")
for i, equipo in enumerate(equipos_opt):
    nombres = [students[idx] for idx in equipo]
    gpas_equipo = [gpas[idx] for idx in equipo]
    skills_equipo = [skills[idx] for idx in equipo]
    print(f"Equipo {i+1}:")
    for n, g, s in zip(nombres, gpas_equipo, skills_equipo):
        print(f"  {n} - GPA: {g:.2f}, Skill: {s}")
    print()

print(f"Aptitud total (varianzas): {aptitud_opt:.4f}")
