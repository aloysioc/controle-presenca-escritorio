# Changelog - Controle de Presença

Histórico detalhado de mudanças e melhorias implementadas no projeto.

## [2.3.1] - 2026-03-31

### 📝 Documentacao
- Registrado no `README.md` o procedimento usado para sincronizar o ambiente desta maquina com a maquina pessoal
- Documentado que a recriacao local do `.venv` e a reinstalacao via `requirements.txt` funcionaram corretamente
- Registrado que o `calendario.bat` foi validado com sucesso nesta maquina

### 🔧 Operacional
- Anotado o comportamento observado durante a automacao assistida: bloqueio de permissao no diretorio temporario do Windows ao usar `ensurepip` e `pip` dentro da sandbox
- Definido no historico do projeto que, em futuras mudancas de maquina, o primeiro passo recomendado e recriar o `.venv` e reinstalar as dependencias
## [2.3.0] - 2026-03-31

### 🐛 Corrigido
- **Clique nos dias voltou a funcionar** mesmo quando o calendário foi inicializado com dados vindos do `presencas_calendario.json`
- Estado do calendário não é mais sobrescrito pelo JSON a cada rerun do Streamlit

### ✨ Alterado
- **Salvamento automático** ao alternar o status de um dia
- Removido o botão "Salvar tudo em JSON", que ficou desnecessário
- Adicionado `calendario.bat` para iniciar o app Streamlit com mais facilidade

### 📝 Técnico
- Criada a função `hidratar_estado_inicial()` para carregar o JSON apenas uma vez por sessão
- Callback de toggle passou a persistir o estado imediatamente no arquivo JSON

## [2.2.0] - 2026-03-02

### ✨ Adicionado
- **Tooltip em português** ao passar o mouse sobre feriados
- Dicionário de tradução de feriados (inglês → português BR)
- Cursor especial (help) ao passar sobre feriados
- Documentação completa no README.md

### 📝 Técnico
- Função `traduzir_feriado()` para conversão automática
- Atributo HTML `title` nas barras de feriados
- Dicionário `TRADUCOES_FERIADOS` com 14 feriados traduzidos

## [2.1.0] - 2026-02-28

### 🐛 Corrigido
- **Removida Quarta de Cinzas** (18/02) como feriado
- Apenas Carnaval (17/02) permanece como feriado móvel
- Total de feriados em 2026 (SP): 13 feriados

### 🎨 Interface
- **Calendário inicia no domingo** (padrão brasileiro)
- Ordem das colunas: Dom → Seg → Ter → Qua → Qui → Sex → Sáb
- Otimização de espaços verticais para evitar scroll
- Título reduzido: "Controle de presença 60%"
- CSS customizado para compactação de layout

### 🔧 Refatorações
- Removido import não utilizado (`eh_feriado`)
- Configuração do ambiente Python no VS Code (Pylance)

## [2.0.0] - 2026-02-28

### 🎉 Melhorias Principais
- **Integração com biblioteca `holidays`** (substituiu hardcoding)
- **Cálculo automático de datas móveis**:
  - Carnaval (47 dias antes da Páscoa)
  - Corpus Christi (60 dias após a Páscoa)
  - Sexta-feira Santa (2 dias antes da Páscoa)
- Suporte a **feriados estaduais** (SP por padrão)
- Funciona para **qualquer ano** (não apenas 2026)

### 📦 Novo Módulo
- Criado `feriados_brasil.py`:
  - Algoritmo de Meeus para cálculo da Páscoa
  - Função `feriados_brasil(ano, state, include_moveis)`
  - Função `calcular_pascoa(ano)`
  - Suporte a múltiplos estados brasileiros

### 📄 Documentação
- Adicionado `requirements.txt`
- Criados arquivos de teste:
  - `teste_holidays.py`
  - `teste_datas_moveis.py`
  - `feriados_brasil.py` com testes integrados

## [1.0.0] - 2026-02-28

### 🚀 Versão Inicial (criada por Perplexity)
- Calendário mensal interativo com Streamlit
- Marcação manual de presença (verde)
- Marcação manual de férias (vermelho)
- Feriados hardcoded para 2026
- Cálculo de meta 60% de presença
- Contador de dias úteis
- Persistência em JSON (`presencas_calendario.json`)
- Callback de toggle para alternar estados dos dias

### 📊 Funcionalidades Base
- Seleção de ano/mês
- Calendário iniciando na segunda-feira
- 3 estados por dia: none, presença, férias
- Exclusão automática de finais de semana
- Resumo mensal com métricas
- Botão "Salvar tudo em JSON"

### 🔧 Configuração
- Arquivo `ARQUIVO = Path("presencas_calendario.json")`
- Cores personalizáveis no dicionário `CORES`
- Feriados manuais para 2026 (12 datas fixas)

---

## Repositório GitHub

🔗 https://github.com/aloysioc/controle-presenca-escritorio

### Commits Principais
- `c78261d` - Docs: Expandir README com documentação completa
- `98a76d9` - Feat: Adicionar tooltip com nome do feriado em português
- `3ea3e5d` - Revert: Voltar tamanho de fontes anterior
- `664b9da` - Fix: Remover Quarta de Cinzas + Domingo como primeiro dia
- `2af0f09` - Feat: Calcular feriados dinamicamente incluindo datas móveis
- `aa187c9` - Initial commit: Controle de presença no escritório

---

## Créditos

- **Versão inicial**: Perplexity AI
- **Refatorações e melhorias**: GitHub Copilot (Claude Sonnet 4.5)
- **Desenvolvedor**: @aloysioc
