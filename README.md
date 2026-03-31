# Controle de Presença no Escritório (60%)

Aplicação Streamlit para controle de presença no escritório com cálculo automático da meta de 60% de presença mensal, considerando feriados nacionais, estaduais e datas móveis.

## 📋 Funcionalidades

### Calendário Interativo
- 📅 Visualização de calendário mensal (inicia no domingo)
- ✅ Marcação de dias de presença no escritório (verde)
- 🏖️ Marcação de férias (vermelho)
- 🎉 Feriados automáticos (azul) com tooltip ao passar o mouse

### Feriados Inteligentes
- 🇧🇷 **Feriados nacionais do Brasil** (automáticos via biblioteca `holidays`)
- 🏛️ **Feriados estaduais** (configurável - padrão: SP)
- 📆 **Datas móveis calculadas automaticamente**:
  - Carnaval (47 dias antes da Páscoa)
  - Sexta-feira Santa (2 dias antes da Páscoa)
  - Corpus Christi (60 dias após a Páscoa)
- 🌍 **Tooltip em português** ao passar o mouse sobre feriados

### Cálculos Automáticos
- 📊 Contador de dias úteis base do mês (seg-sex, excluindo feriados e férias)
- ✅ Total de presenças marcadas
- 📈 Percentual de presença atingido
- 🎯 Meta mínima de 60% calculada automaticamente
- ⚠️ Alertas de meta atingida ou não atingida

### Persistência de Dados
- 💾 Salvamento manual em JSON
- 📂 Arquivo: `presencas_calendario.json`
- ♻️ Carregamento automático ao iniciar

## 🚀 Como usar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:
```bash
pip install streamlit holidays
```

### 2. Execute a aplicação

```bash
streamlit run controle_escritorio.py
```

### 3. Acesse no navegador

A aplicação abrirá automaticamente em: `http://localhost:8501`

### 4. Como usar o calendário

1. **Selecione o ano e mês** nos campos superiores
2. **Clique nos dias** para alternar entre:
   - Branco (sem marcação)
   - Verde (presença)
   - Vermelho (férias)
3. **Feriados aparecem automaticamente em azul** (não clicáveis)
4. **Passe o mouse sobre feriados** para ver o nome em português
5. **Verifique o resumo** no final da página
6. **Clique em "Salvar tudo em JSON"** para persistir os dados

## ⚙️ Configuração

### Alterar o Estado (para feriados estaduais)

Edite o arquivo `controle_escritorio.py` na linha 11:

```python
ESTADO = "SP"  # Altere para: "RJ", "MG", "BA", etc.
```

Estados suportados: SP, RJ, MG, ES, BA, RS, PR, SC, e outros.

### Personalizar cores

Edite o dicionário `CORES` no arquivo `controle_escritorio.py` (linhas 13-17):

```python
CORES = {
    "none": "#FFFFFF",     # sem marcação
    "presenca": "#00C853", # verde vivo
    "ferias": "#FF5252",   # vermelho vivo
    "feriado": "#2979FF",  # azul vivo
}
```

## 📁 Estrutura do Projeto

```
calendario/
├── controle_escritorio.py      # Aplicação principal Streamlit
├── feriados_brasil.py          # Módulo de cálculo de feriados
├── presencas_calendario.json   # Dados persistidos (criado automaticamente)
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
└── teste_*.py                  # Arquivos de teste
```

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework para aplicações web em Python
- **[holidays](https://pypi.org/project/holidays/)** - Biblioteca de feriados internacionais
- **Python 3.8+** - Linguagem de programação

## 📐 Algoritmos Especiais

### Cálculo da Páscoa (Algoritmo de Meeus)

O projeto implementa o algoritmo de Meeus para calcular a Páscoa gregoriana, usado como base para datas móveis:

- **Carnaval**: Páscoa - 47 dias
- **Sexta-feira Santa**: Páscoa - 2 dias  
- **Corpus Christi**: Páscoa + 60 dias

Este algoritmo funciona para qualquer ano gregoriano (após 1582).

### Cálculo de Dias Úteis

A aplicação considera dias úteis apenas:
- Segunda a sexta-feira
- Excluindo feriados nacionais/estaduais
- Excluindo dias marcados como férias

## 📊 Arquivo de Dados

O arquivo `presencas_calendario.json` armazena os estados dos dias no formato:

```json
{
  "2026-02-03": "presenca",
  "2026-02-10": "ferias",
  "2026-02-17": "none"
}
```

- `presenca`: Dia de presença no escritório
- `ferias`: Dia de férias
- `none`: Sem marcação (padrão)

## 🤝 Contribuições

Este projeto foi desenvolvido com assistência de IA (GitHub Copilot) e está disponível para melhorias e personalizações.

## 📄 Licença

Projeto pessoal de uso livre.

## 🔄 Histórico de Versões

- **v1.0** - Versão inicial com calendário básico e feriados hardcoded
- **v2.0** - Integração com biblioteca `holidays` e cálculo de datas móveis
- **v2.1** - Otimização de layout e remoção de Quarta de Cinzas
- **v2.2** - Tooltips em português para feriados

---

Desenvolvido com ❤️ para controle de presença híbrida no escritório
# Setup rapido no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run controle_escritorio.py
```

O arquivo `calendario.bat` tambem pode ser usado para abrir o app e agora procura automaticamente por `.\.venv\Scripts\python.exe`, `py -3` ou `python`.

## Registro de ambiente

Em `2026-03-31`, nesta maquina de trabalho, o ambiente local foi recriado para acompanhar o ambiente atualizado da maquina pessoal.

Passos executados:

```powershell
rmdir /s /q .venv
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Resultado confirmado:
- `.venv` recriado com sucesso
- dependencias instaladas a partir de `requirements.txt`
- `calendario.bat` validado com sucesso nesta maquina

Observacao operacional:
- durante a automacao assistida, houve bloqueio de permissao no diretorio temporario do Windows ao rodar `ensurepip` e `pip` dentro da sandbox
- fora da sandbox, a recriacao do ambiente e a instalacao funcionaram normalmente
- para futuras trocas de maquina, este foi o procedimento que deu certo e deve ser repetido primeiro
