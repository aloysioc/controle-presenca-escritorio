import streamlit as st
import datetime as dt
import calendar
import json
from pathlib import Path
from feriados_brasil import feriados_brasil

# ---------- CONFIGURAÇÃO BÁSICA ----------

ARQUIVO = Path("presencas_calendario.json")
ESTADO = "SP"  # Estado para feriados (SP, RJ, MG, etc.)

CORES = {
    "none": "#FFFFFF",     # sem marcação
    "presenca": "#00C853", # verde vivo
    "ferias": "#FF5252",   # vermelho vivo
    "feriado": "#2979FF",  # azul vivo
}

def proximo_estado(atual: str) -> str:
    if atual == "none":
        return "presenca"
    elif atual == "presenca":
        return "ferias"
    else:
        return "none"

# ---------- FERIADOS (via biblioteca + cálculo de datas móveis) ----------

def feriados_ano(ano: int):
    """Retorna conjunto de datas que são feriados no ano especificado."""
    feriados_dict = feriados_brasil(ano, state=ESTADO, include_moveis=True)
    return set(feriados_dict.keys())

# ---------- PERSISTÊNCIA EM JSON ----------

def carregar_json():
    if ARQUIVO.exists():
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    return {}

def salvar_json(dias_estado: dict):
    ARQUIVO.write_text(
        json.dumps(dias_estado, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# ---------- CALENDÁRIO ----------

def gerar_matriz_mes(ano: int, mes: int):
    cal = calendar.Calendar(firstweekday=6)  # 6 = domingo
    return [list(week) for week in cal.monthdatescalendar(ano, mes)]

# ---------- APP STREAMLIT ----------

st.set_page_config("Controle Escritório – Calendário", layout="centered", initial_sidebar_state="collapsed")

# CSS para otimizar espaço vertical
st.markdown("""
<style>
    .block-container {padding-top: 0.5rem; padding-bottom: 0.5rem;}
    .stMarkdown {margin-bottom: 0rem; margin-top: 0rem;}
    [data-testid="stMetricContainer"] {margin-bottom: 0rem; margin-top: 0rem;}
    [data-testid="stMetricValue"] {font-size: 1.2rem;}
    [data-testid="stMetricLabel"] {font-size: 0.75rem;}
    .stNumberInput, .stSelectbox {margin-bottom: 0.5rem;}
    .stButton {margin-bottom: 0rem;}
    div[data-testid="stHorizontalBlock"] > div {margin-bottom: 0rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='margin: 0rem 0rem 0.3rem 0rem; font-size: 1.3rem;'>Controle 60%</h2>", unsafe_allow_html=True)

# Carrega dados já salvos em disco
dados_salvos = carregar_json()

if "dias_estado" not in st.session_state:
    st.session_state.dias_estado = {}

# Hidrata o session_state com o que veio do JSON
for data_str, estado in dados_salvos.items():
    st.session_state.dias_estado[data_str] = estado

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    ano = st.number_input("Ano", min_value=2024, max_value=2030, value=2026, step=1, label_visibility="collapsed")
with col2:
    mes = st.selectbox("Mês", options=list(range(1, 13)), format_func=lambda m: ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"][m-1], index=1, label_visibility="collapsed")
with col3:
    st.write("")

chave_mes = f"{ano}-{mes:02d}"
feriados = feriados_ano(ano)

matriz = gerar_matriz_mes(ano, mes)

st.markdown(f"<div style='margin: 0.2rem 0;'><strong style='font-size: 0.85rem;'>Calendário {chave_mes}</strong></div>", unsafe_allow_html=True)
weekday_labels = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
cols = st.columns(7, gap="small")
for i, lbl in enumerate(weekday_labels):
    cols[i].markdown(f"<div style='font-size: 0.75rem; text-align: center;'><strong>{lbl}</strong></div>", unsafe_allow_html=True)

# ---------- DESENHO DO CALENDÁRIO COM TOGGLE ----------

for week in matriz:
    cols = st.columns(7, gap="small")
    for i, d in enumerate(week):
        if d.month != mes:
            cols[i].markdown(" ")
            continue

        key_dia = d.isoformat()
        if key_dia not in st.session_state.dias_estado:
            st.session_state.dias_estado[key_dia] = "none"

        is_holiday = d in feriados

        # callback de toggle
        def make_on_click(data_key):
            def _toggle():
                atual = st.session_state.dias_estado[data_key]
                st.session_state.dias_estado[data_key] = proximo_estado(atual)
            return _toggle

        cols[i].button(
            label=str(d.day),
            key=f"btn_{key_dia}",
            on_click=make_on_click(key_dia)
        )

        # cor da faixa inferior
        if is_holiday:
            bg = CORES["feriado"]
        else:
            bg = CORES[st.session_state.dias_estado[key_dia]]

        cols[i].markdown(
            f"<div style='margin-top:-5px; height:12px; "
            f"border:1px solid #CCC; background-color:{bg};'></div>",
            unsafe_allow_html=True
        )

# ---------- LEGENDA ----------

st.markdown(
    "<div style='font-size:0.75rem; margin: 0.2rem 0;'><span style='display:inline-block;width:12px;height:8px;border:1px solid #CCC;background:#00C853;'></span> Pres &nbsp; <span style='display:inline-block;width:12px;height:8px;border:1px solid #CCC;background:#FF5252;'></span> Férias &nbsp; <span style='display:inline-block;width:12px;height:8px;border:1px solid #CCC;background:#2979FF;'></span> Feriado</div>",
    unsafe_allow_html=True
)

# ---------- CÁLCULO RESUMO ----------

# dias úteis brutos (segunda a sexta, excluindo feriados)
dias_uteis_brutos = []
_, last_day = calendar.monthrange(ano, mes)
for dia in range(1, last_day + 1):
    d = dt.date(ano, mes, dia)
    if d.weekday() < 5 and d not in feriados:
        dias_uteis_brutos.append(d)

# base de dias úteis ajustada (tira dias marcados como férias)
dias_base = [
    d for d in dias_uteis_brutos
    if st.session_state.dias_estado.get(d.isoformat(), "none") != "ferias"
]
total_base = len(dias_base)

# presenças
dias_presenca = [
    d for d in dias_base
    if st.session_state.dias_estado.get(d.isoformat(), "none") == "presenca"
]
total_presenca = len(dias_presenca)

percentual = (total_presenca / total_base * 100) if total_base > 0 else 0
meta_minima = int(total_base * 0.6)  # arredonda para baixo

st.markdown("<div style='margin-top:0.3rem;'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom: 0.2rem; margin-top: 0rem; font-size: 1rem;'>Resumo</h3>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4, gap="small")
c1.metric("Base", total_base)
c2.metric("Presença", total_presenca)
c3.metric("%", f"{percentual:.0f}%")
c4.metric("Meta", meta_minima)

if total_presenca >= meta_minima:
    st.success("Meta de 60% ATINGIDA ✅")
else:
    faltam = meta_minima - total_presenca
    st.warning(f"Meta NÃO atingida. Faltam aproximadamente {max(faltam,0)} dia(s).")

# ---------- SALVAR ----------

if st.button("Salvar tudo em JSON"):
    salvar_json(st.session_state.dias_estado)
    st.success(f"Dados salvos em {ARQUIVO.name}.")
