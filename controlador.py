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

    while True:
        msg = conexao.recv(TAM_BUFFER)
        if not msg:
            break
        else:
            nome_dispositivo = msg.decode('utf8')
            print(nome_dispositivo)
            sensorid = randint(1, 999)
            local_dispositivo = str(input('Informe o cômodo onde o dispositivo está instalado: '))
            sensores[sensorid] = {'nome': nome_dispositivo}
            sensores[sensorid] = {'local': local_dispositivo}
            sensores[sensorid] = {'conexao': conexao}

            if nome_dispositivo == 'termometro':
                sensores[sensorid] = {'temperatura'}

            conexao.sendall(bytes(str(sensorid), 'utf8'))
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

        #msg = conexao.recv(TAM_BUFFER)


            # msg = msg.decode('utf8')



            #sensores[idsensor]['thread'] = threading.Thread(target=controla_sensor, args=(conexao, ip_addr))

           # print(sensores)

            #sensores[idsensor]['thread'].start()


if __name__ == '__main__':
    main()