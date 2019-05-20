sensores = {}

for i in range(1, 10):
    sensores[i] = {'nome': 'qualuqer', 'local': 'teste'}

for sensor in sensores:
    print(sensores[sensor]['nome'])