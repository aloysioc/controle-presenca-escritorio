"""
Script de teste para a biblioteca 'holidays'
Testando feriados nacionais do Brasil e estaduais de SP
"""

import holidays
import datetime as dt

print("=" * 60)
print("TESTANDO BIBLIOTECA HOLIDAYS - BRASIL")
print("=" * 60)

# 1. Feriados nacionais do Brasil em 2026
print("\n1. FERIADOS NACIONAIS DO BRASIL (2026):")
print("-" * 60)
feriados_br = holidays.Brazil(years=2026)
for data, descricao in sorted(feriados_br.items()):
    print(f"{data.strftime('%d/%m/%Y (%A)')}: {descricao}")

# 2. Feriados do estado de SP em 2026
print("\n2. FERIADOS DO ESTADO DE SÃO PAULO (2026):")
print("-" * 60)
feriados_sp = holidays.Brazil(state='SP', years=2026)
for data, descricao in sorted(feriados_sp.items()):
    print(f"{data.strftime('%d/%m/%Y (%A)')}: {descricao}")

# 3. Verificar datas específicas
print("\n3. VERIFICAÇÃO DE DATAS ESPECÍFICAS:")
print("-" * 60)
datas_verificar = [
    dt.date(2026, 12, 25),  # Natal
    dt.date(2026, 2, 17),   # Carnaval
    dt.date(2026, 4, 21),   # Tiradentes
    dt.date(2026, 3, 15),   # Dia aleatório (não é feriado)
]

for data in datas_verificar:
    eh_feriado = data in feriados_sp
    descricao = feriados_sp.get(data, "Não é feriado")
    status = "✓ FERIADO" if eh_feriado else "✗ dia útil"
    print(f"{data.strftime('%d/%m/%Y')}: {status} - {descricao}")

# 4. Comparar feriados nacionais vs estaduais
print("\n4. DIFERENÇAS ENTRE NACIONAL E SP:")
print("-" * 60)
apenas_sp = set(feriados_sp.items()) - set(feriados_br.items())
if apenas_sp:
    print("Feriados específicos de SP (não nacionais):")
    for data, descricao in sorted(apenas_sp):
        print(f"  → {data.strftime('%d/%m/%Y')}: {descricao}")
else:
    print("Sem feriados adicionais específicos de SP em 2026")

# 5. Testar múltiplos anos
print("\n5. FERIADOS DE CARNAVAL (2024-2027):")
print("-" * 60)
for ano in range(2024, 2028):
    feriados = holidays.Brazil(years=ano)
    # Procurando por Carnaval
    for data, descricao in sorted(feriados.items()):
        if 'Carnaval' in descricao or 'carnaval' in descricao.lower():
            print(f"{ano}: {data.strftime('%d/%m/%Y')} - {descricao}")
            break

print("\n" + "=" * 60)
print("FIM DO TESTE")
print("=" * 60)
