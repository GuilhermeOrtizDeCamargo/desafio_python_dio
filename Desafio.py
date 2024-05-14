# depósito - Não pode ter depósitos negativos
# Saque - só pode ter 3 saques, cada saque pode ser de até 500,00, caso não tenha saldo informar o usuário
# Extrato - deve ter formatação de valores 

import os
import time

print("\n\033[33mCLIQUE PARA INICIAR O SISTEMA.\n\033[0m")
input()
os.system("cls")


menu = ''' 
 ___________________________
|                           |
|           \033[34mMENU\033[0m            | 
|                           |
|     \033[32m[ 1 ] DEPOSITAR\033[0m       |
|     \033[32m[ 2 ] SACAR\033[0m           |
|     \033[32m[ 3 ] EXTRTATO\033[0m        |
|     \033[31m[ 4 ] SAIR\033[0m            |
|___________________________|
'''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3
opcao = 0

while True:
    
    def tempo():
        cont = 5
        print("O MENU REINICIARÁ EM", end=" ")
        for i in range(5):
            print(cont, end= " ")
            cont -= 1
            time.sleep(1)
                    
    opcao = int(input(menu + "\nDigite a opção desejada: " ))

    if opcao == 1:
        valor = float(input("\nInforme o valor a ser depositado: "))
        
        if valor > 0:
            saldo += valor
            extrato += f"\n\033[34mDepósito: R$ {valor:.2f}\n\033[0m"
            print(f"\n\033[34mO depósito foi de {valor:.2f}.\033[0m")
            print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\n\033[0m")
            tempo()
            os.system("cls")

            
        else:
            print("\n\033[31mOpoeração falhou! Proibído depósito negativo.\n\033[0m")
            print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
            tempo()
            os.system("cls")
            
    elif opcao == 2:
        valor = float(input("\nInforme o valor do saque: "))
        valor = round(valor)
        
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >=limite_saques
        
        if excedeu_saldo:
            print("\n\033[31mOperação falhou! A conta não tem saldo sufucuente.\n\033[0m")
            print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
            tempo()
            os.system("cls")

        elif excedeu_limite:
            print("\n\033[31mOperação falhou! O valor de saque excede o limite.\n\033[0m")
            print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
            tempo()
            os.system("cls")

        elif excedeu_saques:
            print("\n\033[31mOperação falhou! Número de saques excedido.\n\033[0m")
            print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
            tempo()
            os.system("cls")
            
        elif valor > 0:
            saldo -= valor
            extrato += f"\n\033[31mSaque: R$ {valor:.2f}\n\033[0m"
            numero_saques += 1
            print(f"\n\033[31mO saque foi de {valor:.2f}.\n\033[0m")
            print(f"\033[33mO saldo em conta {saldo:.2f}.\n\n\033[0m")
            tempo()
            os.system("cls")
            
        else:
            print("\n\033[31mOperação falhou! O valor informado é inválido.\n\033[0m")
            print(f"\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
            tempo()
            os.system("cls")
            
    elif opcao == 3:
        print("\n*************************************\n\n")
        print(f"           EXTRATO              \n")
        print("\n\033[31mNão foram realizadas movimentações.\n\033[0m" if not extrato else extrato)
        print(f"\n\033[33mSaldo em conta R$ {saldo:.2f}\033[0m")
        print("\n\n*************************************\n")
        print("\n\033[33mCLIQUE PARA VOLTAR AO MENU.\n\033[0m")
        input()
        os.system("cls")

    elif opcao == 4:
        os.system("cls")
        break
    
    else:
        print("\n\033[31mOperação inválida, por favor selecione uma opção do MENU.\033[0m")
        tempo()
        os.system("cls")