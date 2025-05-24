import pandas as pd
import numpy as np

# Leer dataset desde Excel
df = pd.read_excel('dataset.xlsx', sheet_name='Tesistas')  # Cambia la ruta a tu archivo

num_tesistas = len(df)
salas = list(range(6))  # 6 salas
franjas = ['F1','F2','F3','F4','F5','F6']

tesistas = df['TesistaID'].tolist()

# Creamos una matriz de disponibilidad: (tesista, franja)
# True si el tesista puede estar en esa franja
disponibilidad = df[franjas].values.astype(bool)

max_continuas = 4

# Función para asignación inicial secuencial respetando disponibilidad y sin solapamientos
def asignacion_inicial():
    asignacion = []
    ocupacion = {(s,f): False for s in salas for f in franjas}

    for i, t in enumerate(tesistas):
        asignado = False
        for s in salas:
            for f in franjas:
                if disponibilidad[i][franjas.index(f)] and not ocupacion[(s,f)]:
                    asignacion.append({'Tesista': t, 'Sala': s, 'Franja': f})
                    ocupacion[(s,f)] = True
                    asignado = True
                    break
            if asignado:
                break
        if not asignado:
            asignacion.append({'Tesista': t, 'Sala': None, 'Franja': None})
    return pd.DataFrame(asignacion)

# Convertir franjas a números para continuidad
franjas_num = {f: idx for idx,f in enumerate(franjas)}

# Función verificar continuidad máxima 4 franjas
def verificar_continuidad(df_asig):
    for s in salas:
        franjas_ocupadas = sorted([franjas_num[f] for f in df_asig.loc[df_asig['Sala']==s, 'Franja'] if pd.notna(f)])
        if not franjas_ocupadas:
            continue
        count = 1
        max_count = 1
        for i in range(1,len(franjas_ocupadas)):
            if franjas_ocupadas[i] == franjas_ocupadas[i-1] + 1:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 1
        if max_count > max_continuas:
            return False
    return True

# Función calcular huecos (espacios vacíos entre franjas ocupadas)
def calcular_huecos(df_asig):
    huecos_totales = 0
    for s in salas:
        franjas_ocupadas = sorted([franjas_num[f] for f in df_asig.loc[df_asig['Sala']==s, 'Franja'] if pd.notna(f)])
        if not franjas_ocupadas:
            continue
        huecos = (franjas_ocupadas[-1] - franjas_ocupadas[0] +1) - len(franjas_ocupadas)
        huecos_totales += huecos
    return huecos_totales

# Generar vecinos moviendo un tesista a otra sala/franja respetando disponibilidad y sin solapamientos
def generar_vecinos(df_asig):
    vecinos = []
    for idx in df_asig.index:
        t = df_asig.loc[idx, 'Tesista']
        idx_tesista = tesistas.index(t)
        for s in salas:
            for f in franjas:
                if (df_asig['Sala'] == s).any() and (df_asig['Franja'] == f).any():
                    # ya ocupado
                    ocupados = df_asig.loc[(df_asig['Sala']==s) & (df_asig['Franja']==f)]
                    if len(ocupados) > 0 and ocupados.index[0] != idx:
                        continue
                if disponibilidad[idx_tesista][franjas.index(f)]:
                    vecino = df_asig.copy()
                    vecino.loc[idx, 'Sala'] = s
                    vecino.loc[idx, 'Franja'] = f
                    vecinos.append(vecino)
    return vecinos

# Función de costo: combina huecos y penalización por continuidad y no asignados
def costo(df_asig):
    no_asignados = df_asig['Sala'].isnull().sum() * 1000
    if not verificar_continuidad(df_asig):
        return 1e6 + no_asignados
    solapamientos = 0
    grupos = df_asig.groupby(['Sala', 'Franja']).size()
    solapamientos = grupos[grupos > 1].sum() if any(grupos > 1) else 0
    if solapamientos > 0:
        return 1e6 + no_asignados + solapamientos*10000
    huecos = calcular_huecos(df_asig)
    return huecos + no_asignados

# Hill Climbing
def hill_climbing(max_iter=1000):
    df_asig = asignacion_inicial()
    mejor_costo = costo(df_asig)
    mejor_asig = df_asig.copy()

    for _ in range(max_iter):
        vecinos = generar_vecinos(mejor_asig)
        mejor_vecino = None
        mejor_costo_vecino = float('inf')
        for v in vecinos:
            c = costo(v)
            if c < mejor_costo_vecino:
                mejor_costo_vecino = c
                mejor_vecino = v
        if mejor_costo_vecino < mejor_costo:
            mejor_costo = mejor_costo_vecino
            mejor_asig = mejor_vecino
        else:
            break

    return mejor_asig, mejor_costo

# Ejecutar
asignacion_final, costo_final = hill_climbing(1000)

print("Asignación final:")
print(asignacion_final.sort_values(['Sala','Franja']).reset_index(drop=True))
print(f"Costo total (huecos + penalizaciones): {costo_final}")
