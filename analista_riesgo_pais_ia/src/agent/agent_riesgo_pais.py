# ==========================================================
# 1. CONTEXTO GENERAL DEL ARCHIVO
# ==========================================================
# Archivo: src/agent/agent_riesgo_pais.py
#
# Primera implementación programática de la capa agéntica del
# proyecto "Analista de Riesgo País con IA".
#
# Esta versión incorpora una corrección importante:
# evita que una misma dimensión aparezca simultáneamente como
# factor crítico y como fortaleza relativa.
# ==========================================================

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import pandas as pd


# ==========================================================
# 2. CONFIGURACIÓN DE RUTAS DEL PROYECTO
# ==========================================================
BASE_DIR = Path(__file__).resolve().parents[2]

RANKING_CSV = BASE_DIR / "outputs" / "rankings" / "ranking_riesgo_pais.csv"
SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt_riesgo_pais.md"


# ==========================================================
# 3. MAPA DE DIMENSIONES DEL MODELO
# ==========================================================
DIMENSIONES: Dict[str, str] = {
    "riesgo_politico_institucional": "Riesgo político e institucional",
    "riesgo_macroeconomico": "Riesgo macroeconómico",
    "riesgo_regulatorio_cumplimiento": "Riesgo regulatorio y de cumplimiento",
    "riesgo_geopolitico": "Riesgo geopolítico",
    "riesgo_comercial_operativo": "Riesgo comercial y operativo",
    "riesgo_sectorial": "Riesgo sectorial",
}


# ==========================================================
# 4. ESTRUCTURA DE RESPUESTA DEL AGENTE
# ==========================================================
@dataclass
class RespuestaAgente:
    pais: str
    score_global: float
    clasificacion_riesgo: str
    recomendacion: str
    informe: str


