import numpy as np
presupuesto = 8.0
precios = np.array([0.10, 0.12, 0.80])
max_cafes = np.floor(presupuesto / precios)
cantidad_max = int(max_cafes.max())
indice_max = int(max_cafes.argmax())

precio_min = precios.min()
indice_precio_min = int(precios.argmin())
nombres = ['A', 'B', 'C']

print("=== Resultados Ejercicio FOTOCOPIAS PARA APUNTES ===")
for i, nombre in enumerate(nombres):
    print(f"Copistería {nombre}: precio por página S/ {precios[i]:.2f} → puede comprar {int(max_cafes[i])} páginas")
print(f"\nCon S/ {presupuesto:.2f} obtienes la mayor cantidad de fotocopias ({cantidad_max}) en la copistería {nombres[indice_max]}.")
print(f"El precio más bajo es S/ {precio_min:.2f} en la capistería {nombres[indice_precio_min]}.")
