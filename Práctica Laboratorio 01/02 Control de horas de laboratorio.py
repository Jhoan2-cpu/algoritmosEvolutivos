# Ejercicio 2: Control de horas de laboratorio
# -------------------------------------------
import pandas as pd
# 1. Construimos el diccionario de datos
datos = {
 'Estudiante': ['Ana', 'Luis', 'María', 'Juan', 'Carla'],
 'Horas_usadas': [3, 5, 2, 4, 1]
}
# 2. Convertimos el diccionario en un DataFrame de Pandas
df = pd.DataFrame(datos)
# 3. Calculamos el costo total por estudiante (S/ 2.00 por hora)
# Creamos una nueva columna 'Costo_total'
df['Costo_total'] = df['Horas_usadas'] * 2.0
# 4. Mostramos el DataFrame completo
print("=== DataFrame de uso de laboratorio ===")
print(df)
# 5. Estadísticas descriptivas de la columna 'Costo_total'
# describe() devuelve conteo, media, std, min, percentiles y max
stats = df['Costo_total'].describe()
print("\n=== Estadísticas de Costo_total ===")
print(stats)
# 6. Filtramos los estudiantes con gasto mayor a S/ 6.00
# Creamos un DataFrame con la condición df['Costo_total'] > 6.0
df_mayor_6 = df[df['Costo_total'] > 6.0]
# 7. Imprimimos el gasto promedio y la lista de estudiantes con gasto > S/6.00
gasto_promedio = stats['mean']
lista_altos = df_mayor_6['Estudiante'].tolist()
print(f"\nEl gasto promedio por estudiante fue de S/ {gasto_promedio:.2f}.")
print("Estudiantes que gastaron más de S/ 6.00:")
for alumno in lista_altos:
 print(f" - {alumno}")