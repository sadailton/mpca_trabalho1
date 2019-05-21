__author__ = "Adailton Saraiva"
__email__ = "s.adailton@gmail.com"

from ClassServidor import *
from ClassThread import *
from ast import literal_eval
from random import randint
import time
import datetime

TAM_BUFFER: int = 1024

# tempo em segundos
TEMPORIZADOR_SENSOR_PRESENCA = 6000

HORA_LIGAR_ARCONDICIONADO = '20:06:00'
HORA_DESLIGAR_ARCONDICIONADO = '20:10:00'

sensores = {}


def agenda_arcondicionado(hora_ligar, hora_desligar):

    intervalo: int = 30

    h, m, s = hora_ligar.split(':')
    s = int(s) + intervalo - 1
    hora_ligar_max = h+':'+m+':'+str(s)

    h, m, s = hora_desligar.split(':')
    s = int(s) + intervalo - 1
    hora_desligar_max = h+':'+m+':'+str(s)

    print(hora_ligar_max)
    print(hora_desligar_max)

    while True:
        time.sleep(intervalo)
        if hora_ligar <= time.strftime('%H:%M:%S') < hora_ligar_max:
            controla_arcondicionado(22, 'todos', 1)
        elif hora_desligar <= time.strftime('%H:%M:%S') < hora_desligar_max:
            controla_arcondicionado(22, 'todos', 0)


def grava_arquivo(nomeArquivo, conteudo):

    with open(nomeArquivo, 'a+') as arquivo:
        arquivo.writelines("%s\n" % linha for linha in conteudo)


def le_arquivo(nomeArquivo):

    conteudo = []

    with open(nomeArquivo, 'r') as arquivo:
        conteudoarquivo = arquivo.readlines()

        for linha in conteudoarquivo:
            aux = linha[:-1]
            conteudo.append(aux)
    return conteudo


def controla_tomada(consumo, local):

    nomeArquivo = 'relatorio_tomadas.txt'
    log_tomada = []

    for i in sensores:
        if sensores[i]['nome'] == 'tomada':
            if sensores[i]['local'] == local:
                if consumo == 999:
                    try:
                        print(le_arquivo(nomeArquivo))
                    except(FileNotFoundError):
                        print("Arquivo não encontrado")
                else:
                    log_tomada.append({'sensorid': i, 'consumo': consumo, 'local': local})
                    try:
                        grava_arquivo(nomeArquivo, log_tomada)
                    except(EOFError, IOError):
                        print("Erro ao salvar os dados no arquivo '{}'".format(nomeArquivo))


def controla_lampada(tem_presenca, local):

    for i in sensores:
        if sensores[i]['nome'] == 'lampada':
            if sensores[i]['local'] == local:
                try:
                    if tem_presenca == 1:
                        print("Ligando lampadas do ambiente: {}".format(local))
                        sensores[i]['conexao'].sendall(bytes('ligar', 'utf8'))

                    elif tem_presenca == 0:
                        print("Desligando lampadas do ambiente: {}".format(local))
                        sensores[i]['conexao'].sendall(bytes('desligar', 'utf8'))

                except (ConnectionError, ConnectionResetError):
                    print("Erro ao se conectar a lampada instalada em {}.".format(local))


def controla_arcondicionado(temperatura, local, ligar=0):

    for i in sensores:
        if sensores[i]['nome'] == 'arcondicionado':
            if ligar == 1 and local == 'todos':
                print("Ligando o ar condicionado. Local: {}".format(sensores[i]['local']))
                sensores[i]['conexao'].sendall(bytes('ligar', 'utf8'))
            elif ligar == 0 and local == 'todos':
                print("Desligando o ar condicionado. Local: {}".format(sensores[i]['local']))
                sensores[i]['conexao'].sendall(bytes('desligar', 'utf8'))

            elif sensores[i]['local'] == local:
                try:
                    if temperatura > 28:
                        print("Ligando o ar condicionado. Local: {}".format(local))
                        sensores[i]['conexao'].sendall(bytes('ligar', 'utf8'))

                    elif temperatura < 22:
                        print("Desligando o ar condicionado. Local: {}".format(local))
                        sensores[i]['conexao'].sendall(bytes('desligar', 'utf8'))

                except (ConnectionError, ConnectionResetError):
                    print("Erro ao se conectar ao ar condicionado instalado em {}.".format(local))


