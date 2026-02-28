import datetime as dt
import holidays

ano = 2026
br = holidays.country_holidays("BR")
feriados_2026 = {d for d in br if d.year == ano}

print("Qtd 2026:", len(feriados_2026))
print("Tem 2026-01-01?", dt.date(2026,1,1) in feriados_2026)
for d, nome in sorted(br.items()):
    if d.year == ano:
        print("Primeiro feriado 2026:", d, nome)
        break
