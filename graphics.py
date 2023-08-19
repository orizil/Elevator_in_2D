"""

Manages the graphical interface for the game, drawing the game board, passengers, and elevator.

"""

import pygame
import main

pygame.init()
screen = pygame.display.set_mode(main.SCREEN_SIZE)
elements_surface = pygame.Surface(main.SCREEN_SIZE)
top_layer_surface = pygame.Surface(main.SCREEN_SIZE, pygame.SRCALPHA)
prob_surface = pygame.Surface(main.SCREEN_SIZE, pygame.SRCALPHA)
prob_surface.set_alpha(30)

class BoardGraphics:
    def __init__(self, game, screen_size):
        self.game = game
        self.passengers = game.passengers  # dict with passenger location (x,y) as keys and Passenger instance as value
        self.passenger_image_indices = {i for i in range(50)}  # available passenger image indices to choose from
        self.grid_size = game.grid_size  # number of cells along an axis
        self.screen_size = screen_size  # tuple representing the screen size
        self.cell_size = self.screen_size[0] // self.grid_size
        self.p_grid = game.p_grid
        self.create_top_layer()  # add the grid lines and cell numbers

    def create_top_layer(self):
        """
        for drawing grid lines and the parts of the board where passengers can show up
        (based on tuple cords it the p_grid)
        """
        for row in range(len(self.p_grid)):
            for col in range(len(self.p_grid[0])):
                if self.p_grid[row][col] > 0:
                    rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(prob_surface, (255, 255, 0), rect)  # 50,50,50

                pygame.draw.line(top_layer_surface, (120, 120, 120), (col * self.cell_size, 0),
                                 (col * self.cell_size, self.screen_size[1]))

            pygame.draw.line(top_layer_surface, (120, 120, 120), (0, row * self.cell_size),
                             (self.screen_size[0], row * self.cell_size))

    def draw_path(self, path):
        """
        draw elevator path
        """
        for cords in path:
            x_cor, y_cor = cords
            rect = pygame.Rect(x_cor * self.cell_size, y_cor * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(elements_surface, (190, 190, 190), rect)

    def draw_passengers(self, passengers_locs):
        for passenger_loc in passengers_locs:
            x_cor, y_cor = passenger_loc
            img_path = self.passengers[passenger_loc].passenger_image_path
            passenger_img = pygame.image.load(img_path).convert_alpha()

            # resize the image to fit the cell size
            passenger_img = pygame.transform.scale(passenger_img, (self.cell_size, self.cell_size))

            passenger_rect = pygame.Rect((x_cor * self.cell_size), (y_cor * self.cell_size), self.cell_size,
                                         self.cell_size)
            elements_surface.blit(passenger_img, passenger_rect)
    def draw_passengers_targets(self, elevator_cargo):
        for passenger in elevator_cargo+list(self.passengers.values()):
            x_cor, y_cor = passenger.destination
            img_path = passenger.target_path
            target_img = pygame.image.load(img_path).convert_alpha()

            # resize the image to fit the cell size
            target_img = pygame.transform.scale(target_img, (self.cell_size, self.cell_size)).convert_alpha()

            target_rect = pygame.Rect((x_cor * self.cell_size), (y_cor * self.cell_size), self.cell_size,
                                         self.cell_size)
            elements_surface.blit(target_img, target_rect)
    def draw_elevator(self, elevator_cords):
        if self.game.elevator.cargo:  # check if cargo is not empty
            color_i = self.game.elevator.cargo[-1].color_i  # get color index of the passenger getting dropped
            img_path = f"graphics/elevator_and_passenger_{color_i}.png"
        else:
            img_path = "graphics/elevator.png"
        x_cor, y_cor = elevator_cords
        elevator_img = pygame.image.load(img_path)

        # Resize the image to fit the cell size
        elevator_img = pygame.transform.scale(elevator_img, (self.cell_size, self.cell_size))

        elevator_rect = pygame.Rect((x_cor * self.cell_size), (y_cor * self.cell_size), self.cell_size, self.cell_size)
        elements_surface.blit(elevator_img, elevator_rect)

    def draw_board(self, elements):
        elements_surface.fill((255, 255, 255))  # Clear the elements from last turn
        path, passengers, elevator, elevator_cargo = elements

        self.draw_path(path)
        self.draw_passengers_targets(elevator_cargo)
        self.draw_passengers(passengers)
        self.draw_elevator(elevator)

        screen.blit(elements_surface, (0, 0))
        screen.blit(top_layer_surface, (0, 0))
        screen.blit(prob_surface, (0, 0))

        pygame.display.flip()

    def latency(self, millisecs):
        # delay each turn.
        pygame.time.delay(millisecs)

