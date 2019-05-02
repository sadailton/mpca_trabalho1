import socket
from pickle import NONE


class SensorGenerico:

    server: str = ''
    server_port: int = 9876
    idsensor: int = ''
    localizacao: str = ''
    nome: str = ''

    def __init__(self, id_sensor: int, localizacao: str, nome: str):

        self.idsensor = id_sensor
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


class Termometro(SensorGenerico):

    temperatura: float = 0.0

    def __init__(self, id_sensor, temperatura, localizacao):

        super().__init__(id_sensor, localizacao, 'termometro')
        self.temperatura = temperatura

    def get_temperatura(self):
        return temperatura

    def set_temperatura(self, temperatura) -> NONE:
        self.temperatura = temperatura


class Lampada(SensorGenerico):

    estado: int = 0

    def __init__(self, server, server_port, id_sensor, estado: int):
        super().__init__(server, server_port, id_sensor)
        self.estado = estado

    def get_estado(self):
        return self.estado

    def liga(self):
        self.estado = 1

    def desliga(self):
        self.estado = 0


class ArCondicionado(SensorGenerico):

    temperatura: float = 0.0
    estado = 0

    def __init__(self, id_sensor: int, temperatura: float, estado: int, localizacao: str):
        super().__init__(id_sensor, localizacao, 'arcondicionado')
        self.temperatura = temperatura
        self.estado = estado
        self.localizacao = localizacao

    def liga(self):
        self.estado = 1

    def desliga(self):
        self.estado = 0

    def get_temperatura(self) -> float:
        return self.temperatura

    def set_temperatura(self, temperatura):
        self.temperatura = temperatura




