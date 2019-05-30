import sched, time
from random import randint, random, randrange
import datetime
import re

sensores = {}

s = sched.scheduler(time.time, time.sleep)

for i in range(1, 10):
    sensores[i] = {'nome': 'qualuqer', 'local': 'teste'}

def funcao():
    for sensor in sensores:
        print(random()*10)
    #s.enter(5, 1, funcao)



#hora = datetime.timedelta()

#print(datahora)

#print(datetime.timedelta(seconds=10).seconds)

def valida_ip(endereco_ip: str):
    m = re.match('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))', endereco_ip)

    if m:
        return True
    else:
        return False


while True:
    endip = input('IP: ')

    print(valida_ip(endip))

'''
while True:
    start = time.time()

    x = input("Digite alguma coisa: ")
    print(x)

    end = time.time()

    print("Demorou {}".format(end - start))
'''

#s.enter(3,1,funcao)
#s.run()