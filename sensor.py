__author__ = "Adailton Saraiva"
__email__ = "s.adailton@gmail.com"

from ClassSensor import *
from random import randint, random
from ast import literal_eval
import time
from datetime import datetime

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

def envia_msg(sensor_socket: socket, msg: str):

    sensor_socket.sendall(bytes(str(msg), 'utf8'))

def recebe_msg(sensor_socket: socket) -> str:

    msg = sensor_socket.recv(1024)
    return msg.decode('utf8')


def interagir_sensor_servidor(sensor):
    pass


def menu():
    print("Informe o tipo de sensor que deseja instalar neste dispositivo: ")
    print('1 - Lâmpada')
    print('2 - Tomada')
    print('3 - Presença')
    print('4 - Ar condicionado')
    print('5 - Termometro')
    opcao: int = int(input('opcao: '))

    return opcao


def main():

    server_ip: str = '127.0.0.10'
    server_port: int = 9876

    INTERVALO_SEG_MONITORAMENTO_TOMADA = 120

    tipo_sensor = menu()
    idsensor = randint(1, 9999)

    cabecalho_sensor = {'sensorid': ''}

    # Lampada
    if tipo_sensor == 1:

        sensor_lampada = Lampada(idsensor, 0, '')

        sensor_lampada_soquete = sensor_lampada.conecta_servidor(server_ip, server_port)

        if sensor_lampada_soquete:
            msg_to_server = sensor_lampada.get_nome()
            envia_msg(sensor_lampada_soquete, msg_to_server)
            msg_from_server = recebe_msg(sensor_lampada_soquete)

            # O servidor envia um dicionário com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)

            sensorid = list(msg_from_server)[0]

            sensor_lampada.set_sensorid(sensorid)
            sensor_lampada.set_localizacao(msg_from_server[sensorid]['local'])

            cabecalho_sensor['sensorid'] = sensor_lampada.get_sensorid()

            while True:
                msg_from_server = literal_eval(recebe_msg(sensor_lampada_soquete))

                datahora = datetime.fromtimestamp(msg_from_server['timestamp'])

                if msg_from_server['comando'] == 1:
                    print('(id: {}, ts: {}) Ligando lampada... '.format(msg_from_server['sensorid'], datahora), end='')
                    sensor_lampada.ligar()
                    print('OK', end='\n')
                elif msg_from_server['comando'] == 0:
                    print('(id: {}, ts: {})Desligando lampada... '.format(msg_from_server['sensorid'], datahora), end='')
                    sensor_lampada.desligar()
                    print('OK', end='\n')
                else:
                    print('Comando não reconhecido')
    # Tomada
    elif tipo_sensor == 2:
        sensor_tomada = Tomada(idsensor, '')

        sensor_tomada_soquete = sensor_tomada.conecta_servidor(server_ip, server_port)

        if sensor_tomada_soquete:
            msg_to_server = sensor_tomada.get_nome()
            envia_msg(sensor_tomada_soquete, msg_to_server)
            msg_from_server = recebe_msg(sensor_tomada_soquete)

            # O servidor envia um dicionario com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)

            sensorid = list(msg_from_server)[0]

            sensor_tomada.set_sensorid(sensorid)
            sensor_tomada.set_localizacao(msg_from_server[sensorid]['local'])

            cabecalho_sensor['sensorid'] = sensor_tomada.get_sensorid()

            while True:
                msg_to_server = random()*10
                print(msg_to_server)
                #msg_to_server = leFloat("Informe o consumo desta tomada (Kwh): ")

                sensor_tomada.set_consumo(msg_to_server)
                cabecalho_sensor['consumo'] = msg_to_server

                envia_msg(sensor_tomada_soquete, cabecalho_sensor)
                time.sleep(INTERVALO_SEG_MONITORAMENTO_TOMADA)

    # Presenca
    elif tipo_sensor == 3:
        sensor_presenca = Presenca(idsensor, 0, '')

        sensor_presenca_soquete = sensor_presenca.conecta_servidor(server_ip, server_port)

        if sensor_presenca_soquete:

            msg_to_server = sensor_presenca.get_nome()
            envia_msg(sensor_presenca_soquete, msg_to_server)
            msg_from_server = recebe_msg(sensor_presenca_soquete)

            # O servidor envia um dicionario com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)

            sensorid = list(msg_from_server)[0]

            sensor_presenca.set_sensorid(sensorid)
            sensor_presenca.set_localizacao(msg_from_server[sensorid]['local'])

            cabecalho_sensor['sensorid'] = sensor_presenca.get_sensorid()

            while True:

                msg_to_server = str(input('Tem alguém no ambiente? (s/n): '))

                if msg_to_server == 'sair':
                    sensor_presenca_soquete.close()

                elif msg_to_server == 's' or msg_to_server == 'S':
                    sensor_presenca.set_presenca(1)
                    cabecalho_sensor.update({'estado': sensor_presenca.get_estado()})
                    cabecalho_sensor.update({'timestamp': datetime.now().timestamp()})
                    envia_msg(sensor_presenca_soquete, cabecalho_sensor)

                elif msg_to_server == 'n' or msg_to_server == 'N':
                    sensor_presenca.set_presenca(0)
                    cabecalho_sensor.update({'estado': sensor_presenca.get_estado()})
                    cabecalho_sensor.update({'timestamp': datetime.now().timestamp()})
                    envia_msg(sensor_presenca_soquete, cabecalho_sensor)
                else:
                    print('Resposta inválida')
        else:
            print('Não foi possível estabelecer uma conexão com o servidor.')
            print('Verifique se o mesmo encontra-se ligado e conectado à rede')
            exit(2)

    # Ar condicionado
    elif tipo_sensor == 4:
        sensor_arcondicionado = ArCondicionado(idsensor, 22, 0, 'quarto casal')

        sensor_arcondicionado_soquete = sensor_arcondicionado.conecta_servidor(server_ip, server_port)

        if sensor_arcondicionado_soquete:

            msg_to_server = str(sensor_arcondicionado.get_nome())
            envia_msg(sensor_arcondicionado_soquete, msg_to_server)
            msg_from_server = recebe_msg(sensor_arcondicionado_soquete)

            # O servidor envia um dicionario com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)

            sensorid = list(msg_from_server)[0]

            sensor_arcondicionado.set_sensorid(sensorid)
            sensor_arcondicionado.set_localizacao(msg_from_server[sensorid]['local'])

            while True:

                msg_from_server = literal_eval(recebe_msg(sensor_arcondicionado_soquete))
                datahora = datetime.fromtimestamp(msg_from_server['timestamp'])

                if msg_from_server['comando'] == 1:
                    print("(id: {}, ts: {}) Ligando ar condicionado... ".format(msg_from_server['sensorid'], datahora), end="")
                    sensor_arcondicionado.ligar()
                    print("OK", end="\n")
                elif msg_from_server['comando'] == 0:
                    print("(id: {}, ts: {}) Desligando ar condicionado... ".format(msg_from_server['sensorid'], datahora), end="")
                    sensor_arcondicionado.desligar()
                    print("OK", end="\n")
                else:
                    print('Comando não reconhecido')
        else:
            print('Não foi possível estabelecer uma conexão com o servidor.')
            print('Verifique se o mesmo encontra-se ligado e conectado à rede')
            exit(2)

    # Termometro
    elif tipo_sensor == 5:
        sensor_temperatura = Termometro(idsensor, 22, '')

        sensor_temperatura_soquete = sensor_temperatura.conecta_servidor(server_ip, server_port)

        if sensor_temperatura_soquete:

            msg = str(sensor_temperatura.nome)
            envia_msg(sensor_temperatura_soquete, msg)
            msg_from_server = recebe_msg(sensor_temperatura_soquete)

            # O servidor envia um dicionario com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)
            sensorid = list(msg_from_server)[0]

            sensor_temperatura.sensorid = sensorid
            sensor_temperatura.set_localizacao(msg_from_server[sensorid]['local'])

            while True:
                msg = leFloat('Temperatura do ambiente em ºC: ')
                if msg == '99':
                    print('Encerrando conexão com a central...')
                    sensor_temperatura.fecha_conexao(sensor_temperatura_soquete)
                    print('Conexão encerrada:')
                    break
                else:
                    sensor_temperatura.set_temperatura(float(msg))

                    cabecalho_sensor['sensorid'] = sensor_temperatura.get_sensorid()
                    cabecalho_sensor.update({'temperatura': sensor_temperatura.get_temperatura()})
                    cabecalho_sensor.update({'timestamp': datetime.now().timestamp()})

                    envia_msg(sensor_temperatura_soquete, cabecalho_sensor)
        else:
            print("Não foi possível se conectar ao servidor.")
            print("Verifique se o mesmo se encontra ligado e conectado a rede e se o ip do servidor e a porta estão corretos.")
            exit(1)

    else:
        print('Opção inválida')
        exit(2)


if __name__ == '__main__':
    main()
    exit(0)
