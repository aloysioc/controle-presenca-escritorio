"""
Módulo para calcular feriados do Brasil (fixos e móveis)
Combina: biblioteca 'holidays' + algoritmo de Meeus para datas móveis
"""

import holidays
import datetime as dt
from typing import Set, Dict

def calcular_pascoa(ano: int) -> dt.date:
    """
    Calcula a data da Páscoa usando o algoritmo de Meeus.
    Funciona para qualquer ano gregoriano (após 1582).
    
    Args:
        ano: Ano para o qual calcular a Páscoa
        
    Returns:
        Data da Páscoa
    """
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(ano, mes, dia)


def feriados_brasil(ano: int, state: str = 'SP', include_moveis: bool = True) -> Dict[dt.date, str]:
    """
    Retorna dicionário de feriados do Brasil (fixos e opcionalmente móveis).
    
    Args:
        ano: Ano para o qual calcular feriados
        state: Estado brasileiro ('SP', 'RJ', etc.) - padrão 'SP'
        include_moveis: Se True, inclui feriados móveis (Carnaval, Corpus Christi, etc)
        
    Returns:
        Dicionário {data: descrição}
    """
    
    # Feriados fixos via holidays
    feriados = dict(holidays.Brazil(state=state, years=ano))
    
    if include_moveis:
        # Calcula Páscoa e datas derivadas
        pascoa = calcular_pascoa(ano)
        
        # Datas móveis derivadas da Páscoa
        datas_moveis = {
            pascoa - dt.timedelta(days=47): "Carnaval",
            pascoa - dt.timedelta(days=46): "Carnaval",  # Segunda de Carnaval
            pascoa - dt.timedelta(days=2): "Sexta-feira Santa",  # Se não estiver já em holidays
            pascoa + dt.timedelta(days=60): "Corpus Christi",
        }
        
        # Adiciona apenas se não existem nos feriados fixos
        for data, descricao in datas_moveis.items():
            if data not in feriados:
                feriados[data] = descricao
    
    return feriados


def eh_feriado(data: dt.date, state: str = 'SP', include_moveis: bool = True) -> bool:
    """
    Verifica se uma data é feriado.
    
    Args:
        data: Data a verificar
        state: Estado ('SP', 'RJ', etc.)
        include_moveis: Se True, inclui feriados móveis
        
    Returns:
        True se é feriado, False caso contrário
    """
    feriados = feriados_brasil(data.year, state=state, include_moveis=include_moveis)
    return data in feriados


def get_descricao_feriado(data: dt.date, state: str = 'SP', include_moveis: bool = True) -> str:
    """
    Retorna a descrição de um feriado.
    
    Args:
        data: Data a verificar
        state: Estado ('SP', 'RJ', etc.)
        include_moveis: Se True, inclui feriados móveis
        
    Returns:
        Descrição do feriado ou string vazia se não for feriado
    """
    feriados = feriados_brasil(data.year, state=state, include_moveis=include_moveis)
    return feriados.get(data, "")


if __name__ == "__main__":
    # Teste rápido
    print("TESTE - Feriados Brasil 2026 (SP) com datas móveis:")
    print("=" * 60)
    
    feriados_2026 = feriados_brasil(2026, state='SP', include_moveis=True)
    
    for data in sorted(feriados_2026.keys()):
        print(f"{data.strftime('%d/%m/%Y (%a)')}: {feriados_2026[data]}")
    
    print("\n" + "=" * 60)
    print(f"Total: {len(feriados_2026)} feriados")
