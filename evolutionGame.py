import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

population = np.random.randint(0, 2, (50, 50))


class Organismo:
    def __init__(self, longitud_adn):
        self.adn = [random.randint(0, 1) for _ in range(longitud_adn)]

def crear_population_inicial(num_organismos, longitud_adn):
    population = []
    for _ in range(num_organismos):
        population.append(Organismo(longitud_adn))
    return population

def reproducir(organismo1, organismo2):
    # tomamos una posición aleatoria de la cadena de ADN
    punto_cruce = random.randint(1, len(organismo1.adn) - 1)

    # creamos el nuevo organismo combinando las porciones de ADN de cada organismo
    nuevo_adn = organismo1.adn[:punto_cruce] + organismo2.adn[punto_cruce:]
    nuevo_organismo = Organismo(len(nuevo_adn))
    nuevo_organismo.adn = nuevo_adn

    return nuevo_organismo

def seleccion_natural(population, num_descendientes):
    # calculamos la aptitud de cada organismo
    aptitudes = [sum(organismo.adn) for organismo in population]

    # seleccionamos a los organismos más aptos
    seleccionados = []
    for _ in range(num_descendientes):
        # elegimos un organismo aleatoriamente, con mayor probabilidad de ser seleccionado si tiene mayor aptitud
        seleccionado = random.choices(population, weights=aptitudes)[0]
        seleccionados.append(seleccionado)

    return seleccionados

def count_neighbors(population, row, col):
    num_rows, num_cols = population.shape
    count = 0
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if i == row and j == col:
                continue
            if i < 0 or i >= num_rows:
                continue
            if j < 0 or j >= num_cols:
                continue
            count += population[i, j]
    return count


def evolucionar(population_inicial, num_generaciones, num_descendientes):
    population_actual = population_inicial
    for _ in range(num_generaciones):
        # seleccionamos los organismos que tendrán descendencia en la siguiente generación
        descendientes = []
        for _ in range(num_descendientes):
            # elegimos dos organismos aleatorios de la población actual y los hacemos reproducir
            organismo1, organismo2 = random.sample(population_actual, 2)
            descendientes.append(reproducir(organismo1, organismo2))

        # reemplazamos la población actual con los descendientes
        population_actual = descendientes

    return population_actual

# Definir la función update_population
def update_population(population):
    new_population = np.zeros_like(population)
    rows, cols = population.shape
    for row in range(rows):
        for col in range(cols):
            neighbors = count_neighbors(population, row, col)
            if population[row, col] == 1:
                if neighbors in [2, 3]:
                    new_population[row, col] = 1
            else:
                if neighbors == 3:
                    new_population[row, col] = 1
    return new_population

# Asignar un valor a num_generations
num_generations = 100


population_inicial = crear_population_inicial(100, 10)
population_final = evolucionar(population_inicial, 10, 50)

# imprimimos la cadena de ADN de cada organismo en la población final
for organismo in population_final:
    print(organismo.adn)



# Crear una figura y un conjunto de ejes
fig = plt.figure()
ax = fig.add_subplot(111)

# Función que actualiza la trama en cada cuadro de la animación
def update(frame):
    global population
    ax.clear()
    ax.imshow(population, cmap='binary', vmin=0, vmax=1)
    ax.set_title(f'Generación {frame}')

    # Actualizar la población
    population = update_population(population)

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=num_generations, interval=150)

# Mostrar la barra de color
cax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.set_frame_on(False)
cax.imshow([[0, 1]], cmap='binary', vmin=0, vmax=1, aspect='auto')
cax.set_title('Estado de la célula')

# Mostrar la animación
plt.show()

