import utils
import location_randomizer
import math


class ElevatorGame:
    def __init__(self, grid_size, init_passengers_num, max_passengers, new_passenger_p,
                 passenger_priority_value_weights):
        self.turn_n = 1
        self.elevator = Elevator((grid_size // 2, grid_size // 2),
                                 [[], 0])  # init elevator to the middle coordinate of the grid
        self.passengers = dict()  # dict with passenger location (x,y) as keys and Passenger instance as value
        self.grid_size = grid_size  # the size of the grid along the horizontal and vertical axes
        self.max_passengers = max_passengers
        self.new_passenger_p = new_passenger_p  # probability of adding a passenger each turn
        self.passenger_image_indices = {i for i in range(50)}  # available passenger image indices to choose from
        self.p_grid = location_randomizer.create_2d_p_grid(grid_size, grid_size, utils.random_seed(), scale=0.135,
                                                           threshold=0.7)

        # a 3-tuple that used for scaling components in passenger_value func
        self.passenger_priority_value_weights = passenger_priority_value_weights
        # the wait units are calculated based on the number of turns passengers waited each turn
        # total_wait_units is the sum of the wait units of all turns.
        self.total_wait_units = 0

        #  add init_passengers_num passengers to the grid
        while len(self.passengers) < init_passengers_num:
            while True:
                passenger_loc = location_randomizer.choose_point(self.p_grid)
                if self.is_empty_loc(passenger_loc[0], passenger_loc[1]):
                    self.add_passenger(passenger_loc, location_randomizer.choose_point(self.p_grid))
                break

        #  find the most highly valuated passenger and create the elevator path to that passenger
        #  & set the elevator path the elevator's destination_passenger
        self.elevator.path = self.find_best_elevator_path()

    ################# passenger related functions ##################
    def pick_passenger_color(self):
        if len(self.passenger_image_indices) > 0:
            color_i = self.passenger_image_indices.pop()
            return color_i
        else:
            return 0

    def add_passenger(self, location_cords, destination_cords):
        new_passenger = Passenger(location_cords, destination_cords, self.pick_passenger_color(), self.turn_n)
        self.passengers[new_passenger.location] = new_passenger

    def remove_passenger(self, loc):
        self.passenger_image_indices.add(self.passengers[loc].color_i)
        self.passengers.pop(loc)

    ################ passenger evaluation and path finding functions ###############################
    def update_passenger_urgency(self, passenger):
        """
        Used for calculation of passenger value (passengers with higher urgency will be prioritized).
        """
        cur_turn = self.turn_n
        wait_time = cur_turn - passenger.turn_at_creation  # the number of turns the passenger is on the board
        passenger.urgency = math.log10((wait_time / math.sqrt(self.grid_size)) + 10)

    def passenger_priority_value(self, passenger, elevator_cord, center_point):
        urgency = passenger.urgency
        a, b, c = self.passenger_priority_value_weights
        d1 = utils.taxicab_distance(elevator_cord, passenger.location)
        d2 = utils.taxicab_distance(center_point, passenger.destination)
        d3 = utils.taxicab_distance(passenger.destination, passenger.location)

        return (a * d1 + b * d2 + c * d3) / urgency

    def calc_top_priority_passenger(self):
        """
        calculate the priority of each passenger and then find the top priority passenger
        (The passenger with the lowest priority values)
        return: the value of the lowest priority passenger and the corresponding Passenger instance
        """
        center_point = utils.center_of_mass(self.passengers.keys())
        highest_passenger_tuple = min(
            [
                (passenger, self.passenger_priority_value(passenger, self.elevator.get_c_cord(), center_point))
                for passenger in self.passengers.values()
            ],
            key=lambda x: x[1]
        )
        highest_value = highest_passenger_tuple[1]
        highest_passenger = highest_passenger_tuple[0]
        return highest_value, highest_passenger

    def find_best_elevator_path(self):
        """
        return: path to the top priority passenger
        """
        value, passenger = self.calc_top_priority_passenger()
        return utils.taxicab_grid_path_maker(self.elevator.location,
                                             passenger.location)  # return new path

    ######################################## turn update functions #######################################
    def bernoulli_add_passenger(self, p):
        """
        In (p*100)% chance add a passenger to the grid.
        """
        if utils.bernoulli_roll(p):
            while True:
                passenger_loc = location_randomizer.choose_point(self.p_grid)
                if self.is_empty_loc(passenger_loc[0], passenger_loc[1]):
                    self.add_passenger(passenger_loc, location_randomizer.choose_point(self.p_grid))
                    return True
        return False

    def attempt_add_passenger(self):
        """
        Used for adding new passengers to the grid every turn,
        as long as the total number of passenger is less than the maximum allowed passengers
        and a successful Bernoulli experiment with p=new_passenger_p has occurred.
        """
        if len(self.passengers) < self.max_passengers:
            if self.bernoulli_add_passenger(self.new_passenger_p):
                # if a new passenger was added to the grid and the elevator is on "picking mode",
                # the best elevator path is calculated again
                if self.elevator.status == "p":
                    best_path = self.find_best_elevator_path()
                    if best_path[-1] != self.elevator.path[-1]:
                        self.elevator.path = best_path
                        self.elevator.path_index = 0

    def elevator_action(self):
        """
        move elevator if it's not at destination
        """
        destination_loc = self.elevator.path[-1]  # the element at the last index of the path list is the destination
        if self.elevator.location != destination_loc:
            self.elevator.path_index += 1
            self.elevator.location = self.elevator.path[self.elevator.path_index]

        else:
            # check if the elevator is dropping a passenger
            # if so, remove the passenger from cargo and set a new elevator path

            if self.elevator.status == "d":
                # if there are no waiting passengers after getting to the passenger's destination,
                # the elevator status will not change i.e. be "d"
                # but the cargo will be empty.
                if len(self.elevator.cargo) != 0:
                    self.elevator.cargo.pop()
                if len(self.passengers) != 0:
                    self.elevator.path = self.find_best_elevator_path()
                    self.elevator.status = "p"
                else:
                    self.elevator.path = [self.elevator.location]
                    self.elevator.idle_time += 1  # the elevator is staying in place, thus wait time increases by 1.

            # check if the elevator is picking a passenger
            # if so, remove the passenger from passengers list
            elif self.elevator.status == "p":
                self.elevator.add_to_cargo(self.passengers[self.elevator.location])
                new_destination_loc = self.passengers[self.elevator.location].destination
                self.elevator.path = utils.taxicab_grid_path_maker(self.elevator.location, new_destination_loc)
                self.remove_passenger(self.elevator.location)
                self.elevator.status = "d"

            self.elevator.path_index = 0

    def turn_update(self):
        """
        Move the elevator and attempt adding a new passenger.
        Update total turns number, and total wait units.
        """
        self.elevator_action()
        self.attempt_add_passenger()
        self.turn_n += 1

        # calculate the sum of wait units of the current turn and add this sum to the total of all turns.
        sum_wait_units = 0
        for passenger in list(self.passengers.values()):
            self.update_passenger_urgency(passenger)
            sum_wait_units += passenger.urgency
        self.total_wait_units += sum_wait_units

    def board_status(self):
        """
        Used for reporting the board status to the grahpics interface.
        """
        elevator_path = self.elevator.path
        passengers_locs = self.passengers.keys()
        elevator_loc = self.elevator.location
        elevator_cargo = self.elevator.cargo
        return elevator_path, passengers_locs, elevator_loc, elevator_cargo

    ######################################## utils function #######################################
    def is_empty_loc(self, x_cord, y_cord):
        if (x_cord, y_cord) in self.passengers:
            return False
        return True


class Elevator:
    def __init__(self, location, destination_path):
        self.location = location
        self.path = destination_path  # lists of tuples representing cords on the grid
        self.cargo = []  # list of passengers picked by the elevator. The last passenger is first to be dropped.
        self.path_index = 0  # the current index of the path the elevator is moving along
        self.status = "p"  # the elevator can be in two modes: "p" for picking / "d" for dropping a passenger
        self.idle_time = 0  # the total elevator idle time

    def get_c_cord(self):
        return self.location

    def add_to_cargo(self, passenger):  ## add a passenger to cargo
        self.cargo.append(passenger)

    def elevator_destination(self):
        return self.cargo[0].destination

    def elevator_next_move(self):
        """
        :return: tuple representing the next loc the elevator move to, based on the current elevators' path.
        if path is empty, return the current elevator loc.
        """
        if len(self.path) == 0:
            return self.location
        next_loc = self.path[self.path_index]  # the next loc to move to
        self.path_index += 1
        return next_loc


class Passenger:
    def __init__(self, location_cords, destination_cords, color_i, turn_at_creation):
        self.location = location_cords  ## initiate passenger spawning location
        self.destination = destination_cords  ## initiate passenger destination location
        self.target_distance = utils.taxicab_distance(location_cords, destination_cords)
        self.color_i = color_i
        self.passenger_image_path = f"graphics/passenger_{self.color_i}.png"
        self.target_path = f"graphics/passenger_target_{self.color_i}.png"
        self.turn_at_creation = turn_at_creation  # the game turn number at the time of passenger creation
        self.urgency = 1  # updates in relation to the total turn the passenger has waited
        # (see update_passenger_urgency ElevatorGame func)
