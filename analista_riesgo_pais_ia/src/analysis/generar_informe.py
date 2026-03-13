# ==========================================================
# 1. IMPORTACIONES
# ==========================================================
# Este script genera informes ejecutivos en formato Markdown
# a partir del archivo de ranking producido por scoring_base.py.
#
# Objetivo:
# - leer el ranking calculado
# - seleccionar uno o varios países
# - construir un informe ejecutivo legible
# - guardar cada informe en outputs/informes/
#
# Este primer enfoque está pensado como una base funcional
# clara, explicable y fácilmente ampliable.
from pathlib import Path
import pandas as pd


# ==========================================================
# 2. CONFIGURACIÓN GENERAL DEL PROYECTO
# ==========================================================
# Tomamos como referencia la ubicación del propio script para
# reconstruir la ruta raíz del proyecto.
#
# Estructura esperada:
# analista-riesgo-pais-ia/
# ├── outputs/
# │   ├── rankings/
# │   │   └── ranking_riesgo_pais.csv
# │   └── informes/
# └── src/
#     └── analysis/
#         └── generar_informe.py
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_CSV = BASE_DIR / "outputs" / "rankings" / "ranking_riesgo_pais.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "informes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 3. MAPA DE NOMBRES DE DIMENSIONES
# ==========================================================
# Este diccionario traduce los nombres técnicos de columnas del
# dataset a nombres más legibles para el informe final.
DIMENSIONES = {
    "riesgo_politico_institucional": "Riesgo político e institucional",
    "riesgo_macroeconomico": "Riesgo macroeconómico",
    "riesgo_regulatorio_cumplimiento": "Riesgo regulatorio y de cumplimiento",
    "riesgo_geopolitico": "Riesgo geopolítico",
    "riesgo_comercial_operativo": "Riesgo comercial y operativo",
    "riesgo_sectorial": "Riesgo sectorial",
}


# ==========================================================
# 4. FUNCIONES AUXILIARES DE FORMATO
# ==========================================================
def normalizar_nombre_archivo(nombre_pais: str) -> str:
    """
    Convierte el nombre del país en una versión sencilla apta
    para nombres de archivo.

    Ejemplos:
        "Alemania" -> "alemania"
        "Reino Unido" -> "reino_unido"
    """
    return (
        nombre_pais.strip()
        .lower()
        .replace(" ", "_")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )


def interpretar_valor_dimension(valor: float) -> str:
    """
    Traduce un valor numérico 1-5 a una interpretación breve.
    """
    if valor <= 1.5:
        return "Exposición muy baja"
    elif valor <= 2.5:
        return "Exposición baja"
    elif valor <= 3.5:
        return "Exposición media"
    elif valor <= 4.5:
        return "Exposición alta"
    return "Exposición muy alta"


def obtener_factores_criticos(fila: pd.Series) -> list[str]:
    """
    Detecta las dimensiones más comprometidas del país.

    Regla:
    - Si una dimensión tiene valor >= 4, se considera crítica.
    - Si ninguna llega a 4, se muestran las 2 más altas como
      factores relevantes.
    """
    valores = []

    for columna, nombre_legible in DIMENSIONES.items():
        valores.append((nombre_legible, float(fila[columna])))

    criticos = [nombre for nombre, valor in valores if valor >= 4]

    if criticos:
        return criticos

    # Si no hay críticos duros, devolvemos las dos dimensiones
    # con mayor puntuación como áreas de atención.
    valores_ordenados = sorted(valores, key=lambda x: x[1], reverse=True)
    return [nombre for nombre, _ in valores_ordenados[:2]]


def obtener_fortalezas_relativas(fila: pd.Series) -> list[str]:
    """
    Detecta las dimensiones mejor valoradas del país.
    """
    valores = []

    for columna, nombre_legible in DIMENSIONES.items():
        valores.append((nombre_legible, float(fila[columna])))

    valores_ordenados = sorted(valores, key=lambda x: x[1])
    return [nombre for nombre, _ in valores_ordenados[:2]]


def generar_resumen_ejecutivo(fila: pd.Series) -> str:
    """
    Genera un párrafo ejecutivo breve a partir de score,
    clasificación y recomendación.
    """
    pais = fila["pais"]
    score = float(fila["score_global"])
    clasificacion = fila["clasificacion_riesgo"]
    recomendacion = fila["recomendacion"]

    if recomendacion == "Go":
        tono = (
            "presenta un perfil favorable para una operación internacional "
            "desde una perspectiva preliminar"
        )
    elif recomendacion == "Go condicionado":
        tono = (
            "presenta elementos de interés, aunque requiere cautela y "
            "validación adicional en dimensiones sensibles"
        )
    else:
        tono = (
            "presenta un nivel de exposición elevado que aconseja extrema "
            "prudencia antes de plantear una entrada operativa"
        )

    return (
        f"{pais} obtiene un score global de {score:.2f}, lo que lo sitúa en la "
        f"categoría **{clasificacion}**. A partir de la lógica metodológica "
        f"aplicada en este proyecto, la recomendación orientativa es "
        f"**{recomendacion}**. En términos generales, el país {tono}."
    )


