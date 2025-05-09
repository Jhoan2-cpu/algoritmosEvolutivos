import numpy as np

# Crear los arrays de Numpy para los paquetes (GB) y los precios
paquetes = np.array([1, 2, 5, 10])
precios = np.array([5, 9, 20, 35])

# Calcular el costo por GB
costo_GB = precios / paquetes

# Encontrar el paquete más económico
costo_min = costo_GB.min()
indice_min = costo_GB.argmin()

# Mostrar los resultados
print("Costo por GB para cada paquete:")
for i, paquete in enumerate(paquetes):
    print(f"Paquete de {paquete}GB: S/{costo_GB[i]:.2f} por GB")

print(f"\nEl paquete de {paquetes[indice_min]}GB es el más económico con un costo de S/{costo_min:.2f} por GB")
