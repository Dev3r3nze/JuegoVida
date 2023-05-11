import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Creamos la matriz inicial del juego de la vida
def initial_board(N):
    board = np.zeros((N, N))
    # Definimos algunos patrones iniciales aleatorios
    num_points = N * N // 10
    random_row = np.random.randint(0, N, size=num_points)
    random_col = np.random.randint(0, N, size=num_points)
    board[random_row, random_col] = 1

    # Mostrar el valor de la matriz
    print(random_row, random_col)

    # Definimos algunos patrones iniciales
    #board[4, 4] = 1
    #board[4, 5] = 1
    #board[4, 3] = 1
    #board[5, 4] = 1
    #board[5, 5] = 1
    #board[3, 4] = 1
    #board[4, 5] = 1
    return board

# Aplicamos las reglas del juego de la vida para calcular el siguiente estado de la matriz
def update(frameNum, img, board, N):
    new_board = board.copy()
    for i in range(N):
        for j in range(N):
            # Contamos el número de vecinos vivos
            vecinos = board[(i-1) % N, (j-1) % N] + board[(i-1) % N, j] + board[(i-1) % N, (j+1) % N] + \
                      board[i, (j-1) % N] + board[i, (j+1) % N] + \
                      board[(i+1) % N, (j-1) % N] + board[(i+1) % N, j] + board[(i+1) % N, (j+1) % N]
            # Aplicamos las reglas
            if board[i, j] == 1 and (vecinos < 2 or vecinos > 3):
                new_board[i, j] = 0
            elif board[i, j] == 0 and vecinos == 3:
                new_board[i, j] = 1
    # Actualizamos la matriz
    board[:] = new_board[:]
    # Actualizamos la imagen
    img.set_data(board)
    return img,

# Definimos los parámetros del juego
N = 200 # Tamaño de la matriz
interval = 50 # Intervalo de tiempo entre frames en ms

# Creamos la figura
fig, ax = plt.subplots()
board = initial_board(N)
img = ax.imshow(board, cmap='binary')
ani = animation.FuncAnimation(fig, update, fargs=(img, board, N), frames=100, interval=interval, save_count=50)

# Mostramos la animación
plt.show()
