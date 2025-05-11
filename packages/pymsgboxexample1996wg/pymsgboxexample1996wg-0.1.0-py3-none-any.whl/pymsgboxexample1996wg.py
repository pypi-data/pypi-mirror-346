# poetry add -- dodanie zależności i zainstalowanie jej w venv
# poetry run python skrypt - do uruchamiania skryptu pythona
# poetry build - do zbudowania pakietu dystrybucyjnego (dla repo pypi)
# poetry publish - do wyslania pakietów pypi


from pymsgbox import alert, prompt

def calculate(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    else:
        return a / b



def main():
    x = prompt("Podaj pierwszą liczbę: ")
    y = prompt("Podaj pierwszą liczbę: ")
    op = prompt("Wybierz działanie (+ - * /): ")

    result = calculate(float(x), float(y), op)
    prompt(f"Wynik: {result}")



if __name__ == '__main__':
    main()