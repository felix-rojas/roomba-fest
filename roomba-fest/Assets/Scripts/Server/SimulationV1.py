# -*- coding: utf-8 -*-

import numpy as np

import Prereqs
import OficinaModel

Prereqs.get_packages()


def generate_test_grid(width=10, height=10, wall_percentage=0.2, max_garbage_per_cell=8, min_empty_cells=0.5):
    test_grid = np.random.choice(max_garbage_per_cell, width * height).astype("str")
    min_empty_cells = int(round(min_empty_cells * (width * height)))
    wall_qty = int(round(wall_percentage * (width * height)))
    for _ in range(wall_qty): test_grid[_] = "X"
    for _ in range(wall_qty, min_empty_cells): test_grid[_] = "0"
    test_grid[0] = "P"
    np.random.shuffle(test_grid)
    test = test_grid.reshape(width, height)
    return test, np.argwhere(test == "P")[0]


# Commented out IPython magic to ensure Python compatibility.
# %%writefile grid.txt
# 6 5
# 0 4 X 6 0
# 6 X 0 X 4
# 0 X 7 X 0
# 5 0 0 X 8
# 0 0 X 0 0
# 0 0 0 0 P

"""# Global params"""

DEBUG = False
file_name = 'grid.txt'


def leer_grid(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        n, m = map(int, lineas[0].split())
        oficina_ = []
        papelera_pos_ = None
        for i in range(1, n + 1):
            fila = lineas[i].strip().split()
            oficina_.append(fila)
            if 'P' in fila:
                papelera_pos_ = (i - 1, fila.index('P'))
        return oficina_, papelera_pos_, n, m


# Llama a la función para leer el archivo
#OFICINA, PAPELERA_POS, alto, ancho = leer_grid(file_name)

ALTO = 5
ANCHO = 6
OFICINA, PAPELERA_POS = generate_test_grid(ANCHO, ALTO)
print(OFICINA)
print(PAPELERA_POS)

MAX_ITER = 2000
AGENT_NUM = 5
model = OficinaModel.OficinaModel(ANCHO, ALTO, AGENT_NUM)


def advanceSimulation():
    model.step()
    return model.datacollector.get_model_vars_dataframe()

# Obtenemos la informacion requerida para el analsis.
# all_grid = model.datacollector.get_model_vars_dataframe()
