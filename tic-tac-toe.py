# coding=UTF8
from Tkinter import Tk, Button
from tkFont import Font
from copy import deepcopy
 
class Tablero:
  def __init__(self,other=None):
    self.jugador = 'X'
    self.oponente = 'O'
    self.vacio = '.'
    self.size = 3
    self.casillas = {}
    for y in range(self.size):
      for x in range(self.size):
        self.casillas[x,y] = self.vacio
    # copy constructor
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
    # horizontal
    for y in range(self.size):
      ganando = []
      for x in range(self.size):
        if self.casillas[x,y] == self.oponente:
          ganando.append((x,y))
      if len(ganando) == self.size:
        return ganando
    # vertical
    for x in range(self.size):
      ganando = []
      for y in range(self.size):
        if self.casillas[x,y] == self.oponente:
          ganando.append((x,y))
      if len(ganando) == self.size:
        return ganando
    # diagonal
    ganando = []
    for y in range(self.size):
      x = y
      if self.casillas[x,y] == self.oponente:
        ganando.append((x,y))
    if len(ganando) == self.size:
      return ganando
    # other diagonal
    ganando = []
    for y in range(self.size):
      x = self.size-1-y
      if self.casillas[x,y] == self.oponente:
        ganando.append((x,y))
    if len(ganando) == self.size:
      return ganando
    # default
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
    self.font = Font(family="Helvetica", size=32)
    self.buttons = {}
    for x,y in self.tablero.casillas:
      handler = lambda x=x,y=y: self.movimiento(x,y)
      button = Button(self.app, command=handler, font=self.font, width=2, height=1)
      button.grid(row=y, column=x)
      self.buttons[x,y] = button
    handler = lambda: self.reset()
    button = Button(self.app, text='reset', command=handler)
    button.grid(row=self.tablero.size+1, column=0, columnspan=self.tablero.size, sticky="WE")
    self.update()
 
  def reset(self):
    self.tablero = Tablero()
    self.update()
 
  def movimiento(self,x,y):
    self.app.config(cursor="watch")
    self.app.update()
    self.tablero = self.tablero.movimiento(x,y)
    self.update()
    movimiento = self.tablero.mejor()
    if movimiento:
      self.tablero = self.tablero.movimiento(*movimiento)
      self.update()
    self.app.config(cursor="")
 
  def update(self):
    for (x,y) in self.tablero.casillas:
      text = self.tablero.casillas[x,y]
      self.buttons[x,y]['text'] = text
      self.buttons[x,y]['disabledforeground'] = 'black'
      if text==self.tablero.vacio:
        self.buttons[x,y]['state'] = 'normal'
      else:
        self.buttons[x,y]['state'] = 'disabled'
    ganando = self.tablero.ganador()
    if ganando:
      for x,y in ganando:
        self.buttons[x,y]['disabledforeground'] = 'red'
      for x,y in self.buttons:
        self.buttons[x,y]['state'] = 'disabled'
    for (x,y) in self.tablero.casillas:
      self.buttons[x,y].update()
 
  def mainloop(self):
    self.app.mainloop()
 
if __name__ == '__main__':
  Juego().mainloop()