# ==========================================================
# 1. IMPORTACIONES
# ==========================================================
# Usamos pandas para leer y manipular el archivo CSV.
# Path nos ayuda a construir rutas de archivo de forma segura.
from pathlib import Path
import pandas as pd


# ==========================================================
# 2. CONFIGURACIÓN GENERAL DEL PROYECTO
# ==========================================================
# Definimos la ruta base del proyecto tomando como referencia
# la ubicación actual de este script.
#
# Estructura esperada:
# analista-riesgo-pais-ia/
# ├── data/
# │   └── ejemplos/
# │       └── paises_ejemplo.csv
# └── src/
#     └── scoring/
#         └── scoring_base.py
BASE_DIR = Path(__file__).resolve().parents[2]

# Ruta al archivo CSV de entrada con los países de ejemplo.
INPUT_CSV = BASE_DIR / "data" / "ejemplos" / "paises_ejemplo.csv"

# Ruta de salida para guardar una versión recalculada del dataset.
OUTPUT_DIR = BASE_DIR / "outputs" / "rankings"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "ranking_riesgo_pais.csv"


# ==========================================================
# 3. PONDERACIONES DEL MODELO
# ==========================================================
# Estas ponderaciones provienen de la lógica metodológica
# definida en el proyecto.
#
# La suma total debe ser 1.0
PESOS = {
    "riesgo_politico_institucional": 0.25,
    "riesgo_macroeconomico": 0.20,
    "riesgo_regulatorio_cumplimiento": 0.20,
    "riesgo_geopolitico": 0.15,
    "riesgo_comercial_operativo": 0.10,
    "riesgo_sectorial": 0.10,
}


# ==========================================================
# 4. FUNCIONES DE APOYO
# ==========================================================
def calcular_score_global(fila: pd.Series) -> float:
    """
    Calcula el score global ponderado para un país.

    Parámetros:
        fila (pd.Series): Fila del DataFrame con las variables de riesgo.

    Retorna:
        float: Score global redondeado a 2 decimales.
    """
    score = 0.0

    for variable, peso in PESOS.items():
        score += fila[variable] * peso

    return round(score, 2)


def clasificar_riesgo(score: float) -> str:
    """
    Traduce el score numérico a una clasificación cualitativa.

    Bandas iniciales:
        1.00 a 1.80 -> Riesgo muy bajo
        1.81 a 2.60 -> Riesgo bajo
        2.61 a 3.40 -> Riesgo medio
        3.41 a 4.20 -> Riesgo alto
        4.21 a 5.00 -> Riesgo muy alto
    """
    if 1.00 <= score <= 1.80:
        return "Riesgo muy bajo"
    elif 1.81 <= score <= 2.60:
        return "Riesgo bajo"
    elif 2.61 <= score <= 3.40:
        return "Riesgo medio"
    elif 3.41 <= score <= 4.20:
        return "Riesgo alto"
    elif 4.21 <= score <= 5.00:
        return "Riesgo muy alto"
    else:
        return "Fuera de rango"


def generar_recomendacion(score: float, fila: pd.Series) -> str:
    """
    Genera una recomendación orientativa a partir del score global
    y de posibles factores críticos.

    Regla general:
        - Riesgo muy bajo / bajo -> Go
        - Riesgo medio -> Go condicionado
        - Riesgo alto / muy alto -> No-Go

    Regla adicional:
        Si alguna dimensión clave alcanza 5, endurecemos la recomendación.
    """
    factores_criticos = [
        "riesgo_politico_institucional",
        "riesgo_regulatorio_cumplimiento",
        "riesgo_geopolitico",
    ]

    # Si existe un valor extremo en una dimensión muy sensible,
    # adoptamos una postura más prudente.
    if any(fila[col] == 5 for col in factores_criticos):
        if score >= 3.00:
            return "No-Go"
        return "Go condicionado"

    if score <= 2.60:
        return "Go"
    elif score <= 3.40:
        return "Go condicionado"
    else:
        return "No-Go"


def validar_columnas(df: pd.DataFrame) -> None:
    """
    Comprueba que el DataFrame contiene todas las columnas necesarias.
    Lanza un error claro si falta alguna.
    """
    columnas_requeridas = [
        "pais",
        "region",
        "riesgo_politico_institucional",
        "riesgo_macroeconomico",
        "riesgo_regulatorio_cumplimiento",
        "riesgo_geopolitico",
        "riesgo_comercial_operativo",
        "riesgo_sectorial",
    ]

    faltantes = [col for col in columnas_requeridas if col not in df.columns]

    if faltantes:
        raise ValueError(
            f"Faltan columnas obligatorias en el CSV: {', '.join(faltantes)}"
        )


# ==========================================================
# 5. FUNCIÓN PRINCIPAL DEL PROCESO
# ==========================================================
def ejecutar_scoring() -> pd.DataFrame:
    """
    Lee el archivo CSV, recalcula score, clasificación y recomendación,
    ordena los países por nivel de riesgo y guarda el resultado.
    """
    # 1. Leer datos de entrada
    df = pd.read_csv(INPUT_CSV)

    # 2. Validar estructura mínima
    validar_columnas(df)

    # 3. Calcular score global con la metodología definida
    df["score_global"] = df.apply(calcular_score_global, axis=1)

    # 4. Calcular clasificación cualitativa
    df["clasificacion_riesgo"] = df["score_global"].apply(clasificar_riesgo)

    # 5. Generar recomendación orientativa
    df["recomendacion"] = df.apply(
        lambda fila: generar_recomendacion(fila["score_global"], fila),
        axis=1
    )

    # 6. Ordenar de menor a mayor riesgo
    df = df.sort_values(by="score_global", ascending=True).reset_index(drop=True)

    # 7. Guardar salida
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    return df


# ==========================================================
# 6. PUNTO DE ENTRADA DEL SCRIPT
# ==========================================================
if __name__ == "__main__":
    resultado = ejecutar_scoring()

    print("\n==========================================================")
    print("RANKING DE RIESGO PAÍS GENERADO CORRECTAMENTE")
    print("==========================================================")
    print(resultado[["pais", "score_global", "clasificacion_riesgo", "recomendacion"]])
    print("\nArchivo guardado en:")
    print(OUTPUT_CSV)