# thesis.py
import streamlit as st
import plotly.graph_objects as go
import base64
import textwrap
from pathlib import Path

# =========================
# STYLE (editável)
# =========================
# Este bloco reúne controles visuais (tamanhos, cores e espaçamentos)
# usados no app. A ideia é você ajustar aqui sem “caçar” valores no código.

# -------------------------------------------------
# 0) PLANTA (Plotly) — usado nas abas Tab3 e Tab4
# -------------------------------------------------
PLANT_HEIGHT = 520 # Altura total (px) do gráfico Plotly da planta (Floor Plan).
ZONE_TITLE_SIZE = 21 # Tamanho do texto "Zone A/B/C" acima da planta.
ZONE_VALUE_SIZE = 14 # Tamanho do texto percentual (ex.: "25.4%") abaixo da planta.
WINDOW_TEXT_SIZE = 17 # Tamanho do texto "Window" na lateral direita (fachada envidraçada).
WALL_LINE_WIDTH = 9 # Espessura (px) da borda externa da planta (contorno do ambiente).
ZONE_LINE_WIDTH = 1.2 # Espessura (px) das linhas das subzonas (retângulos internos).
WINDOW_LINE_WIDTH = 10 # Espessura (px) da linha da fachada/janela (lado direito).
WINDOW_COLOR = "#9a9a9a" # Cor da linha e do texto "Window" (cinza mais claro que dimgray).

# -------------------------------------------------
# 1) LEGENDA VERTICAL (Hot/Cold) — dentro da planta (Plotly)
# -------------------------------------------------
LEGEND_LABEL_SIZE = 10 # Tamanho dos números da legenda (0%, 20%, ... 100%).
LEGEND_TITLE_SIZE = 14 # Tamanho dos títulos "Cold" e "Hot" acima das barras.
LEGEND_GAP = 0.25 # Espaço horizontal entre as duas barras verticais (Cold e Hot).
LEGEND_BAR_W = 0.22 # Largura de cada barra vertical (Cold e Hot) em unidades do eixo Plotly.
LEGEND_RIGHT_X = -0.62 # Posição X do limite direito do conjunto de legendas.

# -------------------------------------------------
# 2) LEGENDA/LEGENDAS sob a planta — Tab3 e Tab4
# -------------------------------------------------
PLAN_CAPTION_TEXT = "Floor Plan – Office (4.00 x 7.50m)" # Texto da legenda central abaixo da planta.
PLAN_CAPTION_SIZE = 22 # Tamanho da fonte da legenda abaixo da planta.
PLAN_CAPTION_MARGIN_TOP = -20 # Ajuste fino de distância vertical entre a planta e a legenda.
PLAN_CAPTION_COLOR = "#333" # Cor do texto da legenda da planta.

# -------------------------------------------------
# 3) Subtítulos dos painéis de controle — Tab3 e Tab4 (coluna direita)
# -------------------------------------------------
SUBTITLE_SIZE = 14 # Tamanho do subtítulo (texto em cinza abaixo de cada heading).
SUBTITLE_COLOR = "#777777" # Cor do subtítulo.
SUBTITLE_MARGIN_BOTTOM = "0.2rem" # Espaço após o subtítulo (CSS). Ex.: "0.2rem", "6px", etc.

# =================================================
# TAB 3 — BASE CASE INFO (bloco abaixo da planta)
# =================================================
BC_BLOCK_MAX_WIDTH_PX = 1200 # Largura máxima do bloco Base Case (para alinhar com a largura da planta).
BC_TEXT_FONT_PX = 14 # Tamanho do texto das características do modelo.
BC_TITLE_COLOR = "#d33" # Cor do título "Base case model (BC): main characteristics" (vermelho).
BC_DIVIDER_MARGIN_PX = 6 # Margem vertical do <hr> (linha divisória) do bloco BC.
BC_IMG_WIDTH_PX = 600 # Largura (px) da imagem "shoeboxmodel.png".
BC_IMG_ALIGN = "left" # Alinhamento horizontal da imagem do shoebox dentro da coluna.
# Valores válidos: "left" | "center" | "right"

BC_IMG_CAPTION_SIZE = 13 # Tamanho da legenda abaixo da imagem (shoebox).
BC_IMG_CAPTION_COLOR = "#666" # Cor da legenda da imagem.
BC_IMG_MARGIN_TOP_PX = 4 # Espaço acima da imagem (para alinhar verticalmente com o texto).

BC_IMG_JUSTIFY = "center"      # "flex-start" | "center" | "flex-end"
BC_IMG_OFFSET_X_PX = -120      # empurra a imagem (negativo = vai para esquerda)
BC_IMG_MAX_COL_W_PX = 520      # largura do "palco" na coluna da imagem (opcional)

# -------------------------------------------------
# 4) Caminhos (imagens)
# -------------------------------------------------
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent          # .../app
ROOT_DIR = APP_DIR.parent                          # .../thesis_sim
ASSETS_DIR = ROOT_DIR / "assets" / "img"
# Pasta onde ficam as imagens usadas nas abas (iso, plan, histogramas, shoebox etc.)

# =================================================
# TAB 2 — THERMAL ZONING (imagens + textos)
# =================================================
TZ_DROPDOWN_WIDTH_PX = 240
# Largura do dropdown de seleção do Zone Model (evita esticar na tela inteira).

TZ_LEFT_COL_RATIO = 1.55
TZ_RIGHT_COL_RATIO = 2.45
# Proporção das colunas principais:
# esquerda = (iso + planta), direita = (gráficos To + PMV)

TZ_RIGHT_PLOTS_GAP = "large"
# Espaço entre os dois gráficos (To e PMV) no lado direito.
# Valores típicos: "small" | "medium" | "large"

TZ_ISO_WIDTH_PX = 360
# Largura da imagem isométrica (st.image).

TZ_PLAN_WIDTH_PX = 140
# Largura da planta (renderizada no "stage" com translate).
# OBS: você tem TZ_PLAN_WIDTH_PX definido duas vezes no seu bloco anterior;
# aqui deixei só UMA definição para evitar confusão.

TZ_PLOT_TO_WIDTH_PX = 400
TZ_PLOT_PMV_WIDTH_PX = 400 # Largura dos histogramas/barras (To e PMV). Aumente para ficarem mais legíveis.

TZ_TOP_SPACER_PX = 6 # Espaço vertical entre o dropdown e o início das imagens.
TZ_ISO_PLAN_GAP_PX = 10 # Espaço vertical entre isométrica e planta (coluna esquerda).
TZ_LEGEND_FONT_PX = 14 # Fonte da legenda longa abaixo dos histogramas (sem wrap).
TZ_THRESH_FONT_PX = 13 # Fonte das linhas de threshold (To<23 / To>23 etc.) abaixo da legenda.
TZ_TEXT_FONT_PX = 14 # Fonte dos textos dos blocos inferiores (características, zone model, outcomes).

# -------------------------------------------------
# TAB 2 — “Stage” da planta (para mover com offset)
# -------------------------------------------------
TZ_PLAN_STAGE_H_PX = 260
# Altura base do palco onde a planta é desenhada.
# Se muito alta, cria “vazio” antes dos textos abaixo.

TZ_PLAN_STAGE_MIN_H_PX = 90
# Altura mínima do palco, para não esmagar quando offset_y for muito negativo.

TZ_PLAN_CLIP = False
# Se True: corta (clip) a imagem ao sair do palco (overflow hidden).
# Se False: deixa “vazar” (overflow visible).

TZ_PLAN_ZINDEX = 3
# Empilhamento (z-index) da planta dentro do palco.
# Útil se um dia tiver elementos sobrepostos.

TZ_PLAN_PAD_PX = 6
# Padding interno do palco (margem interna).

TZ_PLAN_OFFSET_X_PX = 350
TZ_PLAN_OFFSET_Y_PX = -80
# Deslocamento fino da planta dentro do palco (translate X/Y).
# X positivo empurra para a direita; Y negativo sobe.

TZ_LEFT_MAX_WIDTH_PX = 520
# Largura máxima do container da coluna esquerda (referência para não “invadir” os gráficos).

TZ_SECTION_TITLE_COLOR = "#d33"
# Cor dos títulos dos blocos inferiores da Tab2:
# "Model main characteristics" | "Zone Model X" | "Outcomes"

TZ_DIVIDER_MARGIN_PX = 6
# Margem vertical do <hr> nos blocos inferiores da Tab2.

# =================================================
# TAB 4 — FACADE SELECTOR STYLE (editável)
# =================================================
FACADE_IMG_SCALE = 0.25 # Escala das imagens das alternativas de fachada (multiplica BASE_IMG_W).
FACADE_TITLE_SIZE = 16 # Fonte do título (label) de cada alternativa.
FACADE_META_SIZE = 12 # Fonte dos metadados (SHGC, WWR, Type, Shading) de cada alternativa.
FACADE_DOT_SIZE = 18 # Tamanho “alvo” do quadradinho seletor (os dots desenhados via CSS).
FACADE_TABLE_LABEL_SIZE = 12 # Fonte da coluna esquerda dos rótulos (SHGC, WWR, Type, Shading).

# =========================
# 1) DATA (editável)
# =========================

