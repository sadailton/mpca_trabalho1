import re


def le_endereco_ip(msg):
    while True:
        end_ip = input(msg)
        match = re.match('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))', end_ip)
        if match:
            return str(end_ip)
        else:
            print('Endereço inválido!')


def le_porta(msg):

    while True:
        porta = leInt(msg)
        if 1 < porta <= 65535:
            return porta
        else:
            print('Valor de porta inválido!')


def leFloat(msg):
    while True:
        try:
            numero = float((input(msg)).replace(',', '.'))
            break
        except(ValueError):
            print("Você deve digitar um número real")

    return numero


def leInt(msg):
    while True:
        try:
            numero = int(input(msg))
            break
        except(ValueError):
            print("Você deve digitar um número inteiro")

    return numero


def grava_arquivo(nomeArquivo, conteudo, rwa='a+'):

    with open(nomeArquivo, rwa) as arquivo:
        arquivo.writelines("%s\n" % linha for linha in conteudo)


def le_arquivo(nomeArquivo) -> list:

    conteudo = []

    with open(nomeArquivo, 'r') as arquivo:
        conteudoarquivo = arquivo.readlines()

        for linha in conteudoarquivo:
            aux = linha[:-1]
            conteudo.append(aux)
    return conteudo