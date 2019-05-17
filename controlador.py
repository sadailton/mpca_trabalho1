__author__ = "Adailton Saraiva"
__email__ = "s.adailton@gmail.com"

from ClassServidor import *
from ClassSensor import *
from ClassThread import *
from ast import literal_eval
from random import randint

TAM_BUFFER: int = 1024
sensores = {}

def controla_lampada(estado: int):

    if estado == 1:
        print("Desligando lampada... ")
    else:
        estado = 1

    return 0

def controla_arcondicionado(conexao, ip_addr):
    pass

def controla_sensor(conexao, ip_addr):

    conexao.sendall(b'Seja bem vindo!!!')

    while True:
        print("Conectador por: {}".format(ip_addr))
        try:
            msg = conexao.recv(TAM_BUFFER)
            if not msg:
                break
        except (ConnectionError, ConnectionResetError):
            print("O cliente {} encerrou a conexão".format(ip_addr))
            break

        print(ip_addr, msg.decode('utf8'))

        msg: str = input('Envie sua msg para o cliente: ')
        conexao.sendall(bytes(msg, 'utf8'))

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

            sensores_aux[sensorid] = {'nome': '', 'local': local_dispositivo}

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
            sensores_aux[sensorid].update({'conexao': str(conexao)})
            sensores.update(sensores_aux)
            return True

    return False

def main():

    HOST_IP: str = '127.0.0.10'
    HOST_PORT: int = 9876
    NUM_CONN = 10

    server = Servidor(HOST_IP, HOST_PORT, NUM_CONN)

    while True:
        conexao, ip_addr = server.cria_conexao()
        thread = threading.Thread(target=configura_dispositivo, args=(conexao, ip_addr))

        thread.start()
        thread.join()



if __name__ == '__main__':
    main()