import threading


class MinhaThread (threading.Thread):

    def __init__(self, threadID: int, nome: str):

        super().__init__()
        self.threadID = threadID
        self.name = nome

    def run(self):
        print("Iniciando thread {}".format(self.nome))

