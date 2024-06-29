import os
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime, timezone


def tempo():
    print("\n\033[30mCLIQUE PARA VOLTAR AO MENU.")
    input()


def cliente_inexistente():
    print("\n\033[31mERROR.\nFavor incluir um cliente e uma conta.\n")


def conta_inexistente():
    print("\n\033[31mERROR.\nFavor incluir uma conta.\n")


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Conta:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 5:
            print("\n\033[31mVoce excedeu o número de transações permitidas para hoje!\n")
            return

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
            print("\n\033[31mO limite do saldo foi excedido!\n")

        elif valor > 0:
            self._saldo -= valor
            print("\n\033[34mSaque realizado com sucesso!\n")
            return True

        else:
            print("\n\033[31mO valor informado é inválido!\n")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n\033[34mDepósito realizado com sucesso!.\n")
        else:
            print("\n\033[31mO limite de depósito é inválido!\n")
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
            print("\n\033[31mValor do saque excedido!\nSaques permitidos: até R$ 500,00.\n")

        elif excedeu_saques:
            print("\n\033[31mLimite de saques excedido!\nLimite permitido: 3 saques por CPF.\n")

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
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now(timezone.utc).date()
        transacoes = []
        for transacao in self.transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d/%m/%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


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


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"\033[30m{datetime.now()}: {func.__name__.upper()}")
        print(resultado)
        tempo()

    return envelope


def menu():
    os.system("cls")
    menu = """\n
    \033[30m------------------ MENU ---------------\n
    \033[32m[1]\t DEPOSITAR
    \033[32m[2]\t SACAR
    \033[32m[3]\t EXTRATO
    \033[32m[4]\t NOVO CLIENTE
    \033[32m[5]\t NOVA CONTA
    \033[32m[6]\t LISTAR CONTAS
    \033[31m[7]\t SAIR
    \033[30m--------------------------------------\n

    \033[0m\tDigite a opção desejada:

    => """
    return int(input(textwrap.dedent(menu)))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        cliente_inexistente()
        return

    valor = float(input("\nInforme o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        conta_inexistente()
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        cliente_inexistente()
        return

    valor = float(input("\nInforme o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        conta_inexistente()
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        cliente_inexistente()
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        conta_inexistente()
        return

    print("\n\033[30m--------------- EXTRATO ---------------")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}: R$   {transacao['valor']:.2f}\n"

    if not tem_transacao:
        extrato = "\n\033[30mNão foram realizadas movimentações.\n\033[0m"

    print(f"\033[33mNome do Titular:\033[0m {cliente.nome}")
    print(f"\033[33mConta do Titular:\033[0m {conta.numero}")
    print(extrato)
    print(f"\033[33mSaldo em conta \tR$ {conta.saldo:.2f}")
    print("\033[30m--------------------------------------\n")


@log_transacao
def criar_cliente(clientes):
    cpf = input("\nInforme o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n\033[31m\nJá existe cliente com esse CPF.\n")
        tempo()
        return

    nome = input("\nInforme o nome completo: ")
    data_nascimento = input("\nInforme a data de nascimento (dd-mm-aaaa): ")
    endereco = input("\nInforme o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n\033[34mCliente criado com sucesso!\n\033[0m")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        cliente_inexistente()
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n\033[34mConta criada com sucesso!\n\033[0m")


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("\033[30m------------------------------------\n")
        print(textwrap.dedent(str(conta)))
        tempo()


def main():

    clientes = []
    contas = []
    opcao = 0

    while True:
        os.system("cls")
        opcao = menu()

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

        elif opcao == 7:
            os.system("cls")
            break

        else:
            print("\n\033[31mFavor escolher uma opção válida!")
            tempo()


main()
