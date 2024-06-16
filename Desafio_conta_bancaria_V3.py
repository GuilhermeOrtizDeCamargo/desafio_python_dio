import os
import time
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
#from datetime import datetime


def tempo():
    cont = 5
    print("\033[30mO MENU REINICIARÁ EM", end=" ")
    for i in range(5):
        print(cont, end= " ")
        cont -= 1
        time.sleep(1)
    os.system("cls")


def falhou():
    print("\n\033[31mOperação falhou! Tente novamente.\n")
    tempo()
    os.system("cls")


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
        
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            falhou()

        elif valor > 0:
            self._saldo -= valor
            print("\n\033[34mSaque realizado com sucesso!.\n")
            tempo()
            return True

        else:
            falhou()

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n\033[34mDepósito realizado com sucesso!.\n")
            tempo()
        else:
            falhou()
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            falhou()
            
        elif excedeu_saques:
            falhou()

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            \033[33mAgência:\t\033[0m{self.agencia}
            \033[33mC/C:\t\t\033[0m{self.numero}
            \033[33mTitular:\t\033[0m{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
               # "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    os.system("cls")
    menu = """\n
    \033[30m------------------ MENU ---------------\n
    \033[32m[1]\t DEPOSITAR
    \033[32m[2]\t SACAR
    \033[32m[3]\t EXTRATO
    \033[32m[4]\t NOVO USUÁRIO
    \033[32m[5]\t NOVA CONTA
    \033[32m[6]\t LISTAR CONTAS
    \033[31m[7]\t SAIR
    
    \033[30m--------------------------------------\n
    
    \033[0m\tDigite a opção desejada: 
    
    => """
    return textwrap.dedent(menu)


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        falhou()
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        falhou()
        return

    valor = float(input("\nInforme o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        falhou()
        return

    valor = float(input("\nInforme o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        falhou()
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        falhou()
        return

    print("\n\033[30m--------------- EXTRATO ---------------")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "\n\033[30mNão foram realizadas movimentações.\n\033[0m"
    else:
        for transacao in transacoes:
            extrato += f"\n\033[0m{transacao['tipo']}:R$\t {transacao['valor']:.2f}\n"

    print(f"\n\033[33mNome do Titular:\033[0m {cliente.nome}\n")
    print(f"\033[33mConta do Titular:\033[0m {conta.numero}")
    print(extrato)
    print(f"\n\033[33mSaldo em conta \tR$ {conta.saldo:.2f}")
    print("\033[30m--------------------------------------\n")
    print("\n\033[30mCLIQUE PARA VOLTAR AO MENU.")
    input()


def criar_cliente(clientes):
    cpf = input("\nInforme o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        falhou()
        return
    
    nome = input("\nInforme o nome completo: ")
    data_nascimento = input("\nInforme a data de nascimento (dd-mm-aaaa): ")
    endereco = input("\nInforme o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)
    
    print("\n\033[34mCliente criado com sucesso!\n\033[0m")
    tempo()
   # os.system("cls")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        falhou()
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n\033[34mConta criada com sucesso!\n\033[0m")
    tempo()


def listar_contas(contas):
    for conta in contas:
        print("\033[30m------------------------------------\n")
        print(textwrap.dedent(str(conta)))


def main():

    clientes = []
    contas = []
    opcao = 0

    while True:
        os.system("cls")
        opcao = int(input(menu()))

        if opcao == 1:
            depositar(clientes)
        
        elif opcao == 2:
            sacar(clientes)

        elif opcao == 3:
            exibir_extrato(clientes)
        
        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)
            if not contas:
                falhou()
            else:
                print("\n\033[30mCLIQUE PARA VOLTAR AO MENU.\n\033[0m")
                input()
                
        elif opcao == 7:
            os.system("cls")
            break
        
        else:
            falhou()


main()
