def painel_principal () :

  print("\nEscolha a operação desejada:")
  print("\n1 - Soma")
  print("2 - Subtração")
  print("3 - Multiplicação")
  print("4 - Divisão")
  print("5 - Exponenciação")
  print("6 - Radiciação")
  print("7 - Resto da divisão")
  print("8 - Percentual")
  print("9 - Divisão Inteira")
  print("0 - Sair do Programa")

  escolha = input("\nDigite o número da operação desejada: ")
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

def calcula_divisao(x,y):
   if y==0:
      return "Erro, divisão por 0."
   return x/y

def calcula_divisao_inteira(x,y):
   if y==0:
       return "Erro, divisão por 0."
   return x//y

escolha = painel_principal()

while escolha != "0":
    if escolha == "1":
        x = float(input("\nDigite o primeiro número: "))
        y = float(input("\nDigite o segundo número: "))
        resultado = calcula_soma(x, y)
        print(f"\nO resultado da soma é: {resultado}")
    
    elif escolha == "2":
        a = float(input("\nDigite o primeiro número: "))
        b = float(input("\nDigite o segundo número: "))
        resultado = calcula_subtracao(a, b)
        print(f"\nO resultado da subtração é: {resultado}")
    
    elif escolha == "3":
        a = float(input("\nDigite o primeiro número: "))
        b = float(input("\nDigite o segundo número: "))
        resultado = calcula_multiplicacao(a, b)
        print(f"\nO resultado da multiplicação é: {resultado}")
    
    elif escolha == "4":
        a = float(input("\nDigite o primeiro número: "))
        b = float(input("\nDigite o segundo número: "))
        if b != 0:
            resultado = a / b
            print(f"\nO resultado da divisão é: {resultado}")
        else:
            print("\nErro: Divisão por zero não é permitida.")
    
    elif escolha == "5":
        a = float(input("\nDigite a base: "))
        b = float(input("\nDigite o expoente: "))
        resultado = calcula_exponenciacao(a, b)
        print(f"\nO resultado da exponenciação é: {resultado}")
    
    elif escolha == "6":
        a = float(input("\nDigite o radicando: "))
        b = float(input("\nDigite o índice (raiz): "))
        if b != 0:
            resultado = calcula_radiciacao(a, b)
            print(f"\nO resultado da radiciação é: {resultado}")
        else:
            print("\nErro: Índice de radiciação não pode ser zero.")
    
    elif escolha == "7":
        x = float(input("\nDigite o dividendo: "))
        y = float(input("\nDigite o divisor: "))
        if y != 0:
            resultado = calcula_resto(x, y)
            print(f"\nO resto da divisão é: {resultado}")
        else:
            print("\nErro: Divisão por zero não é permitida.")
    
    elif escolha == "8":
        x = float(input("\nDigite o valor parcial: "))
        y = float(input("\nDigite o valor total: "))
        if y != 0:
            resultado = calcula_percentual(x, y)
            print(f"\nO percentual é: {resultado}")
        else:
            print("\nErro: Divisão por zero não é permitida.")

    elif escolha == "0":
        print("\nSaindo do programa...")
        break 

    escolha = painel_principal() 