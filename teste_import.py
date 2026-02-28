import holidays
import inspect
import sys

print("Módulo holidays:", holidays)
print("Arquivo:", holidays.__file__)
print("Dir:", dir(holidays)[:40])
print("Versão via pkg_resources (se existir):")
try:
    import pkg_resources
    print(pkg_resources.get_distribution("holidays").version)
except Exception as e:
    print("Erro ao pegar versão:", e)

print("sys.path:")
for p in sys.path:
    print("  ", p)
