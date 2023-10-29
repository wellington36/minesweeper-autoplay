import pygame
import numpy as np

MINES = 80
GRID_SIZE = 20

SCREEN_SIZE = 480
TILE_SIZE = SCREEN_SIZE//GRID_SIZE

#Mine sweeper game
class Game:
    def __init__(self, graphics=True):
        self.checked = []
        self.explosion = False
        self.graphics = graphics
        self.mines = self.set_mines()

        # Maybe we want to run the game without graphics
        pygame.init()
        if graphics == True:
            self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
            self.define_number_images()

    def define_number_images(self):
        number_font = pygame.font.SysFont(None, TILE_SIZE)
        self.number_images = []
        for i in range(9):
            number_text = str(i)
            number_image = number_font.render(number_text, True, "black", None)
            self.number_images.append(number_image)

    def draw(self):
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE):
                if self.explosion == True and self.mines[i,j] == 1:
                    self.draw_tiles((i,j), "black")
                else:
                    self.draw_tiles((i,j), "gray")

        for tile in self.checked:
            num_mines_around = self.check_mines(tile)
            if num_mines_around != 0:
                self.draw_tiles(tile, "white")
                self.draw_number(tile, num_mines_around)
            else:
                self.draw_tiles(tile, "white")
        pygame.display.flip()    

    def draw_tiles(self, tile, color):
        rect = pygame.Rect(tile[0]*TILE_SIZE, tile[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        start_pos_x = (0, tile[1]*TILE_SIZE)
        start_pos_y = (tile[0]*TILE_SIZE,0)
        end_pos_x = (SCREEN_SIZE, tile[1]*TILE_SIZE)
        end_pos_y = (tile[0]*TILE_SIZE,SCREEN_SIZE)
        
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.line(self.screen, "black", start_pos_x, end_pos_x)
        pygame.draw.line(self.screen, "black", start_pos_y, end_pos_y)

    def draw_number(self, pos, number):
        number_image = self.number_images[number]
        num_img_width = number_image.get_width()
        num_img_height = number_image.get_height()

        num_img_x = 1+pos[0]*TILE_SIZE + (TILE_SIZE - num_img_width)//2
        num_img_y = 1+pos[1]*TILE_SIZE + (TILE_SIZE - num_img_height)//2
        self.screen.blit(number_image, (num_img_x, num_img_y))

    def on_click(self, pos):
        if pos in self.checked:
            return

        if self.mines[pos] == 1:
            self.explosion = True
            return
        
        self.checked.append(pos)
        mines = self.check_mines(pos)
        if mines != 0:
            return
        
        neighbours = self.get_neighbours(pos)
        for elem in neighbours:
            if self.mines[elem] == 0:
                self.on_click(elem)
        

    def set_mines(self):
        return np.random.binomial(1, MINES/(GRID_SIZE*GRID_SIZE), (GRID_SIZE,GRID_SIZE))
    
    def get_neighbours(self, pos):
        neighbours = []
        for i in range(-1,2):
            for j in range(-1,2):
                if pos[0]+i >= 0 and pos[0]+i < GRID_SIZE:
                    if pos[1]+j >= 0 and pos[1]+j < GRID_SIZE:
                        if (i,j) != (0,0):
                            neighbours.append((pos[0]+i, pos[1]+j))
        return neighbours
    
    def check_mines(self, pos):
        neighbours = self.get_neighbours(pos)
        count = 0
        for elem in neighbours:
            if self.mines[elem] == 1:
                count += 1
        return count
    
    def run(self):
        pygame.event.clear()

        if self.graphics == True:
            self.draw()
        
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.click = self.on_click((pos[0]//TILE_SIZE, pos[1]//TILE_SIZE))

                if self.graphics == True:
                    self.draw()
                if self.explosion == True:
                    if self.graphics == True:
                        pygame.time.wait(1000)
                    pygame.quit()
                    return

# Minesweeper = Game()
# Minesweeper.run()
