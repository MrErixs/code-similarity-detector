import pandas as pd

# Ruta del CSV original
csv_path = "../data/H-AIRosettaMP.csv"
output_path = "../outputs/cpp_dataset.csv"

print("Cargando datos del CSV...")
df = pd.read_csv(csv_path)

print(f"Total de filas en el archivo: {len(df)}")
print(f"Columnas disponibles: {df.columns.tolist()}")

# Filtrar por lenguaje "cpp"
cpp_df = df[df['language_name'] == 'cpp'].copy()
print(f"\nTotal de códigos en C++: {len(cpp_df)}")

# Crear mapeo para la columna 'target'
# "Ai_generated" -> 1, "Human_written" -> 0
provenance_mapping = {
    'Ai_generated': 1,
    'Human_written': 0
}

cpp_df['target'] = cpp_df['target'].map(provenance_mapping)

# Verificar si hay valores no mapeados
if cpp_df['target'].isna().any():
    print("\nValores únicos en 'target' que no se pudieron mapear:")
    unmapped = cpp_df[cpp_df['target'].isna()]['target'].unique()
    print(unmapped)

# Seleccionar solo las columnas 'code' y 'target'
output_df = cpp_df[['code', 'target']].copy()

# Eliminar duplicados en la columna 'code'
output_df = output_df.drop_duplicates(subset=['code'])

# Eliminar filas con valores nulos
output_df = output_df.dropna()

print(f"\nTotal de filas después de procesar: {len(output_df)}")
print(f"\nDistribución de clases:")
print(output_df['target'].value_counts())
print(f"  - Código IA (1): {(output_df['target'] == 1).sum()}")
print(f"  - Código Humano (0): {(output_df['target'] == 0).sum()}")

# Guardar el CSV
output_df.to_csv(output_path, index=False)
print(f"\n✓ CSV guardado en: {output_path}")
