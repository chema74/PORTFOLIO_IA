# ==========================================================
# 1. IMPORTACIONES
# ==========================================================
# Este archivo actúa como punto de entrada principal del
# proyecto Analista de Riesgo País con IA.
#
# Permite:
# 1. recalcular el ranking
# 2. generar informes para todos los países
# 3. generar el informe de un país concreto
#
# Ejemplos de uso:
# python src/main.py --ranking
# python src/main.py --informes
# python src/main.py --pais "México"
# python src/main.py --ranking --informes
import argparse
from pathlib import Path
import sys


# ==========================================================
# 2. CONFIGURACIÓN DE RUTAS DEL PROYECTO
# ==========================================================
# Añadimos la raíz del proyecto al path para poder importar
# módulos internos desde src/.
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


# ==========================================================
# 3. IMPORTACIONES DE MÓDULOS DEL PROYECTO
# ==========================================================
from src.scoring.scoring_base import ejecutar_scoring
from src.analysis.generar_informe import (
    generar_informes_para_todos,
    generar_informe_por_pais,
)


# ==========================================================
# 4. PARSER DE ARGUMENTOS
# ==========================================================
def construir_parser() -> argparse.ArgumentParser:
    """
    Construye el parser de argumentos para línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description="Herramienta CLI del proyecto Analista de Riesgo País con IA"
    )

    parser.add_argument(
        "--ranking",
        action="store_true",
        help="Recalcula el ranking de riesgo país a partir del CSV de ejemplos.",
    )

    parser.add_argument(
        "--informes",
        action="store_true",
        help="Genera informes para todos los países del ranking.",
    )

    parser.add_argument(
        "--pais",
        type=str,
        help='Genera el informe solo para el país indicado. Ejemplo: --pais "México"',
    )

    return parser


# ==========================================================
# 5. FUNCIONES DE EJECUCIÓN
# ==========================================================
def ejecutar_ranking() -> None:
    """
    Ejecuta el cálculo del ranking y muestra un resumen.
    """
    df = ejecutar_scoring()

    print("\n==========================================================")
    print("RANKING DE RIESGO PAÍS ACTUALIZADO")
    print("==========================================================")
    print(df[["pais", "score_global", "clasificacion_riesgo", "recomendacion"]])


def ejecutar_informes_todos() -> None:
    """
    Genera informes para todos los países disponibles.
    """
    rutas = generar_informes_para_todos()

    print("\n==========================================================")
    print("INFORMES GENERADOS PARA TODOS LOS PAÍSES")
    print("==========================================================")
    for ruta in rutas:
        print(ruta)

    print("\nTotal de informes generados:", len(rutas))


def ejecutar_informe_pais(nombre_pais: str) -> None:
    """
    Genera el informe de un único país.
    """
    ruta = generar_informe_por_pais(nombre_pais)

    print("\n==========================================================")
    print("INFORME GENERADO CORRECTAMENTE")
    print("==========================================================")
    print("País:", nombre_pais)
    print("Ruta:", ruta)


# ==========================================================
# 6. LÓGICA PRINCIPAL
# ==========================================================
def main() -> None:
    """
    Punto de entrada principal del programa.
    """
    parser = construir_parser()
    args = parser.parse_args()

    # Si el usuario no pasa ningún argumento, mostramos ayuda.
    if not any([args.ranking, args.informes, args.pais]):
        parser.print_help()
        return

    # 1. Recalcular ranking si se solicita
    if args.ranking:
        ejecutar_ranking()

    # 2. Generar todos los informes si se solicita
    if args.informes:
        ejecutar_informes_todos()

    # 3. Generar informe de un país concreto si se solicita
    if args.pais:
        ejecutar_informe_pais(args.pais)


# ==========================================================
# 7. PUNTO DE ENTRADA
# ==========================================================
if __name__ == "__main__":
    main()