import pandas as pd
import random
from pathlib import Path

# Carpeta principal donde están los datos del dataset
DATA_DIR = Path("data")

# Archivo CSV que contiene la relación entre autores (uid) y códigos (pid)
CSV_FILE = DATA_DIR / "dev.csv"

# Carpeta donde están guardados los archivos de código fuente.
# Cada archivo se llama igual que su pid, por ejemplo: 12180, 67901, etc.
CODE_DIR = DATA_DIR / "dev"

# Carpeta donde guardaremos los archivos generados por nuestros scripts
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Archivo de salida que contendrá los pares de códigos generados
OUTPUT_FILE = OUTPUT_DIR / "pairs.csv"

# Semilla para que los resultados aleatorios sean reproducibles.
# Es decir, si volvemos a correr el script, se generan los mismos pares.
random.seed(42)


def generate_positive_pairs(df, n_pairs_per_user=3):
    """
    Genera pares positivos.

    Un par positivo significa que los dos códigos fueron escritos
    por el mismo autor, por lo tanto tendrán label = 1.

    """

    pairs = []

    # Agrupamos el dataframe por autor.
    # Así podemos obtener todos los códigos que pertenecen al mismo uid.
    grouped = df.groupby("uid")

    # Recorremos cada autor y sus códigos asociados.
    for uid, group in grouped:
        pids = group["pid"].tolist()

        # Si un autor tiene menos de 2 códigos, no podemos formar un par.
        if len(pids) < 2:
            continue

        # Generamos cierta cantidad de pares positivos por cada autor.
        for _ in range(n_pairs_per_user):
            # Tomamos dos códigos diferentes del mismo autor.
            pid1, pid2 = random.sample(pids, 2)

            pairs.append({
                "pid1": pid1,
                "pid2": pid2,
                "uid1": uid,
                "uid2": uid,
                "label": 1
            })

    return pairs


def generate_negative_pairs(df, n_pairs):
    """
    Genera pares negativos.

    Un par negativo significa que los dos códigos fueron escritos
    por autores diferentes, por lo tanto tendrán label = 0.

    """

    pairs = []

    # Convertimos el dataframe a una lista de diccionarios para poder
    # seleccionar registros aleatorios fácilmente.
    rows = df.to_dict("records")

    # Seguimos generando pares hasta alcanzar la cantidad solicitada.
    while len(pairs) < n_pairs:
        # Tomamos dos registros aleatorios del dataset.
        row1, row2 = random.sample(rows, 2)

        # Solo nos interesa que sean de autores distintos.
        if row1["uid"] != row2["uid"]:
            pairs.append({
                "pid1": row1["pid"],
                "pid2": row2["pid"],
                "uid1": row1["uid"],
                "uid2": row2["uid"],
                "label": 0
            })

    return pairs


def main():
    # Cargamos el CSV del dataset.
    # Este archivo debe tener columnas uid y pid.
    df = pd.read_csv(CSV_FILE)

    print("Registros cargados:", len(df))
    print("Autores únicos:", df["uid"].nunique())

    # Generamos pares positivos:
    # códigos del mismo autor.
    positive_pairs = generate_positive_pairs(df, n_pairs_per_user=3)

    # Generamos la misma cantidad de pares negativos:
    # códigos de autores diferentes.
    # Esto mantiene el dataset balanceado entre label 1 y label 0.
    negative_pairs = generate_negative_pairs(df, n_pairs=len(positive_pairs))

    # Unimos positivos y negativos en una sola lista.
    all_pairs = positive_pairs + negative_pairs

    # Mezclamos los pares para que no queden primero todos los positivos
    # y luego todos los negativos.
    random.shuffle(all_pairs)

    # Convertimos la lista de pares en un dataframe.
    pairs_df = pd.DataFrame(all_pairs)

    # Creamos la ruta completa al archivo de código correspondiente a pid1.
    # Ejemplo: data/dev/12180
    pairs_df["path1"] = pairs_df["pid1"].apply(
        lambda pid: str(CODE_DIR / str(pid))
    )

    # Creamos la ruta completa al archivo de código correspondiente a pid2.
    # Ejemplo: data/dev/67901
    pairs_df["path2"] = pairs_df["pid2"].apply(
        lambda pid: str(CODE_DIR / str(pid))
    )

    # Guardamos el nuevo dataset de pares en outputs/pairs.csv.
    pairs_df.to_csv(OUTPUT_FILE, index=False)

    print("Pares positivos:", len(positive_pairs))
    print("Pares negativos:", len(negative_pairs))
    print("Archivo generado:", OUTPUT_FILE)


if __name__ == "__main__":
    main()