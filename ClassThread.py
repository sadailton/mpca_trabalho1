import threading


class MinhaThread (threading.Thread):

    def __init__(self, nome: str, target, args):

        super().__init__(target=target, args=args, name=nome)




