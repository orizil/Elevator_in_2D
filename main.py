import Elevator_Game
import Game_Graphics

# constants
GRID_SIZE = 20  # the size of the grid along the horizontal and vertical axes
SCREEN_SIZE = (600, 600)  # size in pixels
TURNS = 1000
INIT_PASSENGER_NUM = 5
MAX_PASSENGERS = 10
NEW_PASSENGER_P = 0.05 # probability of adding a new passenger each game turn


def main():
    game = Elevator_Game.ElevatorGame(GRID_SIZE, INIT_PASSENGER_NUM, MAX_PASSENGERS, NEW_PASSENGER_P, (1, 1, 1))
    board_graphics = Game_Graphics.BoardGraphics(game, SCREEN_SIZE)  # init board graphic interface
    board_graphics.draw_board(game.board_status())
    board_graphics.latency(80)

    ## turns loop
    while game.turn_n < TURNS:
        game.turn_update()
        board_graphics.draw_board(game.board_status())
        board_graphics.latency(80)


if __name__ == '__main__':
    main()
