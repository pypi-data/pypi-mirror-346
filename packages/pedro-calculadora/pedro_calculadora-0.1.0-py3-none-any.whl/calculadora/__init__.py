def adicionar(x, y):
    """Adiciona dois números."""
    return x + y

def subtrair(x, y):
    """Subtrai dois números."""
    return x - y

def multiplicar(x, y):
    """Multiplica dois números."""
    return x * y

def dividir(x, y):
    """Divide dois números. Retorna erro se o divisor for zero."""
    if y == 0:
        return "Erro! Divisão por zero."
    return x / y


while True:
    print("\nSelecione a operação:")
    print("1. Adição")
    print("2. Subtração")
    print("3. Multiplicação")
    print("4. Divisão")
    print("5. Sair")

    escolha = input("Digite sua escolha (1/2/3/4/5): ")

    if escolha in ('1', '2', '3', '4'):
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
        except ValueError:
            print("Entrada inválida. Por favor, digite números.")
            continue

        if escolha == '1':
            print(num1, "+", num2, "=", adicionar(num1, num2))

        elif escolha == '2':
            print(num1, "-", num2, "=", subtrair(num1, num2))

        elif escolha == '3':
            print(num1, "*", num2, "=", multiplicar(num1, num2))

        elif escolha == '4':
            resultado = dividir(num1, num2)
            print(num1, "/", num2, "=", resultado)

    elif escolha == '5':
        print("Saindo da calculadora.")
        break

    else:
        print("Escolha inválida. Por favor, tente novamente.")
