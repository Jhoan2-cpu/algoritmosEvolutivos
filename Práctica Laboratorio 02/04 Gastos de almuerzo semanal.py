import pandas as pd

# Crear la lista de gastos
gastos = [4.0, 3.5, 5.0, 4.2, 3.8]

# Crear el DataFrame con la columna 'Gasto'
df = pd.DataFrame(gastos, columns=['Gasto'])

# Calcular el gasto total y el gasto medio de la semana
gasto_total = df['Gasto'].sum()
gasto_medio = df['Gasto'].mean()

# Filtrar los días en los que gastó más que el promedio
dias_mas_que_promedio = df[df['Gasto'] > gasto_medio]

# Mostrar los resultados
print(f"Gasto total de la semana: {gasto_total}")
print(f"Gasto medio de la semana: {gasto_medio}")
print("\nDías en los que gastó más que el promedio:")
print(dias_mas_que_promedio)
