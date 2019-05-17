__author__ = "Adailton Saraiva"
__email__ = "s.adailton@gmail.com"

from ClassSensor import *
from random import randint
from ast import literal_eval

def envia_msg(sensor_socket: socket, msg: str):

    sensor_socket.sendall(bytes(msg, 'utf8'))


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

    if tipo_sensor == 1:

        sensor_lampada = Lampada(idsensor, 0, '')

        pass

    elif tipo_sensor == 2:
        pass

    elif tipo_sensor == 3:
        sensor_presenca = Presenca(idsensor, 0, '')

        pass

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

                if msg_from_server[sensorid]['estado'] == 1:
                    sensor_arcondicionado.ligar()
                    envia_msg(sensor_arcondicionado_soquete, sensor_arcondicionado.estado)
                else:
                    sensor_arcondicionado.desligar()
                    envia_msg(sensor_arcondicionado_soquete, sensor_arcondicionado.estado)

        except (ConnectionRefusedError, ConnectionError):
            print("Não foi possível se conectar ao servidor.")
            print("Verifique se o mesmo se encontra ligado e conectado a rede e se o ip do servidor e a porta estão corretos.")
            exit(1)

    # Termometro
    elif tipo_sensor == 5:
        sensor_temperatura = Termometro(idsensor, 22, 'quarto casal')
        try:
            print("Conectando-se ao servidor...")
            sensor_temperatura_soquete = sensor_temperatura.conecta_servidor(server_ip, server_port)
            print("Conexão estabelecida com sucesso!")
            msg = str(sensor_temperatura.nome)
            envia_msg(sensor_temperatura_soquete, msg)
            msg_from_server = recebe_msg(sensor_temperatura_soquete)
            sensor_temperatura.sensorid = list(msg_from_server)[0]
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
                envia_msg(sensor_temperatura_soquete, msg)
                print(recebe_msg(sensor_temperatura_soquete))
    else:
        print('Opção inválida')
        exit(1)


if __name__ == '__main__':
    main()
    exit(0)
