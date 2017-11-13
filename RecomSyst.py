#1 часть задания

import csv
import math

user = 22

def read(file): #считывание csv файла
    arr = []
    with open(file, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for str in reader:
            arr.append(str)
    return arr

data = read('data.csv')

def avrg(arr,user): #высчитывание средней оценки
    sum = 0
    cnt = 0
    for i in range(1, len(arr[user])):
        if int(arr[user][i]) != -1:
            cnt += 1
            sum += int(arr[user][i])
    return sum/cnt

def metrsim(arr, user1, user2): #рассчет метрики схожести
    u = 0
    v = 0
    uv = 0
    arrfilm = []
    for i in range(1, len(arr[0])):
        if (int(arr[user1][i]) != -1) and (int(arr[user2][i]) != -1):
            arrfilm.append(i)
    for x in arrfilm:
        u += math.pow(int(arr[user1][x]),2)
        v += math.pow(int(arr[user2][x]),2)
        uv += int(arr[user1][x]) * int(arr[user2][x])
    return uv /(math.sqrt(u)* math.sqrt(v))

def topKfilms(arrF, arrS, film, k): #поиск ближайших k фильмов 
    markfilms = {}
    for user, x in arrS.items():
        if int(arrF[user][film]) != -1:
            markfilms[user] = x
    top = sorted(markfilms, key = markfilms.__getitem__) #сортировка массива
    top.reverse()
    top = top[0:k] #выборка первых k
    return top


def marks(arr, user, k): #итоговая предполагаемая оценка по неоцененным фильмам
    avrgmarks = {} #суммирование средних оценок
    metrsims = {} #метрики схожести
    mark = {}  #результат
    for i in range(1, len(arr)):
        avrgmarks[i] = avrg(arr, i)
        if i != int(user):
            metrsims[i] = metrsim(arr, user, i)   
    for i in range(1, len(arr[0])):
        if int(arr[user][i]) == -1:        
            top = topKfilms(arr, metrsims, i, k)
            simmin = 0
            simvu = 0          
            for t in top:
                simvu += metrsims[t]
                simmin += metrsims[t] * (int(arr[t][i]) - avrgmarks[t])
            mark[i] = avrgmarks[user] + simmin / simvu
    return mark



context = read('context.csv')
newdata = read('data.csv')

for i in range(1, len(data)): #убираем из контекста все субботы и воскресения
    if i == user:
        continue
    for j in range(1, len(newdata[0])):
        if  context[i][j] == ' Sun' or context[i][j] == ' Sat':                   
                newdata[i][j] = '-1'

newmark = marks(newdata, user, 3)
newmark=dict(sorted(newmark.items(), key=lambda x: x[1], reverse=True)[:1]) #выбор фильма с наибольшим рейтингом


for nm in newmark:
    print('"movie"',nm,':',round(newmark[nm],3))
