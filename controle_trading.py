import streamlit as st
import json
import datetime
from pathlib import Path

# ---------- CONFIGURAÇÃO ----------

ARQUIVO = Path("trading_lotes.json")

ATIVOS_INICIAIS = [
    {"tipo": "Ativo",  "nome": "SP-JUN26",               "lotes_iniciais": 42},
    {"tipo": "Ativo",  "nome": "NSDQ-JUN26",             "lotes_iniciais": 46},
    {"tipo": "Ativo",  "nome": "DOW-JUN26",              "lotes_iniciais": 78},
    {"tipo": "Ativo",  "nome": "DAX-JUN26",              "lotes_iniciais": 79},
    {"tipo": "Ativo",  "nome": "BRENT CRUDE OIL",        "lotes_iniciais": 89},
    {"tipo": "Ativo",  "nome": "CL SWEET CRUDE OIL",     "lotes_iniciais": 94},
    {"tipo": "Ação",   "nome": "DHR – DANAHER CORPORATION",          "lotes_iniciais": 18},
    {"tipo": "Ação",   "nome": "NETFLIX – NETFLIX INC",              "lotes_iniciais": 17},
    {"tipo": "Ação",   "nome": "ISRG – INTUITIVE SURGICAL INC",      "lotes_iniciais": 20},
    {"tipo": "Ação",   "nome": "AMD – ADVANCED MICRO DEVICES INC",   "lotes_iniciais": 1},
]

# ---------- PERSISTÊNCIA ----------

def carregar_dados() -> dict:
    if ARQUIVO.exists():
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"registros": []}


def salvar_dados(dados: dict) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# ---------- LÓGICA ----------

def lotes_usados_por_ativo(registros: list) -> dict:
    """Retorna {nome_ativo: total_lotes_usados}."""
    totais: dict = {}
    for r in registros:
        totais[r["ativo"]] = totais.get(r["ativo"], 0) + r["lotes"]
    return totais


def montar_tabela(registros: list) -> list[dict]:
    totais = lotes_usados_por_ativo(registros)
    linhas = []
    for a in ATIVOS_INICIAIS:
        usados = totais.get(a["nome"], 0)
        restantes = a["lotes_iniciais"] - usados
        linhas.append({
            "Tipo":            a["tipo"],
            "Ativo / Ação":    a["nome"],
            "Lotes Iniciais":  a["lotes_iniciais"],
            "Lotes Usados":    usados,
            "Lotes Restantes": restantes,
        })
    return linhas


# ---------- UI ----------

st.set_page_config(page_title="Controle de Lotes — Trading", layout="wide")
st.title("📊 Controle de Lotes — Trading")

dados = carregar_dados()

# ---- Painel de resumo ----
st.subheader("Resumo de Lotes")

tabela = montar_tabela(dados["registros"])

def formatar_linha(linha: dict) -> dict:
    """Aplica formatação visual aos lotes restantes."""
    restantes = linha["Lotes Restantes"]
    if restantes <= 0:
        emoji = "🔴"
    elif restantes <= linha["Lotes Iniciais"] * 0.25:
        emoji = "🟡"
    else:
        emoji = "🟢"
    return {**linha, "Status": f"{emoji} {restantes}"}

linhas_formatadas = [formatar_linha(l) for l in tabela]

col_ativos, col_acoes = st.columns(2)

with col_ativos:
    st.markdown("### Ativos")
    ativos = [l for l in linhas_formatadas if l["Tipo"] == "Ativo"]
    st.table(
        [{k: v for k, v in l.items() if k not in ("Tipo",)} for l in ativos]
    )

with col_acoes:
    st.markdown("### Ações")
    acoes = [l for l in linhas_formatadas if l["Tipo"] == "Ação"]
    st.table(
        [{k: v for k, v in l.items() if k not in ("Tipo",)} for l in acoes]
    )

st.divider()

# ---- Formulário para registrar uso ----
st.subheader("Registrar Uso de Lotes")

nomes_ativos = [a["nome"] for a in ATIVOS_INICIAIS]

with st.form("form_uso", clear_on_submit=True):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        data_uso = st.date_input("Data", value=datetime.date.today())
    with col2:
        ativo_sel = st.selectbox("Ativo / Ação", nomes_ativos)
    with col3:
        qtd = st.number_input("Lotes utilizados", min_value=1, step=1, value=1)

    obs = st.text_input("Observação (opcional)", max_chars=200)

    submitted = st.form_submit_button("✅ Registrar")

    if submitted:
        # Validar disponibilidade
        totais = lotes_usados_por_ativo(dados["registros"])
        inicial = next(a["lotes_iniciais"] for a in ATIVOS_INICIAIS if a["nome"] == ativo_sel)
        usados_ate_agora = totais.get(ativo_sel, 0)
        if qtd > (inicial - usados_ate_agora):
            st.error(
                f"❌ Não há lotes suficientes para **{ativo_sel}**. "
                f"Restantes: {inicial - usados_ate_agora}."
            )
        else:
            dados["registros"].append({
                "id":    len(dados["registros"]) + 1,
                "data":  str(data_uso),
                "ativo": ativo_sel,
                "lotes": int(qtd),
                "obs":   obs.strip(),
            })
            salvar_dados(dados)
            st.success(f"✅ {int(qtd)} lote(s) de **{ativo_sel}** registrados em {data_uso}.")
            st.rerun()

st.divider()

# ---- Histórico de registros ----
st.subheader("Histórico de Registros")

if not dados["registros"]:
    st.info("Nenhum registro ainda.")
else:
    # Exibe em ordem decrescente de id
    registros_desc = sorted(dados["registros"], key=lambda r: r["id"], reverse=True)

    for reg in registros_desc:
        col_d, col_a, col_l, col_o, col_x = st.columns([1.5, 3, 1, 3, 0.7])
        col_d.write(reg["data"])
        col_a.write(reg["ativo"])
        col_l.write(reg["lotes"])
        col_o.write(reg.get("obs", ""))
        if col_x.button("🗑️", key=f"del_{reg['id']}"):
            dados["registros"] = [r for r in dados["registros"] if r["id"] != reg["id"]]
            salvar_dados(dados)
            st.rerun()
