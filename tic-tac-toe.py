# coding=UTF8

from Tkinter import Tk, Button
from tkFont import Font
from copy import deepcopy

class Tablero:

  def __init__(self,other=None):
    self.jugador = 'X'
    self.oponente = 'O'
    self.vacio = ' '
    self.size = 3
    self.casillas = {}
    for y in range(self.size):
      for x in range(self.size):
        self.casillas[x,y] = self.vacio
    if other:
      self.__dict__ = deepcopy(other.__dict__)

  def movimiento(self,x,y):
    tablero = Tablero(self)
    tablero.casillas[x,y] = tablero.jugador
    (tablero.jugador,tablero.oponente) = (tablero.oponente,tablero.jugador)
    return tablero

  def __minimax(self, jugador):
    if self.ganador():
      if jugador:
        return (-1,None)
      else:
        return (+1,None)
    elif self.empate():
      return (0,None)
    elif jugador:
      mejor = (-2,None)
      for x,y in self.casillas:
        if self.casillas[x,y]==self.vacio:
          valor = self.movimiento(x,y).__minimax(not jugador)[0]
          if valor>mejor[0]:
            mejor = (valor,(x,y))
      return mejor
    else:
      mejor = (+2,None)
      for x,y in self.casillas:
        if self.casillas[x,y]==self.vacio:
          valor = self.movimiento(x,y).__minimax(not jugador)[0]
          if valor<mejor[0]:
            mejor = (valor,(x,y))
      return mejor

  def mejor(self):
    return self.__minimax(True)[1]

  def empate(self):
    for (x,y) in self.casillas:
      if self.casillas[x,y]==self.vacio:
        return False
    return True

  def ganador(self):
    for y in range(self.size):
      ganando = []
      for x in range(self.size):
        if self.casillas[x,y] == self.oponente:
          ganando.append((x,y))
      if len(ganando) == self.size:
        return ganando
    for x in range(self.size):
      ganando = []
      for y in range(self.size):
        if self.casillas[x,y] == self.oponente:
          ganando.append((x,y))
      if len(ganando) == self.size:
        return ganando
    ganando = []
    for y in range(self.size):
      x = y
      if self.casillas[x,y] == self.oponente:
        ganando.append((x,y))
    if len(ganando) == self.size:
      return ganando
    ganando = []
    for y in range(self.size):
      x = self.size-1-y
      if self.casillas[x,y] == self.oponente:
        ganando.append((x,y))
    if len(ganando) == self.size:
      return ganando
    return None

  def __str__(self):
    cadena = ''
    for y in range(self.size):
      for x in range(self.size):
        cadena+=self.casillas[x,y]
      cadena+="\n"
    return cadena
 
class Juego:

  def __init__(self):
    self.app = Tk()
    self.app.title('# Gatito #')
    self.app.resizable(width=True, height=True)
    self.tablero = Tablero()
    self.font = Font(family="Roboto", size=34)
    self.botones = {}
    for x,y in self.tablero.casillas:
      manejador = lambda x=x,y=y: self.movimiento(x,y)
      boton = Button(self.app, command=manejador, font=self.font, width=2, height=1)
      boton.grid(row=y, column=x)
      self.botones[x,y] = boton
    manejador = lambda: self.reiniciar()
    boton = Button(self.app, text='Reiniciar', command=manejador)
    boton.grid(row=self.tablero.size+1, column=0, columnspan=self.tablero.size, sticky="WE")
    self.actualizar() 

  def reiniciar(self):
    self.tablero = Tablero()
    self.actualizar() 

  def movimiento(self,x,y):
    self.app.config(cursor="watch")
    self.app.update()
    self.tablero = self.tablero.movimiento(x,y)
    self.actualizar()
    movimiento = self.tablero.mejor()
    if movimiento:
      self.tablero = self.tablero.movimiento(*movimiento)
      self.actualizar()
    self.app.config(cursor="")

  def actualizar(self):
    for (x,y) in self.tablero.casillas:
      text = self.tablero.casillas[x,y]
      self.botones[x,y]['text'] = text
      self.botones[x,y]['disabledforeground'] = 'black'
      if text==self.tablero.vacio:
        self.botones[x,y]['state'] = 'normal'
      else:
        self.botones[x,y]['state'] = 'disabled'
    ganando = self.tablero.ganador()
    if ganando:
      for x,y in ganando:
        self.botones[x,y]['disabledforeground'] = 'red'
      for x,y in self.botones:
        self.botones[x,y]['state'] = 'disabled'
    for (x,y) in self.tablero.casillas:
      self.botones[x,y].update()

  def mainloop(self):
    self.app.mainloop()

if __name__ == '__main__':
  Juego().mainloop()