# Conforto — controle por Ta (19–24)
COMFORT_TA = {
    "A": {
        24: {"To_gt_26": 97.0, "To_lt_23": 0.0, "PMV_gt_p05": 92.6, "PMV_lt_m05": 0.0},
        23: {"To_gt_26": 71.3, "To_lt_23": 0.0, "PMV_gt_p05": 53.9, "PMV_lt_m05": 0.0},
        22: {"To_gt_26": 27.5, "To_lt_23": 0.0, "PMV_gt_p05": 20.1, "PMV_lt_m05": 0.0},
        21: {"To_gt_26": 14.0, "To_lt_23": 0.0, "PMV_gt_p05": 8.0,  "PMV_lt_m05": 0.0},
        20: {"To_gt_26": 5.4,  "To_lt_23": 8.0, "PMV_gt_p05": 3.4,  "PMV_lt_m05": 6.0},
        19: {"To_gt_26": 2.1,  "To_lt_23": 38.0, "PMV_gt_p05": 2.0,  "PMV_lt_m05": 35.0},
    },
    "B": {
        24: {"To_gt_26": 95.0, "To_lt_23": 0.0, "PMV_gt_p05": 85.9, "PMV_lt_m05": 0.0},
        23: {"To_gt_26": 16.0, "To_lt_23": 0.0, "PMV_gt_p05": 8.5,  "PMV_lt_m05": 0.0},
        22: {"To_gt_26": 2.2,  "To_lt_23": 0.0, "PMV_gt_p05": 2.1,  "PMV_lt_m05": 0.0},
        21: {"To_gt_26": 1.1,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        20: {"To_gt_26": 0.5,  "To_lt_23": 49.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 41.0},
        19: {"To_gt_26": 0.1,  "To_lt_23": 92.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 91.0},
    },
    "C": {
        24: {"To_gt_26": 58.6, "To_lt_23": 0.0, "PMV_gt_p05": 32.0, "PMV_lt_m05": 0.0},
        23: {"To_gt_26": 2.5,  "To_lt_23": 0.0, "PMV_gt_p05": 2.2,  "PMV_lt_m05": 0.0},
        22: {"To_gt_26": 0.6,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        21: {"To_gt_26": 0.2,  "To_lt_23": 0.0, "PMV_gt_p05": 0.7,  "PMV_lt_m05": 0.0},
        20: {"To_gt_26": 0.0,  "To_lt_23": 88.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 85.0},
        19: {"To_gt_26": 0.0,  "To_lt_23": 98.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 97.0},
    }
}

# Conforto — controle por To (22–27)
COMFORT_TO = {
    "A": {
        27: {"To_gt_26": 100.0, "To_lt_23": 0.0, "PMV_gt_p05": 96.9, "PMV_lt_m05": 0.0},
        26: {"To_gt_26": 2.6,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        25: {"To_gt_26": 0.3,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        24: {"To_gt_26": 0.1,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 2.0},
        23: {"To_gt_26": 0.1,  "To_lt_23": 25.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 49.0},
        22: {"To_gt_26": 0.0,  "To_lt_23": 99.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 98.0},
    },
    "B": {
        27: {"To_gt_26": 100.0, "To_lt_23": 0.0, "PMV_gt_p05": 98.6, "PMV_lt_m05": 0.0},
        26: {"To_gt_26": 2.5,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.9},
        25: {"To_gt_26": 0.0,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        24: {"To_gt_26": 0.0,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 1.0},
        23: {"To_gt_26": 0.0,  "To_lt_23": 2.0,  "PMV_gt_p05": 1.7,  "PMV_lt_m05": 3.0},
        22: {"To_gt_26": 0.0,  "To_lt_23": 100.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 98.0},
    },
    "C": {
        27: {"To_gt_26": 100.0, "To_lt_23": 0.0, "PMV_gt_p05": 99.9, "PMV_lt_m05": 0.0},
        26: {"To_gt_26": 1.6,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.9},
        25: {"To_gt_26": 0.0,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        24: {"To_gt_26": 0.0,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        23: {"To_gt_26": 0.0,  "To_lt_23": 2.0,  "PMV_gt_p05": 1.7,  "PMV_lt_m05": 2.0},
        22: {"To_gt_26": 0.0,  "To_lt_23": 100.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 98.0},
    }
}

ENERGY_TA = {19: 321, 20: 306, 21: 291, 22: 276, 23: 262, 24: 249}
ENERGY_TO = {22: 341, 23: 322, 24: 300, 25: 280, 26: 262, 27: 245}

# =========================
# TAB 4 — FACADE DESIGN DATA (editável)
# =========================

FACADE_ALTS = [
    {
        "id": "ALT1",
        "label": "SHGC .16\nNo Shading",
        "img": str(ASSETS_DIR / "001_shgc16noshading.jpg"),
        "meta": {"SHGC": ".16", "WWR": "100%", "Type": "Double Low-E", "Shading": "No"},
    },
    {
        "id": "ALT2",
        "label": "SHGC .29\nNo Shading (BC)",
        "img": str(ASSETS_DIR / "002_shgc29noshading.jpg"),
        "meta": {"SHGC": ".29", "WWR": "100%", "Type": "Laminated", "Shading": "No"},
    },
    {
        "id": "ALT3",
        "label": "SHGC .41\nNo Shading",
        "img": str(ASSETS_DIR / "003_shgc41noshading.jpg"),
        "meta": {"SHGC": ".41", "WWR": "100%", "Type": "Laminated", "Shading": "No"},
    },
    {
        "id": "ALT4",
        "label": "SHGC .29\nNo Shading\n*WWR 50%",
        "img": str(ASSETS_DIR / "004_shgc29noshadingwwr50.jpg"),
        "meta": {"SHGC": ".29", "WWR": "50%", "Type": "Laminated", "Shading": "No"},
    },
    {
        "id": "ALT5",
        "label": "SHGC .29\nShaded",
        "img": str(ASSETS_DIR / "005_shgc29shaded.jpg"),
        "meta": {"SHGC": ".29", "WWR": "100%", "Type": "Laminated", "Shading": "100%"},
    },
]

# --- Comfort (Ta thermostat), extracted from your charts (21°C and 23°C)
# keys inside each zone:
#   To_gt_26, To_lt_23, PMV_gt_p05, PMV_lt_m05

COMFORT_FACADE_TA = {
    21: {
        # Zone A
        "A": {
            "ALT1": {"To_gt_26": 2.3,  "To_lt_23": 0.0, "PMV_gt_p05": 2.1,  "PMV_lt_m05": 0.0},
            "ALT2": {"To_gt_26": 14.0, "To_lt_23": 0.0, "PMV_gt_p05": 8.0,  "PMV_lt_m05": 0.0},
            "ALT3": {"To_gt_26": 25.4, "To_lt_23": 0.0, "PMV_gt_p05": 18.1, "PMV_lt_m05": 0.0},
            "ALT4": {"To_gt_26": 1.1,  "To_lt_23": 0.0, "PMV_gt_p05": 1.8,  "PMV_lt_m05": 0.0},
            "ALT5": {"To_gt_26": 0.6,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        },
        # Zone B
        "B": {
            "ALT1": {"To_gt_26": 0.4, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT2": {"To_gt_26": 1.1, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT3": {"To_gt_26": 2.5, "To_lt_23": 0.0, "PMV_gt_p05": 2.3, "PMV_lt_m05": 0.0},
            "ALT4": {"To_gt_26": 0.1, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT5": {"To_gt_26": 0.1, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
        },
        # Zone C (note: some To<23 exists at 21°C in your chart)
        "C": {
            "ALT1": {"To_gt_26": 0.0, "To_lt_23": 1.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT2": {"To_gt_26": 0.2, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT3": {"To_gt_26": 0.7, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT4": {"To_gt_26": 0.0, "To_lt_23": 7.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT5": {"To_gt_26": 0.0, "To_lt_23": 3.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
        },
    },

    23: {
        "A": {
            "ALT1": {"To_gt_26": 33.5, "To_lt_23": 0.0, "PMV_gt_p05": 22.0, "PMV_lt_m05": 0.0},
            "ALT2": {"To_gt_26": 71.3, "To_lt_23": 0.0, "PMV_gt_p05": 53.9, "PMV_lt_m05": 0.0},
            "ALT3": {"To_gt_26": 84.0, "To_lt_23": 0.0, "PMV_gt_p05": 76.6, "PMV_lt_m05": 0.0},
            "ALT4": {"To_gt_26": 22.5, "To_lt_23": 0.0, "PMV_gt_p05": 14.0, "PMV_lt_m05": 0.0},
            "ALT5": {"To_gt_26": 24.5, "To_lt_23": 0.0, "PMV_gt_p05": 4.6,  "PMV_lt_m05": 0.0},
        },
        "B": {
            "ALT1": {"To_gt_26": 5.8,  "To_lt_23": 0.0, "PMV_gt_p05": 3.2,  "PMV_lt_m05": 0.0},
            "ALT2": {"To_gt_26": 16.0, "To_lt_23": 0.0, "PMV_gt_p05": 8.5,  "PMV_lt_m05": 0.0},
            "ALT3": {"To_gt_26": 46.4, "To_lt_23": 0.0, "PMV_gt_p05": 30.2, "PMV_lt_m05": 0.0},
            "ALT4": {"To_gt_26": 2.1,  "To_lt_23": 0.0, "PMV_gt_p05": 1.9,  "PMV_lt_m05": 0.0},
            "ALT5": {"To_gt_26": 1.5,  "To_lt_23": 0.0, "PMV_gt_p05": 1.7,  "PMV_lt_m05": 0.0},
        },
        "C": {
            "ALT1": {"To_gt_26": 1.6, "To_lt_23": 0.0, "PMV_gt_p05": 1.9, "PMV_lt_m05": 0.0},
            "ALT2": {"To_gt_26": 2.5, "To_lt_23": 0.0, "PMV_gt_p05": 2.2, "PMV_lt_m05": 0.0},
            "ALT3": {"To_gt_26": 8.3, "To_lt_23": 0.0, "PMV_gt_p05": 4.9, "PMV_lt_m05": 0.0},
            "ALT4": {"To_gt_26": 0.7, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
            "ALT5": {"To_gt_26": 0.6, "To_lt_23": 0.0, "PMV_gt_p05": 1.7, "PMV_lt_m05": 0.0},
        },
    },
}

# --- Energy (kWh/m²·year) extracted from your two energy charts
ENERGY_FACADE_TA = {
    21: {"ALT1": 266, "ALT2": 291, "ALT3": 317, "ALT4": 259, "ALT5": 260},
    # 23°C not provided in the images you sent (leave as placeholders; fill later)
    23: {"ALT1": None, "ALT2": None, "ALT3": None, "ALT4": None, "ALT5": None},
}

ENERGY_FACADE_TO26 = {"ALT1": 238, "ALT2": 262, "ALT3": 295, "ALT4": 228, "ALT5": 224}

# =========================
# 2) HELPERS
# =========================

def discomfort_value(metrics: dict, mode: str) -> float:
    """mode: 'To' or 'PMV'"""
    if mode == "To":
        return max(metrics["To_gt_26"], metrics["To_lt_23"])
    return max(metrics["PMV_gt_p05"], metrics["PMV_lt_m05"])


def hot_color(p: float) -> str:
    """
    Hot scale: white -> dark red
    White for <10%
    """
    if p < 10:
        return "#ffffff"
    palette = [
        "#fee5d9",
        "#fcbba1",
        "#fc9272",
        "#fb6a4a",
        "#ef3b2c",
        "#cb181d",
        "#a50f15",
        "#7f0000",
        "#5a0000",
        "#3b0000",
    ]
    p = max(0.0, min(100.0, p))
    idx = int(p // 10)
    if idx >= 10:
        idx = 9
    return palette[idx]


def cold_color(p: float) -> str:
    """
    Cold scale: white -> dark blue
    White for <10%
    """
    if p < 10:
        return "#ffffff"
    palette = [
        "#deebf7",
        "#c6dbef",
        "#9ecae1",
        "#6baed6",
        "#4292c6",
        "#2171b5",
        "#08519c",
        "#08306b",
        "#062450",
        "#041633",
    ]
    p = max(0.0, min(100.0, p))
    idx = int(p // 10)
    if idx >= 10:
        idx = 9
    return palette[idx]

def make_plan_figure(zone_hot: dict, zone_cold: dict) -> go.Figure:
    """
    Dominant rule:
    - if hot <10 and cold <10 -> white + show 0-10 bin (as 0.x etc)
    - if hot >= cold -> use HOT palette, show hot value
    - else -> use COLD palette, show cold value
    """
    W, H = 7.5, 4.0
    zW = 2.5
    fig = go.Figure()

    zones = [
        ("C", 0.0, zW),
        ("B", zW, 2*zW),
        ("A", 2*zW, 3*zW),
    ]

    def dominant_fill(zname: str) -> str:
        h = zone_hot[zname]
        c = zone_cold[zname]
        if h < 10 and c < 10:
            return "#ffffff"
        return hot_color(h) if h >= c else cold_color(c)

    def dominant_value(zname: str) -> float:
        h = zone_hot[zname]
        c = zone_cold[zname]
        # dominante (sem H/C no texto, como você pediu)
        return h if h >= c else c

    # --- zones
    for name, x0, x1 in zones:
        fig.add_shape(
            type="rect",
            x0=x0, y0=0, x1=x1, y1=H,
            line=dict(color="black", width=ZONE_LINE_WIDTH),
            fillcolor=dominant_fill(name),
            layer="below"
        )

        # Zone label ABOVE the plan (always legible)
        fig.add_annotation(
            x=(x0 + x1) / 2, y=H + 0.22,
            text=f"Zone {name}",
            showarrow=False,
            font=dict(size=ZONE_TITLE_SIZE, color="black")
        )

        # Dominant value BELOW the plan
        fig.add_annotation(
            x=(x0 + x1) / 2, y=-0.22,
            text=f"{dominant_value(name):.1f}%",
            showarrow=False,
            font=dict(size=ZONE_VALUE_SIZE, color="black")
        )

    # separators
    fig.add_shape(type="line", x0=zW, y0=0, x1=zW, y1=H, line=dict(color="gray", width=1, dash="dash"))
    fig.add_shape(type="line", x0=2*zW, y0=0, x1=2*zW, y1=H, line=dict(color="gray", width=1, dash="dash"))

    # thick border (editable)
    fig.add_shape(
        type="rect", x0=0, y0=0, x1=W, y1=H,
        line=dict(color="black", width=WALL_LINE_WIDTH),
        fillcolor="rgba(0,0,0,0)"
    )

    # window facade (right) — lighter gray (editable)
    fig.add_shape(
        type="line", x0=W, y0=0, x1=W, y1=H,
        line=dict(color=WINDOW_COLOR, width=WINDOW_LINE_WIDTH)
    )
    fig.add_annotation(
        x=W + 0.28, y=H / 2,
        text="Window",
        textangle=-90,
        showarrow=False,
        font=dict(size=WINDOW_TEXT_SIZE, color=WINDOW_COLOR)
    )

    # --- Two vertical legends on LEFT (parametrized)
    hot_x1 = LEGEND_RIGHT_X
    hot_x0 = hot_x1 - LEGEND_BAR_W

    cold_x1 = hot_x0 - LEGEND_GAP
    cold_x0 = cold_x1 - LEGEND_BAR_W


    bins = list(range(0, 100, 10))  # 0..90
    for i, b in enumerate(bins):
        y0 = (H * i) / 10.0
        y1 = (H * (i + 1)) / 10.0
        mid = b + 5

        fig.add_shape(
            type="rect",
            x0=cold_x0, y0=y0, x1=cold_x1, y1=y1,
            line=dict(color="black", width=0.5),
            fillcolor=cold_color(mid),
            layer="below"
        )
        fig.add_shape(
            type="rect",
            x0=hot_x0, y0=y0, x1=hot_x1, y1=y1,
            line=dict(color="black", width=0.5),
            fillcolor=hot_color(mid),
            layer="below"
        )

        if b % 20 == 0:
            fig.add_annotation(
                x=cold_x0 - 0.08, y=y0,
                text=f"{b}%",
                showarrow=False,
                xanchor="right",
                font=dict(size=LEGEND_LABEL_SIZE, color="black")
            )

    fig.add_annotation(
        x=cold_x0 - 0.08, y=H,
        text="100%",
        showarrow=False,
        xanchor="right",
        font=dict(size=LEGEND_LABEL_SIZE)
    )

    fig.add_annotation(x=(cold_x0+cold_x1)/2, y=H+0.15, text="Cold", showarrow=False, font=dict(size=LEGEND_TITLE_SIZE))
    fig.add_annotation(x=(hot_x0+hot_x1)/2, y=H+0.15, text="Hot",  showarrow=False, font=dict(size=LEGEND_TITLE_SIZE))

    # Required textual legend under the bars (two lines)
    fig.add_annotation(
        x=(cold_x0 + hot_x1)/2, y=-0.50,
        text="Cold: To < 23°C / PMV < −0.5",
        showarrow=False,
        font=dict(size=10, color="black"),
        xanchor="center"
    )
    fig.add_annotation(
        x=(cold_x0 + hot_x1)/2, y=-0.72,
        text="Hot: To > 26°C / PMV > +0.5",
        showarrow=False,
        font=dict(size=10, color="black"),
        xanchor="center"
    )

    # North arrow moved to TOP-RIGHT (as you requested)
    fig.add_annotation(x=W+0.55, y=H-0.08, text="↑", showarrow=False, font=dict(size=26, color="black"))
    fig.add_annotation(x=W+0.55, y=H-0.35, text="N", showarrow=False, font=dict(size=12, color="black"))

    # enlarge ranges to fit labels above/below
    fig.update_xaxes(visible=False, range=[-1.35, W + 0.95])
    fig.update_yaxes(visible=False, range=[-0.95, H + 0.45], scaleanchor="x", scaleratio=1)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=PLANT_HEIGHT,
    )
    return fig

def make_energy_chart(active_kind: str, active_sp: int, ref_sp: int | None) -> tuple[go.Figure, float | None]:
    fig = go.Figure()

    # 1) Eixo X comum (19..27) como categorias (centraliza os ticks)
    x_all = list(range(19, 28))
    x_labels = [str(i) for i in x_all]

    # 2) Séries alinhadas no mesmo eixo (None onde não existe dado)
    ta_y = [ENERGY_TA.get(x, None) for x in x_all]  # Ta só tem 19..24
    to_y = [ENERGY_TO.get(x, None) for x in x_all]  # To só tem 22..27

    # 3) Cores (destaca o setpoint ativo em vermelho, e "some" onde não há dado)
    ta_base = "#1f77b4"   # azul escuro
    to_base = "#9ecae1"   # azul claro
    active_red = "#de2d26"

    ta_colors = []
    for x in x_all:
        if x not in ENERGY_TA:
            ta_colors.append("rgba(0,0,0,0)")  # sem barra
        elif active_kind == "Ta" and x == active_sp:
            ta_colors.append(active_red)
        else:
            ta_colors.append(ta_base)

    to_colors = []
    for x in x_all:
        if x not in ENERGY_TO:
            to_colors.append("rgba(0,0,0,0)")  # sem barra
        elif active_kind == "To" and x == active_sp:
            to_colors.append(active_red)
        else:
            to_colors.append(to_base)

    # garante que o quadradinho da legenda não “herde” transparente
    to_colors[0] = to_base
    ta_colors[0] = ta_base  # opcional (segurança)

    # 4) Barras (mesmo X para as duas séries)
    fig.add_bar(
        x=x_labels,
        y=ta_y,
        name="Ta",
        marker=dict(color=ta_colors, line=dict(width=0)),
    )

    fig.add_bar(
        x=x_labels,
        y=to_y,
        name="To",
        marker=dict(color=to_colors, line=dict(width=0)),
    )

    # 5) Delta vs referência (como antes)
    delta = None
    if ref_sp is not None:
        if active_kind == "Ta" and (active_sp in ENERGY_TA and ref_sp in ENERGY_TA):
            Ea, Er = ENERGY_TA[active_sp], ENERGY_TA[ref_sp]
            delta = (Ea - Er) / Er * 100.0
        elif active_kind == "To" and (active_sp in ENERGY_TO and ref_sp in ENERGY_TO):
            Ea, Er = ENERGY_TO[active_sp], ENERGY_TO[ref_sp]
            delta = (Ea - Er) / Er * 100.0

    # 6) Layout (x categórico -> ticks alinhados com as barras)
    fig.update_layout(
        barmode="group",
        height=230,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="kWh/m²·year",
        xaxis=dict(
            title="Temperature (°C)",
            type="category",
            categoryorder="array",
            categoryarray=x_labels,  # garante ordem 19..27
        ),
        legend=dict(
            orientation="h",
            x=0.5, xanchor="center",
            y=1.05, yanchor="bottom"
        ),
    )

    return fig, delta


def make_energy_chart_facade(control_kind: str, ta_setpoint: int, active_alt_id: str) -> go.Figure:
    """
    control_kind:
      - "Ta" -> uses ENERGY_FACADE_TA[ta_setpoint]
      - "To" -> uses ENERGY_FACADE_TO26 (fixed)
    """
    fig = go.Figure()

    alt_ids = [a["id"] for a in FACADE_ALTS]
    x_labels = [a["label"].replace("\n", "<br>") for a in FACADE_ALTS]  # multiline x tick

    # series values
    if control_kind == "Ta":
        y = [ENERGY_FACADE_TA[ta_setpoint].get(i, None) for i in alt_ids]
        name = f"Ta ({ta_setpoint}°C)"
    else:
        y = [ENERGY_FACADE_TO26.get(i, None) for i in alt_ids]
        name = "To (26°C)"

    base_gray = "#c7c7c7"
    active_red = "#de2d26"

    colors = []
    for alt_id, v in zip(alt_ids, y):
        if v is None:
            colors.append("rgba(0,0,0,0)")
        elif alt_id == active_alt_id:
            colors.append(active_red)
        else:
            colors.append(base_gray)

    fig.add_bar(
        x=x_labels,
        y=y,
        name=name,
        marker=dict(color=colors, line=dict(width=0)),
    )

    fig.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="kWh/m²·year",
        xaxis_title="Facade Designs",
        xaxis=dict(type="category"),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.05, yanchor="bottom"),
    )

    return fig

def make_plan_placeholder(message: str) -> go.Figure:
    """
    Placeholder plotly figure to replace the plan when no results exist
    (e.g., Operative-temperature thermostat mode in Tab 4).
    """
    W, H = 7.5, 4.0
    fig = go.Figure()

    # Base white rectangle (plan area)
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=W, y1=H,
        line=dict(color="black", width=WALL_LINE_WIDTH),
        fillcolor="#ffffff",
        layer="below"
    )

    # Translucent overlay mask (to "hide" the plan)
    fig.add_shape(
        type="rect",
        x0=-1.35, y0=-0.95, x1=W + 0.95, y1=H + 0.45,
        line=dict(color="rgba(0,0,0,0)", width=0),
        fillcolor="rgba(255,255,255,0.75)",
        layer="above"
    )

    # Center message
    fig.add_annotation(
        x=W/2, y=H/2,
        text=message,
        showarrow=False,
        font=dict(size=18, color="#444"),
        xanchor="center",
        yanchor="middle"
    )

    # Keep same viewbox as your normal plan
    fig.update_xaxes(visible=False, range=[-1.35, W + 0.95])
    fig.update_yaxes(visible=False, range=[-0.95, H + 0.45], scaleanchor="x", scaleratio=1)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=PLANT_HEIGHT,
    )
    return fig

# =========================
# 3) UI
# =========================

st.set_page_config(page_title="THESIS_SIM", layout="wide")

# =========================
# CSS (GLOBAL - não vaza)
# =========================
# --- derive sizes (TAB4)
BASE_DOT_PX = 16  # tamanho “base” típico do radio do Streamlit/BaseWeb
dot_scale = FACADE_DOT_SIZE / BASE_DOT_PX

st.markdown(f"""
<style>
/* ===== Global compact layout ===== */
.block-container {{ padding-top: 2.0rem; padding-bottom: 0.6rem; }}
div[data-testid="stVerticalBlock"] > div {{ gap: 0.6rem; }}
h2 {{ margin-top: 0.2rem; margin-bottom: 0.2rem; }}
h3 {{ margin-top: 0.2rem; margin-bottom: 0.2rem; font-size: 1.05rem; }}
div[role="radiogroup"] label {{ font-size: 0.95rem; }}
div[data-testid="stSlider"] label {{ font-size: 0.95rem; }}
/* =========================================================
   TAB4 — DOTS por KEY (st-key-dot_ALT1..ALT5)
   - remove o retângulo padrão do Streamlit
   - desenha um quadradinho 5x5
   - hover vermelho
   - ativo (kind="primary") vermelho
   ========================================================= */

/* 0) Centraliza o botão dentro da coluna */
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"]{{
  display:flex !important;
  justify-content:center !important;
  align-items:center !important;
}}

/* 1) Mata COMPLETAMENTE o estilo do retângulo do Streamlit */
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"] > button{{
  all: unset !important;
  box-sizing: border-box !important;
  cursor: pointer !important;

  /* mantém uma “linha” clicável, mas sem retângulo visível */
  width: 100% !important;
  height: 18px !important;

  display:flex !important;
  justify-content:center !important;
  align-items:center !important;

  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  outline: none !important;
}}

/* 2) Remove qualquer conteúdo interno (se aparecer algo) */
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"] > button *{{
  display:none !important;
}}

/* 3) Desenha o quadradinho*/
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"] > button::before{{
  content:"";
  width: 15px !important;
  height: 15px !important;
  border-radius: 1px !important;
  border: 1px solid rgba(0,0,0,0.35) !important;
  background: transparent !important;
  display:block !important;
}}

/* 4) Hover vermelho */
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"] > button:hover::before{{
  background:#ccc !important;
  border-color:#666 !important;
}}

/* 5) Ativo = kind="primary" => vermelho sólido */
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"] > button[kind="primary"]::before{{
  background:#d33 !important;
  border-color:#d33 !important;
}}

/* 6) Mata focus ring */
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"] > button:focus,
div[data-testid="stElementContainer"][class*="st-key-dot_"] div[data-testid="stButton"] > button:focus-visible{{
  outline:none !important;
  box-shadow:none !important;
}}


            
/* TAB4 meta: evita margens internas do markdown “empurrarem” linhas */
.tab4-meta-left p, .tab4-meta-mid p {{ 
  margin: 0 !important;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("## THERMAL CAUSES AND ENERGY IMPACTS OF OCCUPANTS ADAPTIVE RESPONSES IN GLASS CURTAIN-WALL OFFICE BUILDINGS IN THE TROPICS")
st.markdown("**Dr. Arq. Alexandre Oliveira**")


tabs = st.tabs(["Summary", "Thermal Zoning", "Thermal Environment Control", "Facade Design Alternatives", "Conclusions & Contribution"])

with tabs[0]:
    # =========================================================
    # TAB 1 — SUMMARY (sem repetir o rótulo da aba)
    # =========================================================

    SUMMARY_TEXT = """
### Introduction
Highly glazed façades have remained a strong architectural trend since the 1960s, driven by modernist aesthetics, technical ambitions, and market preferences [1,2]. Although glazing technologies have advanced to mitigate thermal discomfort and cooling energy demand [3], many developing countries still rely heavily on older laminated glass systems [4]. In Brazil, laminated glazing is frequently specified for fully glazed curtain-wall office buildings in low-latitude warm climates—even in projects labelled as “green” by rating systems such as LEED [5,6]. Classic critiques of early curtain-wall buildings already anticipated major thermal gradients and elevated cooling costs [7–10]. In warm climates, façade-driven solar gains can generate non-uniform indoor environments where operative temperature (To) and PMV vary significantly across occupant positions [15–17]. However, this spatial variability is often masked in whole-building simulation workflows because rooms are commonly represented as a single thermal node controlled by an average air temperature (Ta) [18–20]. As a result, occupants frequently adapt by changing blinds and layouts and, notably, by adjusting thermostat setpoints, indirectly increasing energy use and reinforcing the overcooling pattern observed in tropical buildings [22–27]. This study investigates thermal comfort behaviour and energy performance in highly glazed tropical office workspaces as designed, without occupants’ interference.

### Building energy efficiency and thermal comfort
Buildings account for a substantial share of global final energy use and CO₂ emissions, with space cooling being one of the fastest-growing end uses in commercial buildings [29–31]. In Brazil, buildings represent over half of national electricity consumption, and cooling often constitutes a large fraction of end use in commercial and public buildings [32]. Evidence from audits and monitoring suggests that cooling demand in office buildings is highly sensitive to envelope design and climate, particularly for unshaded glazing in warm regions [33]. The thermal performance of façades depends on orientation, window-to-wall ratio (WWR), glazing properties, shading, and thermal resistance [34–36]. In hot and humid climates, cooling energy and indoor comfort are especially sensitive to SHGC and window size, followed by shading and orientation [37]. Experimental and simulation studies reinforce that higher SHGC and large glazed areas intensify mean radiant temperature (Tr) and thermal discomfort near façades, while high-performance glazing and effective shading can yield significant cooling-energy savings [38,39,40–46]. Yet designers must balance solar control with daylighting and visual access, because many market solutions that reduce SHGC may also reduce visible transmittance and affect indoor environmental quality [47].

Cooling energy consumption also depends strongly on thermostat control type and setpoint strategy [48–54]. Setpoint adjustment is often considered a low-cost measure, and increasing setpoints can reduce cooling energy use substantially [55–57]. Conversely, lowering Ta to compensate for higher Tr increases energy consumption and can lead to overcooling [28,58–60]. Conventional HVAC control based on zone-average Ta is poorly suited to spaces with strong radiant asymmetry and perimeter-to-core Tr differences [61,62]. While operative-temperature-based control can improve comfort relevance, it may increase energy use in some contexts and remains uncommon in market-ready systems [28,63,65]. Research indicates that distributed or multi-point control strategies—such as multiple Ta thermostats near occupants—can improve comfort and reduce energy demand compared to a single thermostat controlling the whole space [66,67].

### Thermal comfort assessment of non-uniform thermal environments
Thermal comfort assessment is commonly based on standards such as ASHRAE 55, ISO 7730, and EN 15251 [68–70], with PMV/PPD remaining widely used for air-conditioned environments [71,72]. ISO 7730 proposes comfort categories (A, B, C), where Category B (PMV ±0.5) is often treated as realistic for design, and operative temperature ranges are used as practical thresholds for discomfort screening in cooling conditions [69,73]. Nevertheless, PMV has known limitations for short-wave solar effects and transient or spatially non-uniform environments [25,75–78]. Several improvements have been proposed—particularly involving solar-adjusted mean radiant temperature and radiant asymmetry—but no single approach has been universally adopted in standards and tools [79–85]. Tr remains difficult to measure and model accurately, and uncertainty grows precisely in situations where Ta and Tr diverge spatially—conditions that strongly affect PMV estimation [86–89].

Building simulation tools typically simplify thermal comfort analysis by evaluating variables at the geometric centre of the zone under steady, uniform assumptions [19]. Only some tools can estimate Tr and To at specific points, often requiring additional modelling steps or coupling with CFD [90]. Among the most capable and widely used engines, EnergyPlus stands out as an open-source, validated platform in which surface temperatures and long-wave exchanges are central to indoor heat balance [101,102]. When used via GUIs such as DesignBuilder or OpenStudio/SketchUp workflows, designers can subdivide a space into subzones using partitions and evaluate comfort at each subzone’s representative point, enabling a practical approach to investigate non-uniform environments [103–106].

### Research method
This research method evaluates, through building simulations, three interconnected effects of highly glazed curtain-wall façades in the tropics: (1) non-uniform thermal environments; (2) the impact of thermal environment control on thermal comfort and cooling energy consumption; and (3) façade design alternatives and their effect on energy use when comfort is ensured. A simplified “shoe-box” office workspace model was built in EnergyPlus to focus on façade-driven performance rather than complex building geometry [107]. Simulations were conducted for an annual period at 10-minute intervals, analysing only occupied hours.

A common base case (BC) represents a typical Brazilian office workspace in geometry, construction, and occupancy assumptions, with adiabatic lateral and rear walls, floor, and ceiling. The façade is East-oriented with 100% WWR and no internal or external shading. The BC glazing adopts an “optimistic” laminated-glass SHGC consistent with current market availability in Brazil [108,109]. The 23°C Ta cooling setpoint was used as a reference because it is common in Brazilian HVAC practice and aligns with typical summer comfort recommendations used in design [110]. Weather conditions were defined for Fortaleza (ASHRAE climate 0A) [111,112], where high solar incidence on vertical surfaces makes façade orientation and solar control particularly relevant.

#### Non-uniform thermal environment
To represent spatial thermal variability within a single open-plan office, the room was subdivided into connected subzones using virtual partitions with openings that allow air exchange and long-wave radiative interaction, while short-wave effects are treated within the EnergyPlus radiative framework [91,106]. Four zoning configurations were tested (Zone Models 1, 2, 3, and 9), ranging from a single zone baseline to multi-subzone layouts to evaluate façade proximity effects and potential lateral wall influences. Subzones were compared using frequency distributions of To and PMV above discomfort thresholds consistent with Category B criteria for warm discomfort screening [69,74]. For the nine-zone layout, paired subzones were additionally compared using effect size (Cohen’s d) and overlap coefficient (OVL) metrics to quantify distribution similarity and evaluate whether additional subdivision adds analytical value [113,114].

#### Thermal environment control
Based on the thermal zoning findings, the thermal control assessment focuses on the three-subzone configuration (Zone Model 3). The analysis varies air-temperature-based thermostat setpoints (Ta-sp) and operative-temperature-based thermostat setpoints (To-sp) across appropriate ranges to evaluate how control logic and setpoint selection influence (i) the frequency of warm discomfort and (ii) annual cooling energy consumption.

#### Facade design alternatives
Five highly glazed façade design alternatives, including the BC, were compared to examine energy consumption under thermally comfortable conditions. The set includes variations in SHGC (representing laminated glazing and a higher-performance Low-E system), a reduced WWR configuration, and a fully shaded façade option. All alternatives are assessed using the three-subzone model with independent subzone control. The evaluation compares comfort performance under two Ta setpoints (a practice-based reference and a lower setpoint derived from comfort outcomes), and then contrasts energy implications of strategies that achieve comfort using Ta control versus To-based control targets.
""".strip()

    import re

    def md_to_html(md: str) -> str:
        lines = md.splitlines()
        out = []
        paragraph = []

        def flush_paragraph():
            nonlocal paragraph
            if paragraph:
                txt = " ".join(paragraph).strip()
                # colapsa espaços múltiplos
                txt = re.sub(r"\s{2,}", " ", txt)
                out.append(f"<p>{txt}</p>")
                paragraph = []

        for raw in lines:
            line = raw.strip()
            if not line:
                flush_paragraph()
                continue

            if line.startswith("### "):
                flush_paragraph()
                out.append(f"<h3>{line[4:].strip()}</h3>")
                continue

            if line.startswith("#### "):
                flush_paragraph()
                out.append(f"<h4>{line[5:].strip()}</h4>")
                continue

            paragraph.append(line)

        flush_paragraph()
        return "\n".join(out)

    SUMMARY_HTML = md_to_html(SUMMARY_TEXT)

    st.markdown("""
<style>
.sum-wrap{
    width:1000px;
    max-width:100%;
    margin-left:0;
    margin-right:auto;
}

/* texto principal */
.sum-wrap{
    font-size:15px;
    line-height:1.55;
    text-align:justify;
    color:#222;
}

/* TÍTULOS DE TÓPICO (###) */
.sum-wrap h3{
    font-size:22px;
    font-weight:800;
    margin-top:18px;
    margin-bottom:10px;
    color:#111;
}

/* SUBTÍTULOS (####) */
.sum-wrap h4{
    font-size:16px;
    font-weight:800;
    margin-top:12px;
    margin-bottom:8px;
    color:#111;
}

/* espaçamento */
.sum-wrap p{
    margin-top:0;
    margin-bottom:10px;
}

.sum-note{
    margin-top:14px;
    font-size:12px;
    color:#777;
    font-style:italic;
}
</style>
""", unsafe_allow_html=True)

    st.markdown(
        f"""
<div class="sum-wrap">
  {SUMMARY_HTML}

  <div class="sum-note">
    Note: This section was generated with AI assistance from the author’s original draft and then edited for clarity and structure.
  </div>
  <div class="sum-note">
    References: See original paper (link will be available soon).
  </div>
</div>
""",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------------
    # Renderiza o Markdown dentro de um DIV real
    # ---------------------------------------------------------
    # Converte Markdown simples em HTML (títulos + parágrafos)
    # (sem depender do container do Streamlit)
    import re

    def _md_to_html(md: str) -> str:
        lines = md.splitlines()
        out = []
        paragraph = []

        def flush_paragraph():
            nonlocal paragraph
            if paragraph:
                text = " ".join(paragraph).strip()
                out.append(f"<p>{text}</p>")
                paragraph = []

        for raw in lines:
            line = raw.strip()
            if not line:
                flush_paragraph()
                continue

            if line.startswith("### "):
                flush_paragraph()
                out.append(f"<h3>{line[4:].strip()}</h3>")
                continue

            if line.startswith("#### "):
                flush_paragraph()
                out.append(f"<h4>{line[5:].strip()}</h4>")
                continue

            paragraph.append(line)

        flush_paragraph()

        html = "\n".join(out)
        # pequenos ajustes: múltiplos espaços e travessões já ok
        html = re.sub(r"\s{2,}", " ", html)
        return html

    


with tabs[2]:
    # Layout: plant bigger, controls+energy on right
    colL, colR = st.columns([2.2, 1.0], gap="large")

    # -------- Right column (controls + energy)
    with colR:
        st.markdown("#### THERMAL COMFORT PARAMETER")
        st.markdown(
            f"""
            <div style="
                font-size:{SUBTITLE_SIZE}px;
                color:{SUBTITLE_COLOR};
                margin-top:-6px;
                margin-bottom:{SUBTITLE_MARGIN_BOTTOM};
            ">
                *Percentage of occupied hours in a year above and below thermal comfort thresholds
            </div>
            """,
            unsafe_allow_html=True
        )

        comfort_mode = st.radio(
            "Select parameter",
            ["To", "PMV"],
            label_visibility="collapsed"
        )


        st.markdown("#### TEMPERATURE CONTROL")
        st.markdown(
            f"""
            <div style="
                font-size:{SUBTITLE_SIZE}px;
                color:{SUBTITLE_COLOR};
                margin-top:-6px;
                margin-bottom:{SUBTITLE_MARGIN_BOTTOM};
            ">
                *Choose thermostat control type
            </div>
            """,
            unsafe_allow_html=True
        )

        control_kind = st.radio(
            "Select control",
            ["Air-temperature thermostat (Ta)", "Operative-temperature thermostat (To)"],
            label_visibility="collapsed"
        )

        active_kind = "Ta" if control_kind.startswith("Air") else "To"

        st.markdown("#### SETPOINT")
        if active_kind == "Ta":
            active_sp = st.slider("Ta setpoint (°C)", 19, 24, 21, 1, key="ta_sp_tab3")
            ds = COMFORT_TA
        else:
            active_sp = st.slider("To setpoint (°C)", 22, 27, 26, 1, key="to_sp_tab3")
            ds = COMFORT_TO

        # compute zone values for plant (must be BEFORE drawing plant)
        zone_hot = {}
        zone_cold = {}
        for z in ["A", "B", "C"]:
            metrics = ds[z][active_sp]
            if comfort_mode == "To":
                zone_hot[z] = metrics["To_gt_26"]
                zone_cold[z] = metrics["To_lt_23"]
            else:  # PMV
                zone_hot[z] = metrics["PMV_gt_p05"]
                zone_cold[z] = metrics["PMV_lt_m05"]

        st.markdown("#### COOLING ENERGY USE")

        # Reference right under the title
        if active_kind == "Ta":
            ref_sp = st.radio(
                "Reference (Ta)",
                [19, 20, 21, 22, 23, 24],
                index=4,
                horizontal=True,
                key="ref_ta_tab3"
            )
        else:
            ref_sp = st.radio(
                "Reference (To)",
                [22, 23, 24, 25, 26, 27],
                index=1,
                horizontal=True,
                key="ref_to_tab3"
            )

        figE, delta = make_energy_chart(active_kind=active_kind, active_sp=active_sp, ref_sp=ref_sp)

        if delta is not None:
            st.info(f"Relative change vs reference: **{delta:+.2f}%**")

        st.plotly_chart(figE, width="stretch", config={"responsive": False}, key="tab3_energy")
        
    # -------- Left column (plan) — ONLY the plan here
    with colL:
        fig_plan = make_plan_figure(zone_hot, zone_cold)
        st.plotly_chart(fig_plan, width="stretch", config={"responsive": False}, key="tab3_plan")

        st.markdown(
            f"""
            <div style="
                text-align: center;
                font-size: {PLAN_CAPTION_SIZE}px;
                margin-top: {PLAN_CAPTION_MARGIN_TOP}px;
                color: {PLAN_CAPTION_COLOR};
                line-height: 1.1;
            ">
                {PLAN_CAPTION_TEXT}
            </div>
            """,
            unsafe_allow_html=True
        )

        from PIL import Image

        # =========================
        # BASE CASE — MAIN CHARACTERISTICS (below plan)
        # =========================

        # 1) TÍTULO
        st.markdown(
            f"""
            <div style="
                font-weight:700;
                color:{BC_TITLE_COLOR};
                margin-bottom:4px;
            ">
                Base case model (BC): main characteristics
            </div>
            """,
            unsafe_allow_html=True
        )

        # 2) DIVIDER (logo abaixo do título) — ANTES das colunas
        st.markdown(
            f"""
            <div style="max-width:{BC_BLOCK_MAX_WIDTH_PX}px;">
                <hr style="margin:{BC_DIVIDER_MARGIN_PX}px 0 {BC_DIVIDER_MARGIN_PX}px 0;">
            </div>
            """,
            unsafe_allow_html=True
        )

        # 3) AGORA SIM: duas colunas (texto | imagem)
        bc_col_text, bc_col_img = st.columns([2.2, 1.0], gap="small")

        # ---- TEXTO (esquerda) — dentro da coluna
        with bc_col_text:
            st.markdown(
                f"""
                <div style="font-size:{BC_TEXT_FONT_PX}px; color:#222; line-height:1.5;">
                    Room dimensions: 4.00 m (Width), 7.50 m (Depth), 2.80 m (Ceiling height)<br>
                    Typical Brazilian office workspace routine (Occupied period: 08:00–18:00)<br>
                    Shoe-box model: adiabatic floor, ceiling, and walls, except for the façade wall<br>
                    Fully glazed façade: curtain wall (WWR 100%)<br>
                    Laminated glass: SHGC of 0.29 and no external shading<br>
                    Window orientation: East<br>
                    HVAC system: unitary split AC no fresh air<br>
                    Climate: city of Fortaleza, Brazil (03°46´ S; 38´ W) / ASHRAE climate 0A
                </div>
                """,
                unsafe_allow_html=True
            )

        # ---- IMAGEM (direita)
        with bc_col_img:
            img_path = ASSETS_DIR / "shoeboxmodel.png"
            if img_path.exists():

                justify_map = {
                    "left": "flex-start",
                    "center": "center",
                    "right": "flex-end",
                    "flex-start": "flex-start",
                    "flex-end": "flex-end",
                }
                justify_css = justify_map.get(
                    BC_IMG_ALIGN,
                    BC_IMG_JUSTIFY if "BC_IMG_JUSTIFY" in globals() else "center"
                )

                img_b64 = base64.b64encode(img_path.read_bytes()).decode()

                st.markdown(
                    f"""
                    <div style="
                        width:100%;
                        max-width:{BC_IMG_MAX_COL_W_PX}px;
                        display:flex;
                        flex-direction:column;
                        align-items:center;
                        margin-top:{BC_IMG_MARGIN_TOP_PX}px;
                    ">

                    <div style="
                        width:100%;
                        display:flex;
                        justify-content:{justify_css};
                    ">
                        <img src="data:image/png;base64,{img_b64}"
                            style="
                                width:{BC_IMG_WIDTH_PX}px;
                                height:auto;
                                transform: translateX({BC_IMG_OFFSET_X_PX}px);
                            ">
                    </div>

                    <div style="
                        font-size:{BC_IMG_CAPTION_SIZE}px;
                        color:{BC_IMG_CAPTION_COLOR};
                        text-align:center;
                        margin-top:4px;
                        max-width:{BC_IMG_WIDTH_PX}px;
                    ">
                        Representation of an office workspace modelled as a “shoe-box”
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.warning("Missing: shoeboxmodel.png")

with tabs[1]:
    # =========================================================
    # TAB 2 — THERMAL ZONING (refinado / estável)
    # =========================================================
    from PIL import Image
    import base64

    # -------------------------
    # DADOS POR MODELO
    # -------------------------
    ZONE_MODELS = {
        "Zone Model 1": {
            "iso": "iso_1zone.png",
            "plan": "plan_1zone.png",
            "to": "plot_1zone_to.png",
            "pmv": "plot_1zone_pmv.png",
            "desc": [
                "One single-zone",
                "To and PMV calculated to the area´s geometric centre",
                "Goal: to define the baseline",
            ],
            "outcomes": [
                "Predominantly uncomfortable thermal performance, with 75.3% of occupied hours presenting To > 26°C.",
                "Operative temperature ranged from 25°C to 28°C, indicating high thermal instability.",
                "Thermal sensation followed the same trend, with 74.5% of PMV > +0.5, reaching values up to +1.5.",
                "Results indicate that a single-zone model masks spatial thermal variability and overgeneralizes discomfort.",
            ],
        },
        "Zone Model 2": {
            "iso": "iso_2zone.png",
            "plan": "plan_2zone.png",
            "to": "plot_2zone_to.png",
            "pmv": "plot_2zone_pmv.png",
            "desc": [
                "Two subzones: perimeter (A) and core (D) zones",
                "Perimeter subzone is 1/3 of the workspace length",
                "Goal: to compare perimeter and core subzone performance",
            ],
            "outcomes": [
                "Clear thermal differentiation between subzones, confirming the importance of spatial zoning.",
                "Perimeter subzone (A) showed severe discomfort: 84.6% of To > 26°C and 83.4% of PMV > +0.5, with 48.7% of To exceeding 27°C.",
                "Core subzone (D) was significantly more stable, with only 33.9% of To > 26°C and 35.6% of PMV > +0.5, and negligible extreme overheating.",
                "This model highlights the dominant impact of façade proximity on thermal discomfort.",
            ],
        },
        "Zone Model 3": {
            "iso": "iso_3zone.png",
            "plan": "plan_3zone.png",
            "to": "plot_3zone_to.png",
            "pmv": "plot_3zone_pmv.png",
            "desc": [
                "Three subzones parallel to the facade with the same area: A: adjacent to the facade; B: in the middle; C: deepest zone",
                "Goal: to check an intermediate thermal zone between the perimeter and core subzones",
            ],
            "outcomes": [
                "Introduced an intermediate subzone (B) with moderate discomfort levels (31.9% of To > 26°C and PMV > +0.5).",
                "Perimeter subzone (A) remained highly uncomfortable, with 81.9% of To > 26°C and 80.7% of PMV > +0.5, similar to Zone Model 2.",
                "Core subzone (C) was predominantly comfortable and thermally stable, with only 3.2% of To > 26°C and 7.9% of PMV > +0.5.",
                "This configuration captures a thermal gradient from façade to core, improving representativeness without unnecessary complexity.",
            ],
        },
        "Zone Model 9": {
            "iso": "iso_9zone.png",  # conforme seu naming
            "plan": "plan_9zone.png",
            "to": "plot_9zone_to.png",
            "pmv": "plot_9zone_pmv.png",
            "desc": [
                "Nine subzones with the same area: A1, A2, A3, B1, B2, B3, C1, C2, C3",
                "Goal: To assess the influence of side walls on the thermal zones",
            ],
            "outcomes": [
                "Zones located on the same row showed very similar thermal behavior (A1 ≈ A2 ≈ A3; B1 ≈ B2 ≈ B3; C1 ≈ C2 ≈ C3).",
                "Side walls had no expressive influence on thermal comfort distribution.",
                "Effect size analysis confirmed this redundancy: Cohen’s d < 0.2 for all paired zones, and high overlap coefficients (OVL) for both To and PMV.",
                "Results demonstrate that additional lateral subdivisions do not add analytical value.",
            ],
        },
    }

    # -------------------------
    # Dropdown menor (não estica)
    # -------------------------
    dd_col, _ = st.columns([0.35, 0.65], gap="small")
    with dd_col:
        st.markdown(
            f"""
            <style>
            div[data-testid="stSelectbox"] {{
                max-width: {TZ_DROPDOWN_WIDTH_PX}px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        sel = st.selectbox(
            "",
            list(ZONE_MODELS.keys()),
            index=0,
            label_visibility="collapsed",
            key="tz_model_select",
        )

    st.markdown(f"<div style='height:{TZ_TOP_SPACER_PX}px'></div>", unsafe_allow_html=True)

    model_num = sel.replace("Zone Model ", "").strip()
    cfg = ZONE_MODELS[sel]

    # -------------------------
    # Paths das imagens (SEM variáveis indefinidas!)
    # -------------------------
    iso_path = ASSETS_DIR / cfg["iso"]
    plan_path = ASSETS_DIR / cfg["plan"]
    to_path = ASSETS_DIR / cfg["to"]
    pmv_path = ASSETS_DIR / cfg["pmv"]

    # =========================================================
    # LINHA SUPERIOR: ESQ (ISO+PLANTA) | DIR (TO+PMV)
    # =========================================================
    colL, colR = st.columns([TZ_LEFT_COL_RATIO, TZ_RIGHT_COL_RATIO], gap="large")

    # ---- esquerda: iso em cima + planta embaixo (alinhadas)
    with colL:
        # ISO
        if iso_path.exists():
            st.image(Image.open(iso_path), width=TZ_ISO_WIDTH_PX)
        else:
            st.warning(f"Missing: {iso_path.name}")

        st.markdown(f"<div style='height:{TZ_ISO_PLAN_GAP_PX}px'></div>", unsafe_allow_html=True)

        # PLANTA: render em "stage" com translate controlável (X/Y)
        if plan_path.exists():
            plan_b64 = base64.b64encode(plan_path.read_bytes()).decode("utf-8")
            clip_css = "hidden" if TZ_PLAN_CLIP else "visible"

            # Se você sobe a planta (offset_y negativo), reduz a altura do palco proporcionalmente
            # Ex.: offset_y = -80 => palco fica 260 - 80 = 180
            stage_h = TZ_PLAN_STAGE_H_PX + min(0, TZ_PLAN_OFFSET_Y_PX)
            stage_h = max(TZ_PLAN_STAGE_MIN_H_PX, stage_h)


            st.markdown(
                f"""
                <div style="
                    width:{TZ_LEFT_MAX_WIDTH_PX}px;
                    max-width:100%;
                    position:relative;
                    overflow:{clip_css};
                    height:{stage_h}px;
                    padding:{TZ_PLAN_PAD_PX}px;
                    box-sizing:border-box;
                ">
                <img src="data:image/png;base64,{plan_b64}"
                    style="
                        width:{TZ_PLAN_WIDTH_PX}px;
                        height:auto;
                        position:absolute;
                        left:{TZ_PLAN_PAD_PX}px;
                        top:{TZ_PLAN_PAD_PX}px;
                        transform: translate({TZ_PLAN_OFFSET_X_PX}px, {TZ_PLAN_OFFSET_Y_PX}px);
                        transform-origin: top left;
                        z-index:{TZ_PLAN_ZINDEX};
                        pointer-events:none;
                    "/>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.warning(f"Missing: {plan_path.name}")

    # ---- direita: dois plots maiores e mais próximos entre si
    with colR:
        p1, p2 = st.columns(2, gap=TZ_RIGHT_PLOTS_GAP)

        with p1:
            if to_path.exists():
                st.image(Image.open(to_path), width=TZ_PLOT_TO_WIDTH_PX)
            else:
                st.warning(f"Missing: {to_path.name}")

        with p2:
            if pmv_path.exists():
                st.image(Image.open(pmv_path), width=TZ_PLOT_PMV_WIDTH_PX)
            else:
                st.warning(f"Missing: {pmv_path.name}")

        # legenda SEM wrap (há espaço)
        st.markdown(
            f"""
            <div style="margin-top:6px; font-size:{TZ_LEGEND_FONT_PX}px; color:#333; white-space:nowrap;">
                Zone Model {model_num} performance for To and PMV: annual hourly frequency during occupied periods above and below thresholds
            </div>
            <div style="font-size:{TZ_THRESH_FONT_PX}px; color:#666; line-height:1.35; margin-top:4px;">
                * To &lt; 23°C | To &gt; 23°C<br>
                * PMV &lt; −0.5 | PMV &gt; +0.5
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # =========================================================
    # LINHA INFERIOR: ESQ (características) | DIR (Zone Model + Outcomes)
    # =========================================================
    botL, botR = st.columns([TZ_LEFT_COL_RATIO, TZ_RIGHT_COL_RATIO], gap="large")

    with botL:
        st.markdown(f"<div style='font-weight:700; color:{TZ_SECTION_TITLE_COLOR};'>Model: main characteristics</div>", unsafe_allow_html=True)
        st.markdown(f"<hr style='margin:{TZ_DIVIDER_MARGIN_PX}px 0 {TZ_DIVIDER_MARGIN_PX}px 0;'>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="font-size:{TZ_TEXT_FONT_PX}px; color:#222; line-height:1.5;">
            Room dimensions: 12.0 m (Width), 7.50 m (Depth), 2.80 m (Ceiling height)<br>
            Typical Brazilian office workspace routine (Occupied period: 08:00–18:00)<br>
            Shoe-box model: adiabatic floor, ceiling, and walls, except for the façade wall<br>
            Fully glazed façade: curtain wall (WWR 100%)<br>
            Window orientation: East<br>
            Laminated glass: SHGC of 0.29 and no external shading<br>
            HVAC system: unitary split AC no fresh air<br>
            Setpoint and thermostat control: 23°C air-temperature cooling setpoint<br>
            Climate: city of Fortaleza, Brazil (03°46´ S; 38´ W) / ASHRAE climate 0A
            </div>
            """,
            unsafe_allow_html=True
        )

    with botR:
        r1, r2 = st.columns(2, gap="large")

        with r1:
            st.markdown(f"<div style='font-weight:700; color:{TZ_SECTION_TITLE_COLOR};'>Zone Model {model_num}</div>", unsafe_allow_html=True)
            st.markdown(f"<hr style='margin:{TZ_DIVIDER_MARGIN_PX}px 0 {TZ_DIVIDER_MARGIN_PX}px 0;'>", unsafe_allow_html=True)

            st.markdown(
                "<div style='font-size:{}px; color:#222; line-height:1.5;'>".format(TZ_TEXT_FONT_PX)
                + "<br>".join([f"- {t}" for t in cfg["desc"]]) +
                "</div>",
                unsafe_allow_html=True
            )

        with r2:
            st.markdown(f"<div style='font-weight:700; color:{TZ_SECTION_TITLE_COLOR};'>Outcomes</div>", unsafe_allow_html=True)
            st.markdown(f"<hr style='margin:{TZ_DIVIDER_MARGIN_PX}px 0 {TZ_DIVIDER_MARGIN_PX}px 0;'>", unsafe_allow_html=True)

            st.markdown(
                "<div style='font-size:{}px; color:#222; line-height:1.5;'>".format(TZ_TEXT_FONT_PX)
                + "<br>".join([f"- {t}" for t in cfg["outcomes"]]) +
                "</div>",
                unsafe_allow_html=True
            )

with tabs[3]:
    # Facade Design Alternatives
    colL, colR = st.columns([2.2, 1.0], gap="large")

    # helper map
    alt_by_id = {a["id"]: a for a in FACADE_ALTS}
    alt_ids = [a["id"] for a in FACADE_ALTS]

    # -----------------------------
    # RIGHT: controls + energy
    # -----------------------------
    with colR:
        st.markdown("#### THERMAL COMFORT PARAMETER")
        st.markdown(
            f"""
            <div style="
                font-size:{SUBTITLE_SIZE}px;
                color:{SUBTITLE_COLOR};
                margin-top:-6px;
                margin-bottom:{SUBTITLE_MARGIN_BOTTOM};
            ">
                *Percentage of occupied hours in a year above and below thermal comfort thresholds
            </div>
            """,
            unsafe_allow_html=True
        )
        comfort_mode_4 = st.radio(
            "Select parameter (tab4)",
            ["To", "PMV"],
            label_visibility="collapsed",
            key="comfort_mode_tab4"
        )

        st.markdown("#### TEMPERATURE CONTROL")
        st.markdown(
            f"""
            <div style="
                font-size:{SUBTITLE_SIZE}px;
                color:{SUBTITLE_COLOR};
                margin-top:-6px;
                margin-bottom:{SUBTITLE_MARGIN_BOTTOM};
            ">
                *Choose thermostat control type
            </div>
            """,
            unsafe_allow_html=True
        )

        control_kind_4 = st.radio(
            "Select control (tab4)",
            ["Air-temperature thermostat (Ta)", "Operative-temperature thermostat (Cooling energy use only)"],
            label_visibility="collapsed",
            key="control_kind_tab4"
        )
        active_ctrl_4 = "Ta" if control_kind_4.startswith("Air") else "To"

        st.markdown("#### SETPOINT")

        if active_ctrl_4 == "Ta":
            ta_sp_4 = st.radio(
                "Ta setpoint (°C)",
                [21, 23],
                index=0,
                horizontal=True,
                key="ta_sp_tab4"
            )
        else:
            # "radio" único como na imagem (um item só)
            to_sp_4 = st.radio(
                "To setpoint (°C)",
                ["26"],
                index=0,
                horizontal=True,
                key="to_sp_tab4_fixed"
            )
            # valor numérico pra usar no cálculo (se precisar)
            to_sp_4 = 26
            ta_sp_4 = 21  # dummy (plan é Ta-only mesmo)


        st.markdown("#### COOLING ENERGY USE")

        ref_alt_4 = st.radio(
            "Reference (Facade Design)",
            alt_ids,
            index=2,  # base case = ALT3
            horizontal=False,
            format_func=lambda _id: alt_by_id[_id]["label"].replace("\n", " "),
            key="ref_alt_tab4"
        )

        active_alt_4 = st.session_state.get("active_alt_tab4", "ALT3")

        # ENERGY PLOT
        figE4 = None
        delta4 = None

        if active_ctrl_4 == "Ta":
            y_check = list(ENERGY_FACADE_TA[ta_sp_4].values())
            if all(v is None for v in y_check):
                st.warning("Cooling energy chart for Ta=23°C is not available yet.")
            else:
                figE4 = make_energy_chart_facade(
                    control_kind="Ta",
                    ta_setpoint=ta_sp_4,
                    active_alt_id=active_alt_4
                )
                Ea = ENERGY_FACADE_TA[ta_sp_4].get(active_alt_4, None)
                Er = ENERGY_FACADE_TA[ta_sp_4].get(ref_alt_4, None)
                if (Ea is not None) and (Er not in (None, 0)):
                    delta4 = (Ea - Er) / Er * 100.0
        else:
            figE4 = make_energy_chart_facade(
                control_kind="To",
                ta_setpoint=ta_sp_4,  # ignorado para To
                active_alt_id=active_alt_4
            )
            Ea = ENERGY_FACADE_TO26.get(active_alt_4, None)
            Er = ENERGY_FACADE_TO26.get(ref_alt_4, None)
            if (Ea is not None) and (Er not in (None, 0)):
                delta4 = (Ea - Er) / Er * 100.0

        if delta4 is not None:
            st.info(f"Relative change vs reference: **{delta4:+.2f}%**")

        if figE4 is not None:
            st.plotly_chart(figE4, width="stretch", config={"responsive": False}, key="tab4_energy")

        if active_ctrl_4 == "To":
            st.caption("*Thermal comfort (false-color plan) is available for Ta only. To mode shows cooling energy use only.")


    # -----------------------------
    # LEFT: plan (same position as tab3) + BELOW: facade table
    # -----------------------------
    with colL:
        
        # ---- Compute plan values (depends on selectors + active alt)
        with colL:

            active_alt_4 = st.session_state.get("active_alt_tab4", "ALT3")

            if active_ctrl_4 == "To":
                # Placeholder (no comfort map for To mode)
                fig_plan4 = make_plan_placeholder("No results for Operative-temperature thermostat (To)")
                st.plotly_chart(fig_plan4, width="stretch", config={"responsive": False}, key="tab4_plan_placeholder")

            else:
                # ---- Compute plan values (Ta mode only)
                zone_hot_4 = {}
                zone_cold_4 = {}
                for z in ["A", "B", "C"]:
                    metrics = COMFORT_FACADE_TA[ta_sp_4][z][active_alt_4]
                    if comfort_mode_4 == "To":
                        zone_hot_4[z] = metrics["To_gt_26"]
                        zone_cold_4[z] = metrics["To_lt_23"]
                    else:
                        zone_hot_4[z] = metrics["PMV_gt_p05"]
                        zone_cold_4[z] = metrics["PMV_lt_m05"]

                fig_plan4 = make_plan_figure(zone_hot_4, zone_cold_4)
                st.plotly_chart(fig_plan4, width="stretch", config={"responsive": False}, key="tab4_plan")

            # Caption (pode manter)
            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    font-size: {PLAN_CAPTION_SIZE}px;
                    margin-top: {PLAN_CAPTION_MARGIN_TOP}px;
                    color: {PLAN_CAPTION_COLOR};
                    line-height: 1.1;
                ">
                    {PLAN_CAPTION_TEXT}
                </div>
                """,
                unsafe_allow_html=True
            )


        st.divider()

        # ---- FACADE TABLE (BELOW THE PLAN) - aligned grid (1 label col + 5 alts)
        st.markdown("#### FACADE DESIGN ALTERNATIVES")

        alt_ids = [a["id"] for a in FACADE_ALTS]

        # ---- OUTER GRID: labels + area das 5 alternativas
        outer = st.columns([0.55, 5.0], gap="small")

        # =========================
        # LINHA 1: SELETOR DEFINITIVO (5 botões alinhados às 5 imagens)
        # =========================
        if "active_alt_tab4" not in st.session_state:
            st.session_state["active_alt_tab4"] = "ALT3"

        with outer[0]:
            st.markdown("&nbsp;", unsafe_allow_html=True)

        with outer[1]:
            st.markdown("<div id='tab4_dot_anchor'></div>", unsafe_allow_html=True)

            dot_cols = st.columns(5, gap="small")

            for c, alt in zip(dot_cols, FACADE_ALTS):
                alt_id = alt["id"]
                is_active = (st.session_state["active_alt_tab4"] == alt_id)

                # botão SEM texto (vamos desenhar o quadradinho via CSS)
                if c.button("", key=f"dot_{alt_id}", use_container_width=True,
                            type="primary" if is_active else "secondary"):
                    st.session_state["active_alt_tab4"] = alt_id
                    st.rerun()
          

        active_alt_4 = st.session_state["active_alt_tab4"]


        # =========================
        # LINHA 2: IMAGENS (5 colunas internas)
        # =========================
        with outer[0]:
            st.markdown("&nbsp;", unsafe_allow_html=True)

        with outer[1]:
            cols_img = st.columns(5, gap="small")

            BASE_IMG_W = 520
            IMG_W = max(80, int(BASE_IMG_W * FACADE_IMG_SCALE))

            for c, alt in zip(cols_img, FACADE_ALTS):
                with c:
                    img_path = Path(alt["img"])
                    if img_path.exists():
                        st.image(str(img_path), width=IMG_W)
                    else:
                        st.warning(f"Missing: {img_path.name}")

        # =========================
        # LINHA 3: NOMES (5 colunas internas)
        # =========================
        with outer[0]:
            st.markdown("&nbsp;", unsafe_allow_html=True)

        with outer[1]:
            cols_name = st.columns(5, gap="small")
            for c, alt in zip(cols_name, FACADE_ALTS):
                with c:
                    st.markdown(
                        f"<div style='text-align:center; font-size:{FACADE_TITLE_SIZE}px; line-height:1.15;'>"
                        f"{alt['label'].replace(chr(10), '<br>')}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # =========================
        # LINHA 4: METADADOS (grid 6 colunas — ALINHADO)
        # =========================
        meta_row = st.columns([0.55, 1, 1, 1, 1, 1], gap="small")

        with meta_row[0]:
            st.markdown(
                f"""
                <div class="tab4-meta-left" style="
                    font-size:{FACADE_TABLE_LABEL_SIZE}px;
                    line-height:1.55;
                    text-align:left;
                ">
                <b>SHGC</b><br>
                <b>WWR</b><br>
                <b>Type</b><br>
                <b>Shading</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        for i, alt in enumerate(FACADE_ALTS, start=1):
            with meta_row[i]:
                m = alt["meta"]
                st.markdown(
                    f"""
                    <div class="tab4-meta-mid" style="
                        text-align:center;
                        font-size:{FACADE_META_SIZE}px;
                        line-height:1.55;
                    ">
                    {m['SHGC']}<br>
                    {m['WWR']}<br>
                    {m['Type']}<br>
                    {m['Shading']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


with tabs[4]:
    # =========================================================
    # TAB 5 — CONCLUSIONS & CONTRIBUTION
    # =========================================================

    CONC_TITLE = "Conclusions & Contribution"

    CONC_TEXT = """
This study shows that even a relatively optimistic low solar factor is not sufficient to ensure a uniform thermal sensation inside a single highly glazed office room in a tropical climate. The simulations indicate the emergence of three distinct thermal subzones aligned with the façade influence: a perimeter zone (approximately 0–2.5 m), strongly affected by solar gains; an intermediate zone (2.5–5.0 m), moderately influenced; and a core zone (beyond ~5.0 m), only slightly affected by façade design. This refines common assumptions that the room can be represented by a single “core” condition beyond ~4.5–5.0 m, suggesting that two meaningful subzones may exist between the façade and the core, depending on glass properties and interior shading conditions. As a practical consequence, HVAC designers face a non-trivial task when defining thermal zone depths in whole-building energy simulation tools, because simplified zoning may conceal important spatial discomfort patterns.

The work also demonstrates that thermal comfort and cooling energy use are strongly dependent on the thermostat metric and setpoint strategy. When different thermal subzones are controlled independently, it becomes feasible to achieve comfort with an operative-temperature setpoint near 26°C, while reducing cooling energy use by roughly 10% compared to a conventional strategy relying on very low air-temperature setpoints (e.g., 21°C) to maintain comfort across the entire space with a single control. However, the analysis highlights a critical market and practice limitation: operative-temperature-based thermostats are generally not available, and the common response—lowering air temperature setpoints—has a clear energy penalty, with each 1°C reduction increasing cooling energy consumption on the order of 5–7%. This mechanism helps explain the paradox of overcooling in tropical office buildings, where occupants may end up requiring additional clothing while energy is wasted to compensate for façade-driven non-uniformity.

Comparisons among façade design alternatives reinforce that a highly glazed façade tends to sustain a non-uniform thermal environment even under relatively conservative air-temperature setpoints. Increasing the solar factor further aggravates the problem, while strategies such as reducing window-to-wall ratio or providing effective external shading are more efficient in reducing cooling demand. Yet, the study stresses an important design trade-off: lowering solar factor through currently available glazing options often reduces visible transmittance, potentially compromising daylight availability and the perceived connection to the exterior—qualities that frequently motivate fully glazed architectural language. In this sense, the research exposes a persistent tension between aesthetic preferences for transparency and the environmental performance required for thermal comfort and responsible energy use in the tropics.

The main contribution of this research is methodological and practical. Methodologically, it proposes a modelling abstraction using fictitious, fully open partitions to represent thermal subzones within a single room, overcoming common software limitations for assessing non-uniform thermal environments. Practically, it provides actionable guidance for designers and engineers: (1) acknowledge façade-driven thermal subzones in early layout decisions; (2) avoid continuous occupancy of the perimeter zone when feasible; (3) provide independent thermal control by subzone—ideally using operative-temperature logic; and (4) reduce solar gains without undermining indoor environmental quality, combining appropriate glazing selection (balancing solar factor and visible transmittance) with external shading whenever viable. Ultimately, the findings argue that maintaining highly glazed façades as a default design choice imposes avoidable comfort and energy burdens, reinforcing the ethical and professional responsibility of designers in an era of climate change.

Key limitations remain related to the necessary modelling abstractions used to delineate subzones within EnergyPlus and the lack of a fully adequate thermal comfort index for non-uniform environments, indicating the need for future research focused on improved metrics and control technologies.
""".strip()

    # ---------------------------------------------------------
    # Converte texto em HTML (parágrafos), sem f-string com \n
    # ---------------------------------------------------------
    CONC_HTML = "<p>" + CONC_TEXT.replace("\n\n", "</p><p>") + "</p>"

    # ---------------------------------------------------------
    # Estilos locais (1000px, justificado, mesma tipografia da Summary)
    # ---------------------------------------------------------
    st.markdown("""
<style>
.conc-wrap{
    width:1000px;
    max-width:100%;
    margin-left:0;
    margin-right:auto;
    font-size:15px;
    line-height:1.55;
    text-align:justify;
    color:#222;
}

/* título principal — igual ao h3 da Summary */
.conc-wrap h3{
    font-size:22px;
    font-weight:800;
    margin-top:18px;
    margin-bottom:10px;
    color:#111;
}

/* parágrafos */
.conc-wrap p{
    margin-top:0;
    margin-bottom:10px;
}

/* nota final */
.conc-note{
    margin-top:14px;
    font-size:12px;
    color:#777;
    font-style:italic;
}
</style>
""", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Render único (título + texto + nota) dentro do wrapper real
    # ---------------------------------------------------------
    st.markdown(
        f"""
<div class="conc-wrap">
  <h3>{CONC_TITLE}</h3>
  {CONC_HTML}
  <div class="conc-note">
    Note: This section was generated with AI assistance from the author’s original draft and then edited for clarity and structure.
  </div>
</div>
""",
        unsafe_allow_html=True
    )

st.divider()
st.caption("Results from building simulations conducted as part of a doctoral thesis at the Graduate Program in Architecture and Urbanism (PPGAU/UFRN - Brazil), under the supervision of Senior Lecturer PhD Aldomar Pedrini (Aug/2024).")
st.caption("www.greensim.com.br     | 2026" \
"")
