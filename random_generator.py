import random
import math

dict = {}
def linterp(x,y,x1):
    for i,xn in enumerate(x):
        if x1<xn:
            if (i==0):
                return y[0]
            else:
                return y[i-1] + (y[i]-y[i-1]) * (x1-x[i-1]) / (xn - x[i-1])
    return y[len(y)-1]

for i in range(8,300):
    dict[i] = 0
math.floor(2.5)

l = []
under_160 = 0

NPCnormalX = list(map(lambda x: x/50, range(0,214)))
NPCnormalY = list(map(lambda x: (math.e **(-x**2/2))/math.sqrt(2*math.pi), NPCnormalX))
_sum=0
NPCnormalY2=[]
for y in NPCnormalY:
    NPCnormalY2.append(_sum)
    _sum+=y
NPCnormalY2 = list(map(lambda x: x/_sum, NPCnormalY2))

x = 1

for i in range(x):
    #print(math.floor(8*(1+2*random.random())))
    num = int((1+7 * linterp(NPCnormalY2,NPCnormalX, random.random())) * 8)
    if num>100:
       under_160 += 1 
    dict[num] += 1

for index in range(12):
    l.append([])
    for i in range(4):
        l[index].append(math.floor(8*(1+2*random.random())))


matrix = []
for i in range(5):
    matrix.append([])

print(matrix)
print(l)
print(dict)
print("Numbers over: ", under_160)
print("Numbers under: ", x - under_160)