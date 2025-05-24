import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Carga datos
df = pd.read_excel('dataset.xlsx', sheet_name='Enrollments')  # Cambia la ruta si es necesario

# Variables predictoras
X = df[['Credits', 'Prev_GPA', 'Extracurricular_hours']].values

# Variable objetivo: Categoría con 3 clases: Alta, Media, Baja
y_labels = df['Category'].values

# Codificar etiquetas a números
le = LabelEncoder()
y_int = le.fit_transform(y_labels)

# One-hot encoding para salida categórica
y = to_categorical(y_int)

# Escalar variables predictoras
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir en train y validación
X_train, X_val, y_train, y_val = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y_int
)

# Construir modelo simple de red neuronal
model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(y_train.shape[1], activation='softmax'))

# Compilar modelo
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Entrenar modelo
history = model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_val, y_val), verbose=1)

# Evaluar en validación
loss, acc = model.evaluate(X_val, y_val, verbose=0)
print(f"Accuracy en validación: {acc:.4f}")
