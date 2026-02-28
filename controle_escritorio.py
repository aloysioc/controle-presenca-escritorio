import streamlit as st
import datetime as dt
import calendar
import json
from pathlib import Path
from feriados_brasil import feriados_brasil, eh_feriado

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

st.set_page_config("Controle Escritório – Calendário", layout="centered")
st.title("Controle de presença no escritório – visão tipo calendário")

# Carrega dados já salvos em disco
dados_salvos = carregar_json()

if "dias_estado" not in st.session_state:
    st.session_state.dias_estado = {}

# Hidrata o session_state com o que veio do JSON
for data_str, estado in dados_salvos.items():
    st.session_state.dias_estado[data_str] = estado

col1, col2 = st.columns(2)
with col1:
    ano = st.number_input("Ano", min_value=2024, max_value=2030,
                          value=2026, step=1)
with col2:
    mes = st.selectbox(
        "Mês",
        options=list(range(1, 13)),
        format_func=lambda m: [
            "Jan","Fev","Mar","Abr","Mai","Jun",
            "Jul","Ago","Set","Out","Nov","Dez"
        ][m-1],
        index=1  # 0=Jan, 1=Fev...
    )

chave_mes = f"{ano}-{mes:02d}"
feriados = feriados_ano(ano)

matriz = gerar_matriz_mes(ano, mes)

st.subheader(f"Calendário {chave_mes}")
weekday_labels = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
cols = st.columns(7)
for i, lbl in enumerate(weekday_labels):
    cols[i].markdown(f"**{lbl}**")

# ---------- DESENHO DO CALENDÁRIO COM TOGGLE ----------

for week in matriz:
    cols = st.columns(7)
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
    """
    <div style="margin-top:10px; margin-bottom:10px;">
      <span style="display:inline-block;width:18px;height:12px;border:1px solid #CCC;background-color:#00C853;"></span>
      &nbsp;Presença&nbsp;&nbsp;
      <span style="display:inline-block;width:18px;height:12px;border:1px solid #CCC;background-color:#FF5252;"></span>
      &nbsp;Férias&nbsp;&nbsp;
      <span style="display:inline-block;width:18px;height:12px;border:1px solid #CCC;background-color:#2979FF;"></span>
      &nbsp;Feriado
    </div>
    """,
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

st.markdown("---")
st.subheader("Resumo do mês")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Dias úteis base", total_base)
c2.metric("Presenças", total_presenca)
c3.metric("% atingido", f"{percentual:.1f}%")
c4.metric("Meta mínima (60%)", meta_minima)

if total_presenca >= meta_minima:
    st.success("Meta de 60% ATINGIDA ✅")
else:
    faltam = meta_minima - total_presenca
    st.warning(f"Meta NÃO atingida. Faltam aproximadamente {max(faltam,0)} dia(s).")

# ---------- SALVAR ----------

if st.button("Salvar tudo em JSON"):
    salvar_json(st.session_state.dias_estado)
    st.success(f"Dados salvos em {ARQUIVO.name}.")
