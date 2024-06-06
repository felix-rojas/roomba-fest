from mesa import Agent
import heapq
import numpy as np

DEBUG = False


class Basura(Agent):
    def __init__(self, unique_id, model, cantidad):
        super().__init__(unique_id, model)
        self.qty = cantidad
        self.agents_on_top = None

    def notify(self, AgenteRobot):
        AgenteRobot.clean()

    def step(self):
        self.agents_on_top = model.grid.get_cell_list_contents([self.pos])

        if self.agents_on_top:
            for agent in self.agents_on_top:
                if isinstance(agent, AgenteRobot):
                    self.notify(agent)


class Obstaculo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Papelera(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.position = self.pos


def NewShuffle(arr):
    mutable_arr = [list(item) for item in arr]
    n = len(mutable_arr)
    for i in range(n - 1, 0, -1):
        j = np.random.randint(0, i)
        mutable_arr[i], mutable_arr[j] = mutable_arr[j], mutable_arr[i]

    # Convertir de nuevo a lista de tuplas
    return [tuple(item) for item in mutable_arr]


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        if current:
            total_path.append(current)
    total_path.reverse()
    return total_path


def heuristic(a, b):
    # manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_list:
        _, current = heapq.heappop(open_list)
        if np.all(current == goal):
            return reconstruct_path(came_from, current)
        neighbors = grid.get_neighborhood(current, moore=True, include_center=False)
        for neighbor in neighbors:
            if grid.out_of_bounds(neighbor):
                continue
            cell_contents = grid.get_cell_list_contents(neighbor)
            if any(isinstance(obj, Obstaculo) for obj in cell_contents):
                continue
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No se encontró ningún camino


#Nombre: AgenteRobot
#Parametros: Ninguno.
#Return: Nada
#Se encarga de servir como base para crear agentes de tipo aspiradora
class AgenteRobot(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.capacity = 5
        self.carrying = 0
        self.returning = False
        self.path_to_papelera = []
        self.steps_since_last_path_update = 0

    def almacenamiento(self):
        print(f'El robot {self.unique_id} tiene actualmente {self.carrying} unidades de basura')

    def clean(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        trash_in_cell = [obj for obj in cell_contents if isinstance(obj, Basura)]
        trash_count = len(trash_in_cell)
        if trash_count > 0:
            if trash_count <= (self.capacity - self.carrying):
                to_collect = trash_in_cell
            else:
                to_collect = trash_in_cell[:self.capacity - self.carrying]
            for trash in to_collect:
                self.model.grid.remove_agent(trash)
                self.carrying += 1
                if DEBUG:
                    print(
                        f"Robot {self.unique_id} recogió basura en {self.pos}. Almacenamiento: {self.carrying}/{self.capacity}")

    def empty(self):
        self.carrying = 0
        self.returning = False
        if DEBUG:
            print(f"Robot {self.unique_id} vació su contenido en la papelera.")

    def find_path_to_papelera(self):
        self.path_to_papelera = a_star_search(self.model.grid, self.pos, self.model.papelera_coords)
        if self.path_to_papelera:
            self.path_to_papelera.pop(0)  # Remove the current position

    #def move(self):
    #if self.returning and self.path_to_papelera:
    # new_position = self.path_to_papelera.pop(0)
    #self.model.grid.move_agent(self, new_position)
    #if np.all(new_position == self.model.papelera_coords):
    # self.empty()
    #else:
    # options=self.model.grid.get_neighborhood(self.pos,moore = True, include_center=False)
    #valid_moves = []
    #for pos in options:
    # cell_contents = self.model.grid.get_cell_list_contents(pos)
    # if not any(isinstance(obj, (Obstaculo, AgenteRobot)) for obj in cell_contents):
    #  valid_moves.append(pos)

    #if valid_moves:
    # new_position = random.choice(valid_moves)
    #self.model.grid.move_agent(self, new_position)

    def move(self):
        if self.returning:
            print(f"Robot {self.unique_id} retoma su camino hacia la papelera.")
            if not self.path_to_papelera or self.steps_since_last_path_update >= 4:
                self.find_path_to_papelera()
                self.steps_since_last_path_update = 0
            if self.path_to_papelera:
                new_position = self.path_to_papelera.pop(0)
                self.model.grid.move_agent(self, new_position)
                self.steps_since_last_path_update += 1
                if np.all(new_position == self.model.papelera_coords):
                    self.empty()
        else:
            print(f"Robot {self.unique_id} Moviendose al azar")
            options = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            valid_moves = []
            for pos in options:
                cell_contents = self.model.grid.get_cell_list_contents(pos)
                if not any(isinstance(obj, (Obstaculo, AgenteRobot)) for obj in cell_contents):
                    valid_moves.append(pos)
                if valid_moves:
                    new_position = self.random.choice(valid_moves)
                    self.model.grid.move_agent(self, new_position)

    def step(self):
        self.almacenamiento()
        if self.carrying > 0:
            if not self.returning:
                self.returning = True
                self.find_path_to_papelera()
        if not self.returning:
            self.clean()  # Collect trash in the current cell
        self.move()  # Move to a new cell or towards the papelera
