import sched, time
from random import randint, random, randrange
import datetime

sensores = {}

s = sched.scheduler(time.time, time.sleep)

for i in range(1, 10):
    sensores[i] = {'nome': 'qualuqer', 'local': 'teste'}

def funcao():
    for sensor in sensores:
        print(random()*10)
    #s.enter(5, 1, funcao)


datahora = datetime.datetime.now().second

hora = '19:30:21'

h, m, s = hora.split(':')

print(h,m,int(s)+30)

#hora = datetime.timedelta()

#print(datahora)

#print(datetime.timedelta(seconds=10).seconds)






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