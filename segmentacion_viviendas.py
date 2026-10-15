# =============================================================================
# Trabajo Práctico: Segmentación de Jurisdicciones Argentinas con K-Means
# Materia : Procesamiento de Aprendizaje Automático
# Datos: INDEC - Viviendas particulares habitadas por jurisdicción (Año 2022)
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# -----------------------------------------------------------------------------
# PASO 1: Cargar los datos en un DataFrame
# -----------------------------------------------------------------------------
datos = {
    'Jurisdiccion': [
        'Ciudad Autónoma de Buenos Aires', 'Buenos Aires', 'Catamarca', 'Chaco',
        'Chubut', 'Córdoba', 'Corrientes', 'Entre Ríos', 'Formosa', 'Jujuy',
        'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquén', 'Río Negro',
        'Salta', 'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe',
        'Santiago del Estero', 'Tierra del Fuego', 'Tucumán'
    ],
    'Viviendas_Habitadas': [
        1391258, 5970702, 131978, 368728,
        213317, 1378237, 370958, 494473, 194689, 238141,
        140879, 124149, 639467, 420101, 254545, 276371,
        404504, 241436, 182886, 118047, 1273460,
        311361, 65535, 493794
    ]
}

df = pd.DataFrame(datos)

print("--- Datos cargados ---")
print(df.head())
print()


# -----------------------------------------------------------------------------
# PASO 2: Aplicar K-Means con 3 clusters
# -----------------------------------------------------------------------------
# Seleccionamos la columna numérica sobre la que vamos a agrupar
X = df[['Viviendas_Habitadas']]

# Creamos el modelo con 3 grupos y lo entrenamos
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)


# -----------------------------------------------------------------------------
# PASO 3: Asignar etiquetas interpretables a los clusters
# -----------------------------------------------------------------------------
# Obtenemos los centroides y los ordenamos de menor a mayor para
# asignar las etiquetas: Pocas, Normal y Muchas viviendas.
centroides = kmeans.cluster_centers_.flatten()
orden_centroides = centroides.argsort()

mapeo_etiquetas = {
    orden_centroides[0]: 'Pocas viviendas',
    orden_centroides[1]: 'Cantidad normal de viviendas',
    orden_centroides[2]: 'Muchas viviendas'
}

df['Segmento'] = df['Cluster'].map(mapeo_etiquetas)


# -----------------------------------------------------------------------------
# PASO 4: Mostrar a qué grupo pertenece cada jurisdicción
# -----------------------------------------------------------------------------
print("--- Resultados de la Segmentación ---")
print(df[['Jurisdiccion', 'Viviendas_Habitadas', 'Segmento']]
      .sort_values(by='Viviendas_Habitadas', ascending=False)
      .to_string(index=False))
print()


# -----------------------------------------------------------------------------
# PASO 5: Visualizar los resultados en un gráfico de dispersión
# -----------------------------------------------------------------------------
plt.figure(figsize=(12, 6))

# Colores para cada segmento
colores = {
    'Pocas viviendas': 'red',
    'Cantidad normal de viviendas': 'blue',
    'Muchas viviendas': 'green'
}

# Graficamos los puntos de cada segmento
for segmento in df['Segmento'].unique():
    subset = df[df['Segmento'] == segmento]
    plt.scatter(subset['Jurisdiccion'], subset['Viviendas_Habitadas'],
                label=segmento, color=colores[segmento], s=100)

# Líneas horizontales punteadas que marcan los centroides
for i, centroide in enumerate(centroides):
    plt.axhline(y=centroide, color='gray', linestyle='--', alpha=0.5,
                label=f'Centroide {mapeo_etiquetas[i]}')

plt.title('Segmentación de Jurisdicciones Argentinas por Viviendas Habitadas (2022)')
plt.xlabel('Jurisdicción')
plt.ylabel('Cantidad de Viviendas Habitadas')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()