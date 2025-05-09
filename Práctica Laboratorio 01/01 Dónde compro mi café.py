# Ejercicio 1: ¿Dónde compro mi café?
# ----------------------------------
import numpy as np
# 1. Definimos el presupuesto disponible (S/ 10)
presupuesto = 10.0
# 2. Creamos un array con los precios de café en cada cafetería
# A: 2.50, B: 3.00, C: 1.75, D: 2.20
precios = np.array([2.50, 3.00, 1.75, 2.20])
# 3. Calculamos cuántos cafés puede comprar en cada cafetería
# np.floor realiza la división y redondea hacia abajo al entero más próximo
max_cafes = np.floor(presupuesto / precios)
# 4. Encontramos la mayor cantidad de cafés posibles
# max_cafes.max() devuelve el valor máximo de cafés
# max_cafes.argmax() devuelve el índice (0-3) donde se alcanza ese máximo
cantidad_max = int(max_cafes.max())
indice_max = int(max_cafes.argmax())
# 5. Determinamos el precio mínimo y su índice
precio_min = precios.min()
indice_precio_min = int(precios.argmin())
# 6. Mapeo de índices a nombres de cafetería
nombres = ['A', 'B', 'C', 'D']
# 7. Imprimimos los resultados
print("=== Resultados Ejercicio Café ===")
for i, nombre in enumerate(nombres):
    print(f"Cafetería {nombre}: precio S/ {precios[i]:.2f} → puede comprar {int(max_cafes[i])} cafés")
print(f"\nCon S/ {presupuesto:.2f} obtienes la mayor cantidad de cafés ({cantidad_max}) en la cafetería {nombres[indice_max]}.")
print(f"El precio más bajo es S/ {precio_min:.2f} en la cafetería {nombres[indice_precio_min]}.")