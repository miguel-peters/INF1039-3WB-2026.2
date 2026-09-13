def painel_principal () :

  print("Escolha a operação desejada:")
  print("1 - Soma")
  print("2 - Subtração")
  print("3 - Multiplicação")
  print("4 - Divisão")
  print("5 - Exponenciação")
  print("6 - Radiciação")
  print("7 - Resto da divisão")
  print("8 - Percentual")
  print("0 - Sair do Programa")

  escolha = input("Digite o número da operação desejada: ")
  return escolha

def calcula_soma(x, y):
  return x + y

def calcula_subtracao(a,b):
    return a-b

def calcula_radiciacao(a,b):
    resp = a**(1/b)
    return resp

def calcula_resto(x, y):
  return x % y

def calcula_percentual(x, y):
  return (x / y) * 100

def calcula_multiplicacao(a, b):
    return a * b

def calcula_exponenciacao(a, b):
    return a ** b  

escolha = painel_principal()

if escolha == "1":
    x = float(input("Digite o primeiro número: "))
    y = float(input("Digite o segundo número: "))
    resultado = calcula_soma(x, y)
    print(f"O resultado da soma é: {resultado}")

elif escolha == "2":
    a = float(input("Digite o primeiro número: "))
    b = float(input("Digite o segundo número: "))
    resultado = calcula_subtracao(a, b)
    print(f"O resultado da subtração é: {resultado}")

elif escolha == "3": 
    a = float(input("Digite o primeiro número: "))
    b = float(input("Digite o segundo número: "))
    resultado = calcula_multiplicacao(a, b)
    print(f"O resultado da multiplicação é: {resultado}")

elif escolha == "4":
    a = float(input("Digite o primeiro número: "))
    b = float(input("Digite o segundo número: "))
    resultado = calcula_divisao(a, b)
    print(f"O resultado da divisão é: {resultado}")

elif escolha == "5":
    a = float(input("Digite o primeiro número: "))
    b = float(input("Digite o segundo número: "))
    resultado = calcula_exponenciacao(a, b)
    print(f"O resultado da exponenciação é: {resultado}")   

elif escolha == "6":
    a = float(input("Digite o número: "))
    b = float(input("Digite o índice da raiz: "))
    resultado = calcula_radiciacao(a, b)
    print(f"O resultado da radiciação é: {resultado}")

elif escolha == "7":
    x = float(input("Digite o dividendo: "))
    y = float(input("Digite o divisor: "))
    resultado = calcula_resto(x, y)
    print(f"O resultado do resto da divisão é: {resultado}")

elif escolha == "8":
    x = float(input("Digite o valor: "))
    y = float(input("Digite o total: "))
    resultado = calcula_percentual(x, y)
    print(f"O resultado do percentual é: {resultado}%")

elif escolha == "0":
    print("Saindo do programa...")
    exit()



 