def construir_bloque_dimensiones(fila: pd.Series) -> str:
    """
    Construye el bloque Markdown con el detalle por dimensión.
    """
    lineas = []

    for columna, nombre_legible in DIMENSIONES.items():
        valor = float(fila[columna])
        interpretacion = interpretar_valor_dimension(valor)
        lineas.append(f"- **{nombre_legible}:** {valor:.2f} — {interpretacion}")

    return "\n".join(lineas)


def construir_comentario_final(fila: pd.Series) -> str:
    """
    Genera un comentario de cierre con fortalezas y factores críticos.
    """
    factores_criticos = obtener_factores_criticos(fila)
    fortalezas = obtener_fortalezas_relativas(fila)

    texto_criticos = ", ".join(factores_criticos)
    texto_fortalezas = ", ".join(fortalezas)

    return (
        f"Las principales áreas de atención en este análisis son: "
        f"**{texto_criticos}**. Como fortalezas relativas del país dentro de "
        f"este modelo destacan: **{texto_fortalezas}**. Este resultado debe "
        f"interpretarse como una evaluación preliminar de apoyo a la decisión, "
        f"no como sustitución de un análisis experto integral."
    )


# ==========================================================
# 5. GENERACIÓN DE INFORME INDIVIDUAL
# ==========================================================
def generar_informe_markdown(fila: pd.Series) -> str:
    """
    Genera el contenido Markdown completo para un país.
    """
    pais = fila["pais"]
    region = fila["region"]
    score = float(fila["score_global"])
    clasificacion = fila["clasificacion_riesgo"]
    recomendacion = fila["recomendacion"]

    resumen = generar_resumen_ejecutivo(fila)
    bloque_dimensiones = construir_bloque_dimensiones(fila)
    comentario_final = construir_comentario_final(fila)

    contenido = f"""# Informe Ejecutivo — {pais}

## 1. Identificación del caso

- **País analizado:** {pais}
- **Región:** {region}
- **Score global:** {score:.2f}
- **Clasificación de riesgo:** {clasificacion}
- **Recomendación orientativa:** {recomendacion}

---

## 2. Resumen ejecutivo

{resumen}

---

## 3. Desglose por dimensiones

{bloque_dimensiones}

---

## 4. Lectura analítica

{comentario_final}

---

## 5. Recomendación orientativa

La recomendación final para **{pais}** dentro de esta versión del modelo es:

**{recomendacion}**

Esta recomendación debe leerse como una señal inicial de apoyo a la evaluación estratégica. En un desarrollo posterior del proyecto, esta salida podrá enriquecerse con fuentes, mayor trazabilidad, comparativa sectorial y generación agéntica de informes más extensos.

---

## 6. Nota metodológica

Este informe ha sido generado a partir del archivo `ranking_riesgo_pais.csv`, utilizando la metodología base del proyecto **Analista de Riesgo País con IA**. La clasificación sintetiza variables políticas, macroeconómicas, regulatorias, geopolíticas, comerciales y sectoriales en una lógica de evaluación preliminar.

[Inference] Al tratarse de un dataset de ejemplo y una primera versión funcional del sistema, esta salida debe entenderse como una simulación metodológica orientada a validación del modelo y construcción progresiva del proyecto.

---

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
"""
    return contenido


def guardar_informe_pais(fila: pd.Series) -> Path:
    """
    Genera y guarda el informe Markdown de un país.
    """
    pais = fila["pais"]
    nombre_archivo = f"informe_{normalizar_nombre_archivo(pais)}.md"
    ruta_salida = OUTPUT_DIR / nombre_archivo

    contenido = generar_informe_markdown(fila)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta_salida


# ==========================================================
# 6. PROCESO PRINCIPAL
# ==========================================================
def cargar_ranking() -> pd.DataFrame:
    """
    Lee el CSV de ranking previamente generado.
    """
    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de entrada esperado: {INPUT_CSV}"
        )

    df = pd.read_csv(INPUT_CSV)
    return df


def generar_informes_para_todos() -> list[Path]:
    """
    Genera informes para todos los países del ranking.
    """
    df = cargar_ranking()
    rutas_generadas = []

    for _, fila in df.iterrows():
        ruta = guardar_informe_pais(fila)
        rutas_generadas.append(ruta)

    return rutas_generadas


def generar_informe_por_pais(nombre_pais: str) -> Path:
    """
    Genera el informe únicamente para el país solicitado.
    """
    df = cargar_ranking()

    coincidencias = df[df["pais"].str.lower() == nombre_pais.strip().lower()]

    if coincidencias.empty:
        paises_disponibles = ", ".join(df["pais"].tolist())
        raise ValueError(
            f"No se encontró el país '{nombre_pais}'. "
            f"Países disponibles: {paises_disponibles}"
        )

    fila = coincidencias.iloc[0]
    return guardar_informe_pais(fila)


# ==========================================================
# 7. PUNTO DE ENTRADA
# ==========================================================
if __name__ == "__main__":
    rutas = generar_informes_para_todos()

    print("\n==========================================================")
    print("INFORMES EJECUTIVOS GENERADOS CORRECTAMENTE")
    print("==========================================================")

    for ruta in rutas:
        print(ruta)

    print("\nTotal de informes generados:", len(rutas))