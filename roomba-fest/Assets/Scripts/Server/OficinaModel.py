import numpy as np

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

import Agents

DEBUG = False

#Nombre: getGrid
#Parametros: un model.
#Return: Nada
#Se encarga de crear una representación visual del estado actual de la cuadrícula en el modelo
def getGrid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for x in range(model.grid.width):
        for y in range(model.grid.height):
            if not model.grid.is_cell_empty((x, y)):
                contents = model.grid.get_cell_list_contents((x, y))
                if any(isinstance(agent, Agents.Basura) for agent in contents):
                    grid[x][y] = 2  # Asignar 1 si hay una basura en la celda
                elif any(isinstance(agent, Agents.AgenteRobot) for agent in contents):
                    grid[x][y] = 4  # Asignar 2 si hay un agente robot en la celda
                elif any(isinstance(agent, Agents.Obstaculo) for agent in contents):
                    grid[x][y] = 1  # Asignar 3 si hay un agente obstaculo en la celda
                elif any(isinstance(agent, Agents.Papelera) for agent in contents):
                    grid[x][y] = 3  # Asignar 5 si hay un agente papelera en la celda
            else:
                grid[x][y] = 0  # Celda vacía
    return grid

def generate_test_grid(width = 10, height = 10, wall_percentage=0.2, max_garbage_per_cell=8, min_empty_cells = 0.5):
    test_grid = np.random.choice(max_garbage_per_cell,width*height).astype("str")
    min_empty_cells = int(round(min_empty_cells * (width * height)))
    wall_qty = int(round(wall_percentage * (width * height)))
    for _ in range(wall_qty): test_grid[_] = "X"
    for _ in range(wall_qty, min_empty_cells): test_grid[_] = "0"
    test_grid[0] = "P"
    np.random.shuffle(test_grid)
    test = test_grid.reshape(width,height)
    return test, np.argwhere(test=="P")[0]


class OficinaModel(Model):
    def __init__(self, width, height, num_agents = 5):
        super().__init__()
        self.cells = np.zeros((width, height))
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.currentStep = 0
        self.numBasuraTotal = 0
        self.basuraRestante = 0
        self.width = width
        self.height = height
        self.initial_grid, self.papelera_coords = generate_test_grid(width=width, height=height)

        self.datacollector = DataCollector(model_reporters = {"Grid": "initial_grid", "TrashBin": "papelera_coords" , "GridStatus": getGrid}, 
                                           agent_reporters = {"Position": "pos", "Carrying": "carrying" })

        obstaculo_id = 0
        basura_id = 0
        for i in range(width):
            for j in range(height):
                if self.initial_grid[i][j] == 'X':
                    new_obstaculo = Agents.Obstaculo(obstaculo_id, self)
                    self.grid.place_agent(new_obstaculo, (i, j))
                    obstaculo_id += 1
                elif self.initial_grid[i][j] == 'P':
                    new_papelera = Agents.Papelera(1, self)
                    self.papelera_coords = (i, j)
                    self.grid.place_agent(new_papelera, (i, j))
                    if DEBUG:
                        print(f'La papelera fue colocada en: {(i,j)} y su ubicacion correcta es: {self.papelera_coords}')
                elif self.initial_grid[i][j].isdigit():
                    num = int(self.initial_grid[i][j])  # Cantidad de basura
                    for _ in range(num):
                        new_basura = Agents.Basura(basura_id, self, num)
                        self.grid.place_agent(new_basura, (i, j))
                        basura_id += 1
                        self.numBasuraTotal += 1
                    if DEBUG:
                        print(f'Basura colocada en: {(i,j)} con una cantidad de: {num}')

        for i in range(self.num_agents):
            empty_positions = self.grid.empties
            if empty_positions:
                position = self.random.choice(list(empty_positions))
                agent = Agents.AgenteRobot(i, self)
                self.grid.place_agent(agent, position)
                self.schedule.add(agent)

    def allAgentsEmpty(self):
        empty = all(agent.carrying == 0 for agent in self.schedule.agents if isinstance(agent, Agents.AgenteRobot))
        if DEBUG: print(f'Agentes vacíos: {empty}')
        return empty


    #def allCellClean(self):
    #self.basuraRestante = sum(isinstance(agent, Agents.Basura) for agent in self.schedule.agents)
    #print(f'Basura restaste es: {self.basuraRestante}')
    #if (self.numBasuraTotal - self.basuraRestante) == 0:
    #return True

    def allCellClean(self):
        self.basuraRestante = sum(isinstance(obj, Agents.Basura) for cell in self.grid.coord_iter() for obj in cell[0])
        if DEBUG: print(f'Basura restante es: {self.basuraRestante}')
        return self.basuraRestante == 0

    def SimulationDone(self):
        if self.allCellClean() and self.allAgentsEmpty():
            return True
        else:
            return False

    def SimulationDonecomprobation(self):
        all_clean = self.allCellClean()
        all_empty = self.allAgentsEmpty()
        if DEBUG: print(f'SimulationDone -> all_clean: {all_clean}, all_empty: {all_empty}')
        return all_clean and all_empty

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        if self.allCellClean() and self.allAgentsEmpty():
            if DEBUG: print(f'Todas las celdas están limpias y todos los robots han vaciado su basura en {self.currentStep} pasos.')
        self.currentStep += 1
        self.SimulationDonecomprobation()
