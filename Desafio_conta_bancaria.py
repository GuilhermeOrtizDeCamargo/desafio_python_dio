import os
import time
import textwrap


def tempo():
    cont = 5
    print("\033[30mO MENU REINICIARÁ EM", end=" ")
    for i in range(5):
        print(cont, end= " ")
        cont -= 1
        time.sleep(1)


def menu():
    menu = """\n
    \033[30m------------------ MENU ---------------\n
     \033[32m[1]\t DEPOSITAR
     \033[32m[2]\t SACAR
     \033[32m[3]\t EXTRTATO 
     \033[32m[4]\t NOVO USUÁRIO
     \033[32m[5]\t NOVA CONTA
     \033[32m[6]\t LISTAR CONTAS
     \033[31m[7]\t SAIR
     
     \033[30m--------------------------------------\n
     
    \033[0m\tDigite a opção desejada: 
     
    => """
    return textwrap.dedent(menu)


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"\n\033[34mDepósito: R$ {valor:.2f}\n"
        print(f"\n\033[34mO depósito foi de {valor:.2f}.")
        print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\n\033[0m")
        tempo()
        os.system("cls")
    else:
        print("\n\033[31mOpoeração falhou! Proibído depósito negativo.\n")
        print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
        tempo()
        os.system("cls")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n\033[31mOperação falhou! A conta não tem saldo sufucuente.\n")
        print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
        tempo()
        os.system("cls")

    elif excedeu_limite:
        print("\n\033[31mOperação falhou! O valor de saque excede o limite.\n")
        print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
        tempo()
        os.system("cls")

    elif excedeu_saques:
        print("\n\033[31mOperação falhou! Número de saques excedido.\n")
        print(f"\n\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
        tempo()
        os.system("cls")

    elif valor > 0:
        saldo -= valor
        extrato += f"\n\033[31mSaque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n\033[31mO saque foi de {valor:.2f}.\n")
        print(f"\033[33mO saldo em conta {saldo:.2f}.\n\n\033[0m")
        tempo()
        os.system("cls")

    else:
        print("\n\033[31mOperação falhou! O valor informado é inválido.\n")
        print(f"\033[33mO saldo em conta {saldo:.2f}.\n\033[0m")
        tempo()
        os.system("cls")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n\033[30m--------------- EXTRATO ---------------\n")
    print("\n\033[31mNão foram realizadas movimentações.\n" if not extrato else extrato)
    print(f"\n\033[33mSaldo em conta R$ {saldo:.2f}")
    print("\n\033[30m--------------------------------------\n")
    print("\n\033[30mCLIQUE PARA VOLTAR AO MENU.")
    input()
    os.system("cls")


def criar_usuario(usuarios):
    cpf = input("\nInforme o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n\033[31mOperação falhou! Já existe usuário com esse CPF!.\n")
        tempo()
        os.system("cls")

    nome = input("\n\033[0mInforme o nome completo: ")
    data_nascimento = input("\nInforme a data de nascimento (dd-mm-aaaa): ")
    endereco = input("\nInforme o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(f"\n\033[30mUsuário criado com sucesso!\n\033[0m")
    tempo()
    os.system("cls")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    tempo()
    os.system("cls")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("\nInforme o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
       print(f"\n\033[30mConta criada com sucesso!\n\033[0m")
       tempo()
       os.system("cls")       
       return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    
    print("\n\033[31mOperação falhou! Usuário não encontrado!.\n\033[0m")
    tempo()
    os.system("cls")


def listar_contas(contas):
    for conta in contas:
        
        linha = f"""\
            \033[33mAgência:\t{conta['agencia']}
            \033[33mC/C:\t\t{conta['numero_conta']}
            \033[33mTitular:\t{conta['usuario']['nome']}\033[0m
        """
        print(textwrap.dedent(linha))


def main():

    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    limite_saques = 3
    usuarios = []
    contas = []
    opcao = 0

    while True:
        
        opcao = int(input(menu()))

        if opcao == 1:
            valor = float(input("\n\033[0mInforme o valor a ser depositado: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 2:
            valor = float(input("\n\033[0mInforme o valor do saque: "))
            valor = round(valor)
            
            saldo, extrato = sacar(
            saldo = saldo,
            valor = valor,
            extrato = extrato,
            limite = limite,
            numero_saques = numero_saques,
            limite_saques = limite_saques,
            )

        elif opcao == 3:
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == 4:
            criar_usuario(usuarios)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 6:
            listar_contas(contas)
            print("\n\033[30mCLIQUE PARA VOLTAR AO MENU.\n\033[0m")
            input()
            os.system("cls")
                
        elif opcao == 7:
            os.system("cls")
            break
        
        else:
            print("\n\033[31mOperação inválida, por favor selecione uma opção do MENU.\n\033[0m")
            tempo()
            os.system("cls")


main()
