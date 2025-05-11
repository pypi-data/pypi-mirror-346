# poetry add -- dodanie zalkeżności i zainstalowanie jej w venv
# poetry run python skrypt - do uruchomienia skryptu pythona
# poetry build - do zbudowania pakietu dystrybucyjnego (dla repozytorium pypi)
# poetry publish - do wysłania pakietów do pypi

from pymsgbox import prompt, alert

def calculate(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a*b
    else:
        return a/b

def main():
    x = prompt("podaj pierwsza liczbe:")
    y = prompt("podaj druga liczbe:")
    op = prompt("wybierz dzialanie (+-*/):")

    result = calculate(float(x), float(y), op)

    alert(f"wynik: {result}")


if __name__ == '__main__':
    main()