# ==========================================================
# 5. CLASE PRINCIPAL DEL AGENTE
# ==========================================================
class AgenteRiesgoPais:
    def __init__(
        self,
        ranking_csv_path: Path = RANKING_CSV,
        system_prompt_path: Path = SYSTEM_PROMPT_PATH,
    ) -> None:
        self.ranking_csv_path = ranking_csv_path
        self.system_prompt_path = system_prompt_path
        self.df_ranking = self._cargar_ranking()
        self.system_prompt = self._cargar_system_prompt()

    # ======================================================
    # 5.1. CARGA DE ACTIVOS
    # ======================================================
    def _cargar_ranking(self) -> pd.DataFrame:
        if not self.ranking_csv_path.exists():
            raise FileNotFoundError(
                f"No se encontró el ranking esperado en: {self.ranking_csv_path}"
            )
        return pd.read_csv(self.ranking_csv_path)

    def _cargar_system_prompt(self) -> str:
        if self.system_prompt_path.exists():
            return self.system_prompt_path.read_text(encoding="utf-8")
        return ""

    # ======================================================
    # 5.2. UTILIDADES DE RECUPERACIÓN
    # ======================================================
    def obtener_paises_disponibles(self) -> List[str]:
        return self.df_ranking["pais"].tolist()

    def buscar_pais(self, nombre_pais: str) -> pd.Series:
        coincidencias = self.df_ranking[
            self.df_ranking["pais"].str.lower() == nombre_pais.strip().lower()
        ]

        if coincidencias.empty:
            disponibles = ", ".join(self.obtener_paises_disponibles())
            raise ValueError(
                f"No se encontró el país '{nombre_pais}'. "
                f"Países disponibles: {disponibles}"
            )

        return coincidencias.iloc[0]

    def _obtener_valores_dimensiones(self, fila: pd.Series) -> List[Tuple[str, float]]:
        """
        Devuelve una lista de tuplas con formato:
        [(nombre_legible_dimension, valor), ...]
        """
        valores = []
        for columna, nombre_legible in DIMENSIONES.items():
            valores.append((nombre_legible, float(fila[columna])))
        return valores

    # ======================================================
    # 5.3. INTERPRETACIÓN DE DIMENSIONES
    # ======================================================
    def interpretar_dimension(self, valor: float) -> str:
        if valor <= 1.5:
            return "Exposición muy baja"
        elif valor <= 2.5:
            return "Exposición baja"
        elif valor <= 3.5:
            return "Exposición media"
        elif valor <= 4.5:
            return "Exposición alta"
        return "Exposición muy alta"

    def obtener_factores_criticos(self, fila: pd.Series) -> List[str]:
        """
        Regla corregida:
        - Si hay dimensiones >= 4, esas son factores críticos.
        - Si no las hay, devolvemos las 2 dimensiones de mayor valor
          como áreas principales de atención.
        """
        valores = self._obtener_valores_dimensiones(fila)

        criticos_duros = [nombre for nombre, valor in valores if valor >= 4]
        if criticos_duros:
            return criticos_duros

        valores_ordenados = sorted(valores, key=lambda x: x[1], reverse=True)
        return [nombre for nombre, _ in valores_ordenados[:2]]

    def obtener_fortalezas_relativas(self, fila: pd.Series) -> List[str]:
        """
        Regla corregida:
        - Las fortalezas se eligen entre las dimensiones no incluidas
          en factores críticos o áreas principales de atención.
        - Si tras excluirlas no quedan suficientes, se completan con
          las de menor valor no repetidas.
        """
        valores = self._obtener_valores_dimensiones(fila)
        factores_criticos = set(self.obtener_factores_criticos(fila))

        # Primero intentamos elegir fortalezas excluyendo los factores críticos
        candidatos = [(nombre, valor) for nombre, valor in valores if nombre not in factores_criticos]

        if len(candidatos) >= 2:
            candidatos_ordenados = sorted(candidatos, key=lambda x: x[1])
            return [nombre for nombre, _ in candidatos_ordenados[:2]]

        # Si no hay suficientes candidatos, completamos sin repetir
        valores_ordenados = sorted(valores, key=lambda x: x[1])
        fortalezas = []

        for nombre, _ in valores_ordenados:
            if nombre not in fortalezas and nombre not in factores_criticos:
                fortalezas.append(nombre)
            if len(fortalezas) == 2:
                break

        # Si aún no hay 2, completamos con las menores aunque haya empate estructural,
        # pero sin repetir elementos.
        if len(fortalezas) < 2:
            for nombre, _ in valores_ordenados:
                if nombre not in fortalezas:
                    fortalezas.append(nombre)
                if len(fortalezas) == 2:
                    break

        return fortalezas[:2]

    def construir_bloque_dimensiones(self, fila: pd.Series) -> str:
        lineas = []

        for columna, nombre_legible in DIMENSIONES.items():
            valor = float(fila[columna])
            interpretacion = self.interpretar_dimension(valor)
            lineas.append(f"- **{nombre_legible}:** {valor:.2f} — {interpretacion}")

        return "\n".join(lineas)

    # ======================================================
    # 5.4. GENERACIÓN DE TEXTO
    # ======================================================
    def generar_resumen_ejecutivo(
        self,
        fila: pd.Series,
        sector: Optional[str] = None,
        objetivo: Optional[str] = None,
    ) -> str:
        pais = fila["pais"]
        score = float(fila["score_global"])
        clasificacion = fila["clasificacion_riesgo"]
        recomendacion = fila["recomendacion"]

        complemento_sector = f" para el sector **{sector}**" if sector else ""
        complemento_objetivo = f" en un contexto de **{objetivo}**" if objetivo else ""

        if recomendacion == "Go":
            tono = "presenta un perfil global favorable dentro del modelo actual"
        elif recomendacion == "Go condicionado":
            tono = (
                "presenta elementos de interés, aunque exige cautela en varias "
                "dimensiones del análisis"
            )
        else:
            tono = (
                "presenta una exposición elevada dentro del marco metodológico "
                "del proyecto"
            )

        return (
            f"**{pais}** obtiene un score global de **{score:.2f}**, lo que lo sitúa "
            f"en la categoría **{clasificacion}**. La recomendación orientativa del "
            f"modelo es **{recomendacion}**. En esta evaluación preliminar{complemento_sector}"
            f"{complemento_objetivo}, el país {tono}."
        )

    def generar_nota_metodologica(self) -> str:
        return (
            "[Inference] Este análisis se apoya en el dataset interno de ejemplo "
            "y en la metodología del proyecto **Analista de Riesgo País con IA**, "
            "por lo que debe interpretarse como una evaluación preliminar de apoyo "
            "a la decisión, no como validación empírica definitiva ni como "
            "sustitución de análisis legal, fiscal, financiero o geoestratégico especializado."
        )

    def generar_comentario_final(self, fila: pd.Series) -> str:
        factores_criticos = self.obtener_factores_criticos(fila)
        fortalezas = self.obtener_fortalezas_relativas(fila)

        texto_criticos = ", ".join(factores_criticos)
        texto_fortalezas = ", ".join(fortalezas)

        return (
            f"Las principales áreas de atención del caso son: **{texto_criticos}**. "
            f"Como fortalezas relativas dentro del modelo destacan: **{texto_fortalezas}**. "
            f"La recomendación final debe leerse con prudencia metodológica y como "
            f"soporte inicial para priorización, filtrado o ampliación posterior del análisis."
        )

    def _convertir_lista_a_bullets(self, elementos: List[str]) -> str:
        return "\n".join(f"- {elemento}" for elemento in elementos)

    # ======================================================
    # 5.5. CONSTRUCCIÓN DE INFORMES
    # ======================================================
    def construir_informe_agente(
        self,
        fila: pd.Series,
        sector: Optional[str] = None,
        objetivo: Optional[str] = None,
        contexto: Optional[str] = None,
    ) -> str:
        pais = fila["pais"]
        region = fila["region"]
        score = float(fila["score_global"])
        clasificacion = fila["clasificacion_riesgo"]
        recomendacion = fila["recomendacion"]

        resumen = self.generar_resumen_ejecutivo(
            fila=fila,
            sector=sector,
            objetivo=objetivo,
        )

        bloque_dimensiones = self.construir_bloque_dimensiones(fila)
        factores_criticos = self.obtener_factores_criticos(fila)
        fortalezas = self.obtener_fortalezas_relativas(fila)
        comentario_final = self.generar_comentario_final(fila)
        nota_metodologica = self.generar_nota_metodologica()

        sector_txt = sector if sector else "No especificado"
        objetivo_txt = objetivo if objetivo else "Evaluación general"
        contexto_txt = contexto if contexto else "Apoyo preliminar a la decisión"

        return f"""# Informe Ejecutivo — {pais}

## 1. Identificación del caso

- **País analizado:** {pais}
- **Región:** {region}
- **Sector:** {sector_txt}
- **Objetivo del análisis:** {objetivo_txt}
- **Contexto de uso:** {contexto_txt}
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

## 4. Factores críticos

{self._convertir_lista_a_bullets(factores_criticos)}

---

## 5. Fortalezas relativas

{self._convertir_lista_a_bullets(fortalezas)}

---

## 6. Recomendación orientativa

La recomendación final del agente para **{pais}** es:

**{recomendacion}**

---

## 7. Lectura analítica de cierre

{comentario_final}

---

## 8. Nota metodológica

{nota_metodologica}

---

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
"""

    # ======================================================
    # 5.6. MÉTODOS PÚBLICOS
    # ======================================================
    def analizar_pais(
        self,
        pais: str,
        sector: Optional[str] = None,
        objetivo: Optional[str] = None,
        contexto: Optional[str] = None,
    ) -> RespuestaAgente:
        fila = self.buscar_pais(pais)

        informe = self.construir_informe_agente(
            fila=fila,
            sector=sector,
            objetivo=objetivo,
            contexto=contexto,
        )

        return RespuestaAgente(
            pais=str(fila["pais"]),
            score_global=float(fila["score_global"]),
            clasificacion_riesgo=str(fila["clasificacion_riesgo"]),
            recomendacion=str(fila["recomendacion"]),
            informe=informe,
        )

    def comparar_paises(
        self,
        pais_1: str,
        pais_2: str,
        objetivo: Optional[str] = None,
    ) -> str:
        fila_1 = self.buscar_pais(pais_1)
        fila_2 = self.buscar_pais(pais_2)

        score_1 = float(fila_1["score_global"])
        score_2 = float(fila_2["score_global"])

        if score_1 < score_2:
            pais_mas_favorable = fila_1["pais"]
            pais_mas_expuesto = fila_2["pais"]
        elif score_2 < score_1:
            pais_mas_favorable = fila_2["pais"]
            pais_mas_expuesto = fila_1["pais"]
        else:
            pais_mas_favorable = "Empate técnico"
            pais_mas_expuesto = "Empate técnico"

        objetivo_txt = objetivo if objetivo else "Comparación estratégica general"

        return f"""# Comparativa Ejecutiva — {fila_1['pais']} vs {fila_2['pais']}

## 1. Objetivo de la comparación

**{objetivo_txt}**

---

## 2. Resultado general

- **{fila_1['pais']}:** {score_1:.2f} — {fila_1['clasificacion_riesgo']} — {fila_1['recomendacion']}
- **{fila_2['pais']}:** {score_2:.2f} — {fila_2['clasificacion_riesgo']} — {fila_2['recomendacion']}

---

## 3. Lectura comparativa

El país comparativamente más favorable dentro del modelo actual es: **{pais_mas_favorable}**.  
El país que presenta mayor exposición relativa es: **{pais_mas_expuesto}**.

### Dimensiones destacadas de {fila_1['pais']}
{self.construir_bloque_dimensiones(fila_1)}

### Dimensiones destacadas de {fila_2['pais']}
{self.construir_bloque_dimensiones(fila_2)}

---

## 4. Conclusión orientativa

[Inference] Esta comparación se apoya en el dataset interno de ejemplo y en la lógica metodológica del proyecto, por lo que debe interpretarse como apoyo preliminar a la priorización entre mercados y no como validación empírica definitiva.

---

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
"""

# ==========================================================
# 6. DEMO LOCAL
# ==========================================================
def demo() -> None:
    agente = AgenteRiesgoPais()

    respuesta = agente.analizar_pais(
        pais="México",
        sector="agroalimentario",
        objetivo="evaluación preliminar de exportación",
        contexto="priorización de mercados internacionales",
    )

    print("\n==========================================================")
    print("DEMO DEL AGENTE DE RIESGO PAÍS")
    print("==========================================================")
    print(respuesta.informe)


# ==========================================================
# 7. PUNTO DE ENTRADA
# ==========================================================
if __name__ == "__main__":
    demo()