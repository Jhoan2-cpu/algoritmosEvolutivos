# Ejercicio 2: VIAJES AL CAMPUS
# -------------------------------------------
import numpy as np

presupuesto = 15.0
precios = np.array([2.50, 3.00, 1.80])
max_viajes = np.floor(presupuesto / precios)
cantidad_max = int(max_viajes.max())
indice_max = int(max_viajes.argmax())

precio_min = precios.min()
indice_precio_min = int(precios.argmin())
nombres = ['Bus', 'Combi', 'Tren']

print("=== Resultados Ejercicio Viajes al Campus ===")
for i, nombre in enumerate(nombres):
    print(f"medio de transporte {nombre}: precio por viaje S/ {precios[i]:.2f} → puede viajar {int(max_viajes[i])} veces")
print(f"\nCon S/ {presupuesto:.2f} obtienes la mayor cantidad de viajes ({cantidad_max}) en el {nombres[indice_max]}.")
print(f"El precio más bajo es S/ {precio_min:.2f} en el {nombres[indice_precio_min]}.")
