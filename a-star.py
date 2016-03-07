# coding=UTF8

import numpy
from heapq import *
import random

def heuristica(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(tablero, inicio, meta):
    posibilidades = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    conjuntoPosibilidades = set()
    vieneDe = {}
    costeReal = {inicio:0}
    valorHeuristico = {inicio:heuristica(inicio, meta)}
    conjunto = []
    heappush(conjunto, (valorHeuristico[inicio], inicio))  
    while conjunto:
        posicionActual = heappop(conjunto)[1]
        if posicionActual == meta:
            datos = []
            while posicionActual in vieneDe:
                datos.append(posicionActual)
                posicionActual = vieneDe[posicionActual]
            return datos
        conjuntoPosibilidades.add(posicionActual)
        for i, j in posibilidades:
            posicionInmediata = posicionActual[0] + i, posicionActual[1] + j    
            costoTentativo = costeReal[posicionActual] + heuristica(posicionActual, posicionInmediata)
            if 0 <= posicionInmediata[0] < tablero.shape[0]:
                if 0 <= posicionInmediata[1] < tablero.shape[1]:
                    if tablero[posicionInmediata[0]][posicionInmediata[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue  
            if posicionInmediata in conjuntoPosibilidades and costoTentativo >= costeReal.get(posicionInmediata, 0):
                continue
            if  costoTentativo < costeReal.get(posicionInmediata, 0) or posicionInmediata not in [i[1]for i in conjunto]:
                vieneDe[posicionInmediata] = posicionActual
                costeReal[posicionInmediata] = costoTentativo
                valorHeuristico[posicionInmediata] = costoTentativo + heuristica(posicionInmediata, meta)
                heappush(conjunto, (valorHeuristico[posicionInmediata], posicionInmediata))             
    return False
    
random.seed()
valorInicio =  (random.randint(0, 5), random.randint(0, 6))
valorFin =  (random.randint(0, 5), random.randint(0, 6))
valorBloqueo1 =  (random.randint(0, 5), random.randint(0, 6))
valorBloqueo2 =  (random.randint(0, 5), random.randint(0, 6))
valorBloqueo3 =  (random.randint(0, 5), random.randint(0, 6))
print "2.- Inicio: ", valorInicio
print "3.- Meta: ", valorFin
print "1.- Bloqueo 1: ", valorBloqueo1
print "1.- Bloqueo2: ", valorBloqueo2
print "1.- Bloqueo 3: ", valorBloqueo3
ejercicio6x7 = numpy.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]])
ejercicio6x7[valorBloqueo1[0]][valorBloqueo1[1]]= 1
ejercicio6x7[valorBloqueo2[0]][valorBloqueo2[1]]= 1
ejercicio6x7[valorBloqueo3[0]][valorBloqueo3[1]]= 1
ejercicio = ejercicio6x7
ejercicio[valorInicio[0]][valorInicio[1]]= 2
ejercicio[valorFin[0]][valorFin[1]]= 3
print ejercicio    
print astar(ejercicio6x7, valorFin, valorInicio)

