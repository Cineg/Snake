import pygame
import math
import random

class Board:
    def __init__(self, side_size_px: int = 20) -> None:
        self.window: pygame.surface.Surface = pygame.display.get_surface()
        self.side_size: int = side_size_px
        self.rows: int 
        self.columns: int
        self.cells: list[list[Cell]]

        self.snake_head_pos: tuple[int, int]
        self.snake: list[tuple[int, int]] = []

        self.snake_food_pos: tuple[int, int]

        self._get_board_size()
        self._seed_cells()
        
        self.direction: tuple[int, int]  = (0,0)
        self.game_over: bool = False
    
    def draw(self) -> None:
        self._update_board()

        for _ in self.cells:
            for cell in _:
                cell_pos: tuple[int, int] = cell.get_position
                if cell_pos == self.snake_food_pos:
                    cell.draw(True, False, False)

                elif cell_pos in self.snake:
                    if cell_pos == self.snake_head_pos:
                        cell.draw(False, False, True)
                    else:
                        cell.draw(False, True, False)
                
                else:
                    cell.draw(False, False, False)
    

    def _update_board(self) -> None:
        ate_food: bool = False
        if self.snake_head_pos == self.snake_food_pos:
            ate_food = True
            self._repositon_food()
        
        self._update_snake(ate_food)

        if self.snake_head_pos in self.snake[1:]:
            self.game_over = True
        
        if self.snake_head_pos[0] > self.columns or self.snake_head_pos[1] > self.rows:
            self.game_over = True
        
        if self.snake_head_pos[0] < 0 or self.snake_head_pos[1] < 0:
            self.game_over = True
            


    def _get_board_size(self) -> None:
        self.rows = math.floor(self.window.get_height() / self.side_size)
        self.columns = math.floor(self.window.get_width() / self.side_size)

    def _seed_cells(self) -> None:
        self.snake_head_pos: tuple[int, int] = random.randint(0, self.columns), random.randint(0, self.rows)
        self.snake.append(self.snake_head_pos)

        self.snake_food_pos: tuple[int, int] = random.randint(0, self.columns), random.randint(0, self.rows)

        cells_board: list[list[Cell]] = []
        for row in range(self.rows):
            row_list: list[Cell] = []
            for column in range(self.columns):
                cell: Cell = Cell((column, row), self.side_size)
                row_list.append(cell)

            cells_board.append(row_list)

        self.cells = cells_board

    def _update_snake(self, got_food: bool = False) -> None:
        self.snake_head_pos = self.snake_head_pos[0] + self.direction[0], self.snake_head_pos[1] + self.direction[1]

        temp_list: list[tuple[int, int]] = []
        temp_list.append(self.snake_head_pos)
        self.snake = temp_list + self.snake
        if not got_food:
            self.snake.pop()

    def _repositon_food(self) -> None:
        random_pos: tuple[int, int] = random.randint(0, self.columns - 1), random.randint(0, self.rows - 1)

        while random_pos in self.snake:
            random_pos = random.randint(0, self.columns - 1), random.randint(0, self.rows - 1)
        
        self.snake_food_pos = random_pos

class Cell:
    def __init__(self, coordinates: tuple[int, int], side_px_length: int) -> None:
        self.window: pygame.surface.Surface = pygame.display.get_surface()
        self.row: int = coordinates[1]
        self.column: int = coordinates[0]

        self.side_size: int = side_px_length
        self.x_position: int 
        self.y_position: int

        self._calculate_position()
    
    @property
    def get_position(self) -> tuple[int, int]:
        return (self.column, self.row)

    def draw(self, is_food: bool = False, is_snake: bool = False, is_snake_head: bool = False) -> None:
        color: tuple[int, int, int] = self._get_color(is_snake_head, is_snake, is_food)
        pygame.draw.rect(
            surface=self.window,
            color=color,
            rect=(self.y_position, self.x_position, self.side_size, self.side_size),
        )

    def _get_color(self, is_snake_head: bool, is_snake: bool, is_food: bool) -> tuple[int, int, int]:
        if is_snake_head:
            return (255, 0, 0)
        if is_snake:
            return (150, 0, 0)
        if is_food:
            return (0, 255, 0)
        
        return 10, 0, 10
    
    def _calculate_position(self) -> None:
        self.x_position = self.row * self.side_size
        self.y_position = self.column * self.side_size

def main() -> None:
    pygame.init()
    pygame.surface.Surface = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Snek")
    clock = pygame.time.Clock()

    board: Board = Board()

    while board.game_over == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.direction = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    board.direction = (1, 0)
                if event.key == pygame.K_DOWN:
                    board.direction = (0, 1)
                if event.key == pygame.K_UP:
                    board.direction = (0, -1)
                
        clock.tick(15)
        board.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()