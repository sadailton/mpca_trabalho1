__author__ = "Adailton Saraiva"
__email__ = "s.adailton@gmail.com"

from ClassSensor import *
from random import randint
from ast import literal_eval
import time


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

    server_ip = '127.0.0.10'
    server_port = 9876

    '''
    server_ip = input('Informe o IP da central de controle: ')
    server_port = input('Informe a porta TCP de conexão: ')
    '''

    tipo_sensor = menu()
    idsensor = randint(1, 9999)

    cabecalho_sensor = {'sensorid': ''}

    if tipo_sensor == 1:

        sensor_lampada = Lampada(idsensor, 0, '')

        pass

    elif tipo_sensor == 2:
        pass

    elif tipo_sensor == 3:
        sensor_presenca = Presenca(idsensor, 0, '')

        try:
            print('Conectando-se ao servidor... ')
            sensor_presenca_soquete = sensor_presenca.conecta_servidor(server_ip, server_port)
            print('Conexao estabelecida com sucesso!')

            msg_to_server = str(sensor_presenca.get_nome())
            envia_msg(sensor_temperatura_soquete, msg_to_server)
            msg_from_server = recebe_msg(sensor_temperatura_soquete)

            # O servidor envia um dicionario com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)

            sensorid = list(msg_from_server)[0]

            sensor_presenca.set_sensorid(sensorid)
            sensor_presenca.set_localizacao(msg_from_server[sensorid]['local'])

            while True:

                msg_to_server = str('Tem alguém no ambiente? (s/n): ')

                if msg_to_server == 'sair':
                    sensor_presenca_soquete.close()
                elif msg_to_server == 's':
                    sensor_presenca.set_presenca(1)

                    cabecalho_sensor['sensorid'] = sensor_presenca.get_sensorid()
                    cabecalho_sensor.update({'estado': sensor_presenca.get_estado()})
        except:
            print("Deu pau!")

    elif tipo_sensor == 4:
        sensor_arcondicionado = ArCondicionado(idsensor, 22, 0, 'quarto casal')
        try:
            print('Conectando-se ao servidor... ')
            sensor_arcondicionado_soquete = sensor_arcondicionado.conecta_servidor(server_ip, server_port)
            print('Conexao estabelecida com sucesso!')

            msg_to_server = str(sensor_arcondicionado.get_nome())
            envia_msg(sensor_arcondicionado_soquete, msg_to_server)
            msg_from_server = recebe_msg(sensor_arcondicionado_soquete)

            # O servidor envia um dicionario com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)

            sensorid = list(msg_from_server)[0]

            sensor_arcondicionado.set_sensorid(sensorid)
            sensor_arcondicionado.set_localizacao(msg_from_server[sensorid]['local'])

            while True:

                msg_from_server = recebe_msg(sensor_arcondicionado_soquete)
                print(msg_from_server)
                if msg_from_server == 'ligar':
                    print("Ligando ar condicionado... ", end="")
                    time.sleep(1)
                    sensor_arcondicionado.ligar()
                    print("OK", end="\n")
                elif msg_from_server == 'desligar':
                    print("Desligando ar condicionado... ", end="")
                    time.sleep(1)
                    sensor_arcondicionado.desligar()
                    print("OK", end="\n")

        except (ConnectionRefusedError, ConnectionError):
            print("Não foi possível se conectar ao servidor.")
            print("Verifique se o mesmo se encontra ligado e conectado a rede e se o ip do servidor e a porta estão corretos.")
            exit(1)

    # Termometro
    elif tipo_sensor == 5:
        sensor_temperatura = Termometro(idsensor, 22, 'sala')
        try:
            print("Conectando-se ao servidor...")
            sensor_temperatura_soquete = sensor_temperatura.conecta_servidor(server_ip, server_port)
            print("Conexão estabelecida com sucesso!")
            msg = str(sensor_temperatura.nome)
            envia_msg(sensor_temperatura_soquete, msg)
            msg_from_server = recebe_msg(sensor_temperatura_soquete)

            # O servidor envia um dicionario com as configurações do sensor
            msg_from_server = literal_eval(msg_from_server)
            sensorid = list(msg_from_server)[0]

            sensor_temperatura.sensorid = sensorid
            sensor_temperatura.set_localizacao(msg_from_server[sensorid]['local'])

        except (ConnectionRefusedError, ConnectionError):
            print("Não foi possível se conectar ao servidor.")
            print("Verifique se o mesmo se encontra ligado e conectado a rede e se o ip do servidor e a porta estão corretos.")
            exit(1)

        while True:
            msg = input('Temperatura do ambiente em ºC: ')
            if msg == '000':
                print('Encerrando conexão com a central...')
                sensor_temperatura.fecha_conexao(sensor_temperatura_soquete)
                print('Conexão encerrada:')
                break
            else:
                sensor_temperatura.set_temperatura(float(msg))

                cabecalho_sensor['sensorid'] = sensor_temperatura.get_sensorid()
                cabecalho_sensor.update({'temperatura': sensor_temperatura.get_temperatura()})

                print('Cabeçalho: {}'.format(cabecalho_sensor))

                envia_msg(sensor_temperatura_soquete, cabecalho_sensor)

    else:
        print('Opção inválida')
        exit(1)


if __name__ == '__main__':
    main()
    exit(0)
