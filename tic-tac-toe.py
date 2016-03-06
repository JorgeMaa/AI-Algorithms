# coding=UTF8

# 
from Tkinter import Tk, Button
# 
from tkFont import Font
# 
from copy import deepcopy
# 
class Tablero:
  # 
  def __init__(self,other=None):
    # 
    self.jugador = 'X'
    # 
    self.oponente = 'O'
    # 
    self.vacio = ' '
    # 
    self.size = 3
    # 
    self.casillas = {}
    # 
    for y in range(self.size):
      # 
      for x in range(self.size):
        # 
        self.casillas[x,y] = self.vacio
    # copy constructor
    if other:
      # 
      self.__dict__ = deepcopy(other.__dict__)
  # 
  def movimiento(self,x,y):
    # 
    tablero = Tablero(self)
    # 
    tablero.casillas[x,y] = tablero.jugador
    # 
    (tablero.jugador,tablero.oponente) = (tablero.oponente,tablero.jugador)
    # 
    return tablero
  # 
  def __minimax(self, jugador):
    # 
    if self.ganador():
      # 
      if jugador:
        # 
        return (-1,None)
      # 
      else:
        # 
        return (+1,None)
    # 
    elif self.empate():
      # 
      return (0,None)
    # 
    elif jugador:
      # 
      mejor = (-2,None)
      # 
      for x,y in self.casillas:
        # 
        if self.casillas[x,y]==self.vacio:
          # 
          valor = self.movimiento(x,y).__minimax(not jugador)[0]
          # 
          if valor>mejor[0]:
            # 
            mejor = (valor,(x,y))
            # 
      return mejor
    # 
    else:
      # 
      mejor = (+2,None)
      # 
      for x,y in self.casillas:
        # 
        if self.casillas[x,y]==self.vacio:
          # 
          valor = self.movimiento(x,y).__minimax(not jugador)[0]
          # 
          if valor<mejor[0]:
            # 
            mejor = (valor,(x,y))
      # 
      return mejor
  # 
  def mejor(self):
    # 
    return self.__minimax(True)[1]
  # 
  def empate(self):
    # 
    for (x,y) in self.casillas:
      # 
      if self.casillas[x,y]==self.vacio:
        # 
        return False
    # 
    return True
  # 
  def ganador(self):
    # horizontal
    for y in range(self.size):
      # 
      ganando = []
      # 
      for x in range(self.size):
        # 
        if self.casillas[x,y] == self.oponente:
          # 
          ganando.append((x,y))
      # 
      if len(ganando) == self.size:
        # 
        return ganando
    # vertical
    for x in range(self.size):
      # 
      ganando = []
      # 
      for y in range(self.size):
        # 
        if self.casillas[x,y] == self.oponente:
          # 
          ganando.append((x,y))
      # 
      if len(ganando) == self.size:
        # 
        return ganando
    # diagonal
    ganando = []
    # 
    for y in range(self.size):
      # 
      x = y
      # 
      if self.casillas[x,y] == self.oponente:
        # 
        ganando.append((x,y))
    # 
    if len(ganando) == self.size:
      # 
      return ganando
    # other diagonal
    ganando = []
    # 
    for y in range(self.size):
      # 
      x = self.size-1-y
      # 
      if self.casillas[x,y] == self.oponente:
        # 
        ganando.append((x,y))
    # 
    if len(ganando) == self.size:
      # 
      return ganando
    # default
    return None
  # 
  def __str__(self):
    # 
    cadena = ''
    # 
    for y in range(self.size):
      # 
      for x in range(self.size):
        # 
        cadena+=self.casillas[x,y]
      # 
      cadena+="\n"
    # 
    return cadena
 
# Clase para la interfaz gráfica
class Juego:
  # Definicion del constructor
  def __init__(self):
    # Inicializar la clase Tk de la librería Tkinter
    self.app = Tk()
    # Definir parámetro Título
    self.app.title('# Gatito #')
    # Definir posiilidad de reajustar el tamaño de la ventana
    self.app.resizable(width=True, height=True)
    # Inicializar la clase Tablero dentro de la clase Juego
    self.tablero = Tablero()
    # Definir el tipo de fuente
    self.font = Font(family="Roboto", size=34)
    # Inicializar el arreglo de botones
    self.botones = {}
    # Ciclo para crear el arreglo de botones que se usaran como Juego (Recurrente)
    for x,y in self.tablero.casillas:
      # Manejador encargado de verificar el movimiento realizado por el usuario
      # para determinar la mejor estrategía en base a la clase Tablero
      manejador = lambda x=x,y=y: self.movimiento(x,y)
      # Define el objeto botón con los parámetros ateriores
      boton = Button(self.app, command=manejador, font=self.font, width=2, height=1)
      # Define la posición en la tabla que ocupará el botón
      boton.grid(row=y, column=x)
      # Incluye el botón creado en el arreglo de botónes
      self.botones[x,y] = boton
    # Se asigna el manejador para su uso como botón Reiniciar
    manejador = lambda: self.reiniciar()
    # Se define el botón Reiniciar con los parámetros correspondientes
    boton = Button(self.app, text='Reiniciar', command=manejador)
    # Asignar el botón Reiniciar al Juego
    boton.grid(row=self.tablero.size+1, column=0, columnspan=self.tablero.size, sticky="WE")
    # Ejecutar el método Actualizar
    self.actualizar() 
 # Definición del método Reiniciar
  def reiniciar(self):
    # Inicializa el objeto tablero dentro de la clase Juego
    self.tablero = Tablero()
    # Ejecuta el método Actualizar
    self.actualizar() 
  # Definición del método Movimiento
  def movimiento(self,x,y):
    # 
    self.app.config(cursor="watch")
    # 
    self.app.update()
    # 
    self.tablero = self.tablero.movimiento(x,y)
    # 
    self.actualizar()
    # 
    movimiento = self.tablero.mejor()
    # 
    if movimiento:
      # 
      self.tablero = self.tablero.movimiento(*movimiento)
      # 
      self.actualizar()
      # 
    self.app.config(cursor="")
  # 
  def actualizar(self):
    # 
    for (x,y) in self.tablero.casillas:
      # 
      text = self.tablero.casillas[x,y]
      # 
      self.botones[x,y]['text'] = text
      # 
      self.botones[x,y]['disabledforeground'] = 'black'
      # 
      if text==self.tablero.vacio:
        # 
        self.botones[x,y]['state'] = 'normal'
      # 
      else:
        # 
        self.botones[x,y]['state'] = 'disabled'
    # 
    ganando = self.tablero.ganador()
    # 
    if ganando:
      # 
      for x,y in ganando:
        # 
        self.botones[x,y]['disabledforeground'] = 'red'
      # 
      for x,y in self.botones:
        # 
        self.botones[x,y]['state'] = 'disabled'
    # 
    for (x,y) in self.tablero.casillas:
      # 
      self.botones[x,y].update()
  # 
  def mainloop(self):
    # 
    self.app.mainloop()
# 
if __name__ == '__main__':
  # 
  Juego().mainloop()