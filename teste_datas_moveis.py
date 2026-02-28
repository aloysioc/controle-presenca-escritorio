"""
Script para testar cálculo de datas móveis (Carnaval, Páscoa, etc)
Testando diferentes abordagens
"""

import holidays
import datetime as dt

print("=" * 70)
print("TESTANDO DATAS MÓVEIS - BRASIL")
print("=" * 70)

# 1. Testa se a biblioteca holidays tem Carnaval para Brasil
print("\n1. VERIFICANDO HOLIDAYS COM INCLUDE_HOLIDAYS:")
print("-" * 70)

# Testa com parâmetro include_holidays
try:
    feriados_br = holidays.Brazil(years=2026, include_holidays=['Carnival'])
    print("Tentativa com include_holidays=['Carnival']:")
    for data, descricao in sorted(feriados_br.items()):
        if 'Carnival' in descricao or 'Carnaval' in descricao:
            print(f"  {data.strftime('%d/%m/%Y')}: {descricao}")
except Exception as e:
    print(f"  Erro: {e}")

# 2. Tenta com workalendar (biblioteca específica para calendários de trabalho)
print("\n2. TESTANDO WORKALENDAR (Brasil):")
print("-" * 70)

try:
    from workalendar.america import Brazil as BrazilCal
    
    cal = BrazilCal()
    holidays_list = cal.holidays(2026)
    
    print("Feriados do Brasil (2026) com workalendar:")
    for data, descricao in sorted(holidays_list):
        print(f"  {data.strftime('%d/%m/%Y')}: {descricao}")
        
except ImportError:
    print("  Biblioteca 'workalendar' não está instalada.")
    print("  Precisa instalar: pip install workalendar")

# 3. Tenta com workalendar para SP
print("\n3. TESTANDO WORKALENDAR (São Paulo):")
print("-" * 70)

try:
    from workalendar.america import SaoPaulo
    
    cal = SaoPaulo()
    holidays_list = cal.holidays(2026)
    
    print("Feriados de SP (2026) com workalendar:")
    for data, descricao in sorted(holidays_list):
        print(f"  {data.strftime('%d/%m/%Y')}: {descricao}")
        
except ImportError as e:
    print(f"  Erro ao importar workalendar: {e}")

# 4. Cálculo manual da Páscoa (para calcular Carnaval e Corpus Christi)
print("\n4. CÁLCULO MANUAL - PÁSCOA E DATAS DERIVADAS:")
print("-" * 70)

def calcular_pascoa(ano):
    """
    Algoritmo de Meeus para calcular Páscoa
    Funciona para qualquer ano gregoriano
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

ano = 2026
pascoa = calcular_pascoa(ano)
carnaval = pascoa - dt.timedelta(days=47)  # 47 dias antes da Páscoa
corpus_christi = pascoa + dt.timedelta(days=60)  # 60 dias depois da Páscoa
sexta_feira_santa = pascoa - dt.timedelta(days=2)

print(f"Ano: {ano}")
print(f"  Páscoa: {pascoa.strftime('%d/%m/%Y')}")
print(f"  Sexta-feira Santa: {sexta_feira_santa.strftime('%d/%m/%Y')}")
print(f"  Carnaval: {carnaval.strftime('%d/%m/%Y')}")
print(f"  Corpus Christi: {corpus_christi.strftime('%d/%m/%Y')}")

print("\n" + "=" * 70)
print("FIM DO TESTE")
print("=" * 70)
