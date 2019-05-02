import socket


class Servidor:

    HOST: str = ''
    PORT: int = 0
    TCP_SOCKET: socket = ''

    def __init__(self, host_ip: str, host_port: int, num_conexoes: int):

        self.HOST = host_ip
        self.PORT = host_port

        self.TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.TCP_SOCKET.bind((self.HOST, self.PORT))
        self.TCP_SOCKET.listen(num_conexoes)

    def cria_conexao(self) -> tuple:

        return self.TCP_SOCKET.accept()

    def fecha_conexao(self):
        self.TCP_SOCKET.close()