def gerencia_sensor(conexao, ip_addr):

    while True:
        print("Conectador por: {}".format(ip_addr))
        try:
            msg_from_client = conexao.recv(TAM_BUFFER)
            if not msg_from_client:
                break
        except (ConnectionError, ConnectionResetError):
            print("O cliente {} encerrou a conexão".format(ip_addr))
            break

        msg_from_client = literal_eval(msg_from_client.decode())
        sensorid = int(msg_from_client['sensorid'])

        if sensores[sensorid]['nome'] == 'termometro':
            temperatura = float(msg_from_client['temperatura'])
            local = str(sensores[sensorid]['local'])
            controla_arcondicionado(temperatura, local)

        elif sensores[sensorid]['nome'] == 'presenca':
            tem_presenca = int(msg_from_client['estado'])
            if tem_presenca == 0:
                time.sleep(TEMPORIZADOR_SENSOR_PRESENCA)

            local = str(sensores[sensorid]['local'])
            controla_lampada(tem_presenca, local)

        elif sensores[sensorid]['nome'] == 'tomada':
            consumo = float(msg_from_client['consumo'])
            local = str(sensores[sensorid]['local'])
            controla_tomada(consumo, local)


def configura_dispositivo(conexao, ip_addr):

    sensores_aux = {}

    while True:

        msg = conexao.recv(TAM_BUFFER)

        if not msg:
            break
        else:
            nome_dispositivo = msg.decode('utf8')
            local_dispositivo = input('Sensor: {}. Informe o cômodo onde este dispositivo está instalado: '.format(nome_dispositivo))

            print("Gerando id do dispositivo... ", end="")
            sensorid = randint(1, 999)
            print("id: {}".format(sensorid))

            sensores_aux[sensorid] = {'nome': nome_dispositivo, 'local': local_dispositivo}

            if nome_dispositivo == 'lampada':
                sensores_aux[sensorid].update({'estado': ''})

            elif nome_dispositivo == 'tomada':
                sensores_aux[sensorid].update({'estado': ''})
                sensores_aux[sensorid].update({'consumo': ''})

            elif nome_dispositivo == 'presenca':
                sensores_aux[sensorid].update({'estado': ''})

            elif nome_dispositivo == 'arcondicionado':
                sensores_aux[sensorid].update({'estado': 1})

            elif nome_dispositivo == 'termometro':
                sensores_aux[sensorid].update({'temperatura': ''})
            else:
                return False

            conexao.sendall(bytes(str(sensores_aux), 'utf8'))
            sensores_aux[sensorid].update({'conexao': conexao})
            sensores.update(sensores_aux)
            return True

    return False


def main():

    HOST_IP: str = '127.0.0.10'
    HOST_PORT: int = 9876
    NUM_CONN = 10

    server = Servidor(HOST_IP, HOST_PORT, NUM_CONN)
    threads = []
    threads2 = []

    thread = threading.Thread(target=agenda_arcondicionado, args=(HORA_LIGAR_ARCONDICIONADO, HORA_DESLIGAR_ARCONDICIONADO))
    thread.daemon = True
    thread.start()

    while True:
        conexao, ip_addr = server.cria_conexao()
        newthread = threading.Thread(target=configura_dispositivo, args=(conexao, ip_addr))

        newthread.start()
        threads.append(newthread)

        for t in threads:
            t.join()

        newthread2 = threading.Thread(target=gerencia_sensor, args=(conexao, ip_addr))
        newthread2.start()

        for t in threads2:
            t.join()


if __name__ == '__main__':
    main()
