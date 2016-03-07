# coding=UTF8

from Tkinter import Tk, Button
from tkFont import Font
from copy import deepcopy

# Clase Tablero
class Tablero:

  # Funcion para declarar los componentes del juego.
  def __init__(self,other=None):
    self.jugador = 'X'
    self.oponente = 'O'
    self.vacio = ' '
    self.size = 3
    self.casillas = {}
    # Crear las casillas definidas en el arreglo Casillas.
    for y in range(self.size):
      for x in range(self.size):
        self.casillas[x,y] = self.vacio
    # Crea una copia exacta del elemento para su análisis y comparación más adelante.
    if other:
      self.__dict__ = deepcopy(other.__dict__)

  # Declarar la fución movimiento que determina los pasos a seguir del jugador vs oponente.
  def movimiento(self,x,y):
    tablero = Tablero(self)
    tablero.casillas[x,y] = tablero.jugador
    (tablero.jugador,tablero.oponente) = (tablero.oponente,tablero.jugador)
    return tablero

  # Decarar la función para generar el árbol de decisiones en torno al primer movimiento que genera el usuario.
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

  # Declarar el método para identificar el siguiente mejor paso en función al arbol creado en _minimax.
  def mejor(self):
    return self.__minimax(True)[1]

  # Declarar el método para identificar el empate de acuerdo con el árbol de decisiones creado en _minimax.
  def empate(self):
    # Ciclo para identificar si existen casillas vacias.
    for (x,y) in self.casillas:
      # Si existe una casilla vacía, entonces lanza un False, de lo contrario lanza un True
      if self.casillas[x,y]==self.vacio:
        return False
    return True

  # Declarar el método para identificar el ganador de acuerdo con el árbol de decisiones creado en _minimax.
  def ganador(self):
    # Ciclo para revisar si existe un ganador de manera horizontal.
    for y in range(self.size):
      ganando = []
      for x in range(self.size):
        if self.casillas[x,y] == self.oponente:
          ganando.append((x,y))
      if len(ganando) == self.size:
        return ganando
    # Ciclo para revisar si existe un ganador de manera vertical.
    for x in range(self.size):
      ganando = []
      for y in range(self.size):
        if self.casillas[x,y] == self.oponente:
          ganando.append((x,y))
      if len(ganando) == self.size:
        return ganando
    ganando = []
    # Ciclo para revisar si existe un ganador de manera diagonal.
    for y in range(self.size):
      x = y
      if self.casillas[x,y] == self.oponente:
        ganando.append((x,y))
    # Comparar el tamaño del arreglo ganando, si es igual a size=3, entonces regresa la condición ganando.
    if len(ganando) == self.size:
      return ganando
    # Se limpia el arreglo.
    ganando = []
    # Ciclo para determinar si el que gano fue el oponente (IA).
    for y in range(self.size):
      x = self.size-1-y
      if self.casillas[x,y] == self.oponente:
        ganando.append((x,y))
    # Comparar el tamaño del arreglo ganando, si es igual a size=3, entonces regresa la condición ganando.
    # Una vez revisado el oponente, si no fue el gnador, entonces gana el jugador.
    if len(ganando) == self.size:
      return ganando
    return None

  # 
  def __str__(self):
    cadena = ''
    for y in range(self.size):
      for x in range(self.size):
        cadena+=self.casillas[x,y]
      cadena+="\n"
    return cadena
 
# Clase Juego
class Juego:

  # Declarar el constructor de la clase Juego.
  def __init__(self):
    self.app = Tk()
    self.app.title('# Gatito #')
    self.app.resizable(width=True, height=True)
    self.tablero = Tablero()
    self.font = Font(family="Roboto", size=34)
    self.botones = {}
    # Ciclo para crear los objetos botón para posteriormente asignarlos en el Juego.
    for x,y in self.tablero.casillas:
      manejador = lambda x=x,y=y: self.movimiento(x,y)
      boton = Button(self.app, command=manejador, font=self.font, width=2, height=1)
      boton.grid(row=y, column=x)
      self.botones[x,y] = boton
    manejador = lambda: self.reiniciar()
    boton = Button(self.app, text='Reiniciar', command=manejador)
    boton.grid(row=self.tablero.size+1, column=0, columnspan=self.tablero.size, sticky="WE")
    self.actualizar() 

  # Declarar el método Reiniciar que será asignada al botón Reiniciar en el Juego.
  def reiniciar(self):
    self.tablero = Tablero()
    self.actualizar() 

  # Declarar la función movimiento que revisará los click's realizados por el usuario y los movimientos realizados por el oponente (IA).
  def movimiento(self,x,y):
    self.app.config(cursor="watch")
    self.app.update()
    self.tablero = self.tablero.movimiento(x,y)
    self.actualizar()
    movimiento = self.tablero.mejor()
    # Si se detecta un movimiento en el Juego, entonces el oponente realizara el siguiente movimiento en base al árbol creado en _minimax.
    # Después ejecutara el método actualizar y regresara el cursor al jugador para el siguiente movimiento.
    if movimiento:
      self.tablero = self.tablero.movimiento(*movimiento)
      self.actualizar()
    self.app.config(cursor="")

  # Declarar el método Actualizar que realizará 
  def actualizar(self):
    # 
    for (x,y) in self.tablero.casillas:
      text = self.tablero.casillas[x,y]
      self.botones[x,y]['text'] = text
      self.botones[x,y]['disabledforeground'] = 'black'
      # 
      if text==self.tablero.vacio:
        self.botones[x,y]['state'] = 'normal'
      else:
        self.botones[x,y]['state'] = 'disabled'
    ganando = self.tablero.ganador()
    # 
    if ganando:
      for x,y in ganando:
        self.botones[x,y]['disabledforeground'] = 'red'
      for x,y in self.botones:
        self.botones[x,y]['state'] = 'disabled'
    for (x,y) in self.tablero.casillas:
      self.botones[x,y].update()
  
  # Declarar el método Principal donde se inicializa el objeto app.
  def principal(self):
    self.app.mainloop()

# Método main del programa donde se inicializa la clase Juego y el método principal para indicar 
if __name__ == '__main__':
  Juego().principal()