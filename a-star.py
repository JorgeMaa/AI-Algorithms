# coding=UTF8

# 
import numpy
# 
from heapq import *
# Formula para determinar el valor heuristico
def heuristica(a, b):
    # 
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
# Funcion principal, requiere tres parámetros, el tablero, la posicion de inicio y la posicion de meta
def astar(tablero, inicio, meta):
    # 
    posibilidades = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    # 
    conjuntoPosibilidades = set()
    # 
    vieneDe = {}
    # 
    costeReal = {inicio:0}
    # 
    valorHeuristico = {inicio:heuristica(inicio, meta)}
    # 
    conjunto = []
    # 
    heappush(conjunto, (valorHeuristico[inicio], inicio))  
    #   
    while conjunto:
        # 
        posicionActual = heappop(conjunto)[1]
        # 
        if posicionActual == meta:
            # 
            datos = []
            # 
            while posicionActual in vieneDe:
                # 
                datos.append(posicionActual)
                # 
                posicionActual = vieneDe[posicionActual]
            # 
            return datos
        # 
        conjuntoPosibilidades.add(posicionActual)
        # 
        for i, j in posibilidades:
            # 
            posicionInmediata = posicionActual[0] + i, posicionActual[1] + j
            #          
            costoTentativo = costeReal[posicionActual] + heuristica(posicionActual, posicionInmediata)
            # 
            if 0 <= posicionInmediata[0] < tablero.shape[0]:
                # 
                if 0 <= posicionInmediata[1] < tablero.shape[1]:
                    # 
                    if tablero[posicionInmediata[0]][posicionInmediata[1]] == 1:
                        # 
                        continue
                # 
                else:
                    # 
                    continue
            # 
            else:
                # 
                continue
            #             
            if posicionInmediata in conjuntoPosibilidades and costoTentativo >= costeReal.get(posicionInmediata, 0):
                # 
                continue
            # 
            if  costoTentativo < costeReal.get(posicionInmediata, 0) or posicionInmediata not in [i[1]for i in conjunto]:
                # 
                vieneDe[posicionInmediata] = posicionActual
                # 
                costeReal[posicionInmediata] = costoTentativo
                # 
                valorHeuristico[posicionInmediata] = costoTentativo + heuristica(posicionInmediata, meta)
                # 
                heappush(conjunto, (valorHeuristico[posicionInmediata], posicionInmediata))                
    # 
    return False
# 
ejercicio6x7 = numpy.array([
    [0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0]])
# 
print ejercicio6x7    
# Imprimir el conunto de pasos para llegar a la Meta...
print astar(ejercicio6x7, (5,6), (0,2))
