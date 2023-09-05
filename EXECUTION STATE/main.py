import tkinter as tk
import pickle
import os

# Función para tomar un checkpoint del juego
def tomar_checkpoint(tablero, turno):
    estado = {'tablero': tablero, 'turno': turno}
    with open('checkpoint.pkl', 'wb') as archivo:
        pickle.dump(estado, archivo)

# Función para cargar un checkpoint y restaurar el estado del juego
def cargar_checkpoint():
    try:
        with open('checkpoint.pkl', 'rb') as archivo:
            estado = pickle.load(archivo)
        return estado['tablero'], estado['turno']
    except FileNotFoundError:
        return [[' ' for _ in range(3)] for _ in range(3)], 'X'

# Función para verificar si hay un ganador
def hay_ganador(tablero):
    # Comprobar filas, columnas y diagonales
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != ' ':
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != ' ':
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != ' ':
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != ' ':
        return True
    return False

# Función para manejar el clic en un botón del tablero
def hacer_movimiento(i, j):
    global turno  # Declarar 'turno' como una variable global
    if tablero[i][j] == ' ' and not hay_ganador(tablero):
        tablero[i][j] = turno
        actualizar_tablero()
        if hay_ganador(tablero):
            mensaje.config(text=f'¡Jugador {turno} gana!')
        elif ' ' not in tablero[0] + tablero[1] + tablero[2]:
            mensaje.config(text='¡Empate!')
        else:
            turno = 'X' if turno == 'O' else 'O'
            tomar_checkpoint(tablero, turno)

# Función para actualizar la interfaz gráfica del tablero
def actualizar_tablero():
    for i in range(3):
        for j in range(3):
            botones[i][j].config(text=tablero[i][j])

# Función para iniciar un nuevo juego
def nuevo_juego():
    global tablero, turno
    tablero = [[' ' for _ in range(3)] for _ in range(3)]
    turno = 'X'
    actualizar_tablero()
    mensaje.config(text='')
    if os.path.exists('checkpoint.pkl'):
        os.remove('checkpoint.pkl')

# Crear la ventana principal
ventana = tk.Tk()
ventana.title('Triqui')

# Cargar el estado del juego desde un checkpoint o iniciar uno nuevo
tablero, turno = cargar_checkpoint()

# Crear los botones del tablero
botones = []
for i in range(3):
    fila = []
    for j in range(3):
        boton = tk.Button(ventana, text=tablero[i][j], width=10, height=3, command=lambda i=i, j=j: hacer_movimiento(i, j))
        boton.grid(row=i, column=j)
        fila.append(boton)
    botones.append(fila)

# Etiqueta para mostrar el mensaje de resultado
mensaje = tk.Label(ventana, text='', font=('Helvetica', 16))
mensaje.grid(row=3, column=0, columnspan=3)

# Botón para comenzar un nuevo juego
nuevo_juego_button = tk.Button(ventana, text='Nuevo Juego', command=nuevo_juego)
nuevo_juego_button.grid(row=4, column=0)

# Botón para reiniciar el juego y eliminar el checkpoint
def reiniciar_juego():
    nuevo_juego()
    if os.path.exists('checkpoint.pkl'):
        os.remove('checkpoint.pkl')

reiniciar_juego_button = tk.Button(ventana, text='Reiniciar Juego', command=reiniciar_juego)
reiniciar_juego_button.grid(row=4, column=1)

# Iniciar la ventana
ventana.mainloop()
