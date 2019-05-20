__author__ = "Adailton Saraiva"
__email__ = "s.adailton@gmail.com"

from ClassServidor import *
from ClassThread import *
from ast import literal_eval
from random import randint

TAM_BUFFER: int = 1024
sensores = {}

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


def controla_arcondicionado(temperatura, local, estado=0):

    for i in sensores:
        if sensores[i]['nome'] == 'arcondicionado':
            if sensores[i]['local'] == local:
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

        elif sensorid[sensorid]['nome'] == 'presenca':
            tem_presenca = int(msg_from_client['estado'])
            local = str(sensores[sensorid]['local'])
            controla_lampada(tem_presenca, local)


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