import pygame
import sys
from random import choice

CELL_SIZE = 10
SCREEN = WIDTH, HEIGHT = 100, 70
DEAD_COLOR = 30, 30, 30
ALIVE_COLOR = 100, 200, 100


class TheGameOfLife:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH*CELL_SIZE, HEIGHT*CELL_SIZE))

    def draw_circle(self, x, y, r):
        pygame.draw.circle(self.window, ALIVE_COLOR, (x,y), r)

    class Field(object):
        def __init__(self, w, h, surface):
            self.__w = w
            self.__h = h
            self.__field = [[choice((1, 0)) for x in range(self.__w)] for y in range(self.__h)]
            self.__surface = surface

        def generate_field(self, val: int = None) -> None:
            if val is None:
                self.__field = [[choice((1, 0)) for x in range(self.__w)] for y in range(self.__h)]
            else:
                self.__field = [[val for x in range(self.__w)] for y in range(self.__h)]

        def get_field(self):
            return self.__field

        def draw_field(self):
            for i, row in enumerate(self.get_field()):
                for j, el in enumerate(row):
                    if el:
                        pygame.draw.rect(self.__surface, ALIVE_COLOR, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        def set_field(self, new_field: list):
            self.__field = new_field

    def next_generation_calculation(self, current_field: Field, future_field: Field) -> None:
        """
        for alive cell
        0/1 neighbours  - die
        2/3             - stay
        4+              - die

        for dead cell:
        == 3 neighbours - become alive
        != 3 neighbours - stay alive:
         """
        current_list = current_field.get_field()
        future_field.generate_field(val=0)
        future_list = future_field.get_field()

        SURROUNDING_CELLS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        def _get_surrounding_alive_cells(x: int, y: int) -> int:
            """ x, y - indexes in field """
            s = 0
            for cell in SURROUNDING_CELLS:
                try:
                    try_cell = list(map(sum, list(zip((x, y), cell))))  # surrounding cell around  cell
                    if -1 in try_cell:
                        raise IndexError
                    if current_list[try_cell[1]][try_cell[0]]:
                        s += 1
                except IndexError:
                    continue
            return s

        for y, row in enumerate(current_list):
            for x, el in enumerate(row):
                neighbours = _get_surrounding_alive_cells(x, y)
                if el == 0:
                    if neighbours == 3:
                        future_list[y][x] = 1
                    else:
                        future_list[y][x] = 0
                elif el == 1:
                    if neighbours < 2:
                        future_list[y][x] = 0
                    elif 2 <= neighbours <= 3:
                        future_list[y][x] = 1
                    elif neighbours > 3:
                        future_list[y][x] = 0

        current_field.set_field(future_list)

    def update_screen(self):
        self.window.fill(DEAD_COLOR)

    def events_check(self, field: Field):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    field.generate_field()

    def run(self):
        current_field = self.Field(WIDTH, HEIGHT, self.window)
        future_field = self.Field(WIDTH, HEIGHT, self.window)
        # print(a)
        while True:
            self.update_screen()
            self.events_check(current_field)
            current_field.draw_field()
            self.next_generation_calculation(current_field, future_field)

            # self.draw_circle(50, 100, 2)
            pygame.display.update()
