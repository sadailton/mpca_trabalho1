import socket
from pickle import NONE


class SensorGenerico:

    server: str = ''
    server_port: int = 9876
    sensorid: int = ''
    localizacao: str = ''
    nome: str = ''

    def __init__(self, id_sensor: int, localizacao: str, nome: str):

        self.sensorid = id_sensor
        self.nome = nome
        self.localizacao = localizacao

    def conecta_servidor(self, ip_servidor: str, porta_servidor: int) -> socket:

        self.SERVER = ip_servidor
        self.SERVER_PORT = porta_servidor
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((ip_servidor, porta_servidor))

        return tcp

    def fecha_conexao(self, conexao: object):

        conexao.close()

    def set_sensorid(self, sensorid):
        self.sensorid = sensorid

    def get_sensorid(self):
        return self.sensorid

    def get_nome(self):
        return self.nome

    def set_localizacao(self, localizacao):
        self.localizacao = localizacao

    def get_localizacao(self):
        return self.localizacao


class Presenca(SensorGenerico):

    estado: int = 0

    def __init__(self, id_sensor, estado, localizacao):
        super().__init__(id_sensor, localizacao, 'presenca')
        self.estado = estado

    def get_estado(self):
        return self.estado

    def set_presenca(self, tem_presenca):
        self.estado = tem_presenca


class Termometro(SensorGenerico):

    temperatura: float = 0.0

    def __init__(self, id_sensor, temperatura, localizacao):

        super().__init__(id_sensor, localizacao, 'termometro')
        self.temperatura = temperatura

    def get_temperatura(self):
        return self.temperatura

    def set_temperatura(self, temperatura: float) -> NONE:
        self.temperatura = temperatura


class Lampada(SensorGenerico):

    estado: int = 0

    def __init__(self, id_sensor, estado: int, localizacao):
        super().__init__(id_sensor, estado, 'lampada')
        self.estado = estado

    def get_estado(self):
        return self.estado

    def ligar(self):
        self.estado = 1

    def desligar(self):
        self.estado = 0


class ArCondicionado(SensorGenerico):

    estado: int = 0

    def __init__(self, id_sensor: int, temperatura: float, estado: int, localizacao: str):
        super().__init__(id_sensor, localizacao, 'arcondicionado')
        self.temperatura = temperatura
        self.estado = estado
        self.localizacao = localizacao

    def ligar(self):
        self.estado = 1

    def desligar(self):
        self.estado = 0

    def get_estado(self):
        return self.estado





