import pandas as pd

# Crear el DataFrame con los datos proporcionados
data = {
    'Estudiante': ['Rosa', 'David', 'Elena', 'Mario', 'Paula'],
    'Días_prestamo': [7, 10, 5, 12, 3]
}
df = pd.DataFrame(data)

# Calcular el promedio y el máximo de los días de préstamo
promedio = df['Días_prestamo'].mean()
maximo = df['Días_prestamo'].max()

# Filtrar quiénes retuvieron el libro más de 8 días
filtrados = df[df['Días_prestamo'] > 8]

# Mostrar los resultados
print(f"Promedio de días de préstamo: {promedio}")
print(f"Día de préstamo máximo: {maximo}")
print("\nEstudiantes que retuvieron el libro más de 8 días:")
print(filtrados)
