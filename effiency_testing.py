import numpy as np
import matplotlib.pyplot as plt
import Elevator_Game
from skopt import gp_minimize
from skopt.space import Real

# Constants
GRID_SIZE = 20
TURNS = 500
INIT_PASSENGER_NUM = 5
MAX_PASSENGERS = 10
NEW_PASSENGER_P = 0.065
N_GAMES = 10000

def run_game(turns, scale):
    switch_turns = []
    game = Elevator_Game.ElevatorGame(GRID_SIZE, INIT_PASSENGER_NUM, MAX_PASSENGERS, NEW_PASSENGER_P, scale)
    last_status = "p"
    while game.turn_n < turns:
        cur_status = game.elevator.status
        if last_status != cur_status:
            switch_turns.append(game.turn_n)
        last_status = cur_status
        game.turn_update()
    return game.total_wait_units, np.average(np.diff(switch_turns)), game.elevator.wait_time / game.turn_n


def stats(scale):
    results = np.array([run_game(TURNS, scale) for _ in range(N_GAMES)])
    r1, r2, r3 = results[:, 0], results[:, 1], results[:, 2]
    return np.average(r1),np.average(r2), np.average(r3)


r1, r2, r3 = stats((1,0,0))
print("(1,0,0)")
print("total_wait_units", np.average(r1), "avg time to reach dest", np.average(r2), "avg elevator idle time",
      np.average(r3))


# r1,r2,r3 = stats(5000)
# np.save("results/passengers_total_wait_units", r1)
# np.save("results/avg_switch_time", r2)
# np.save("results/avg_elevator_total_wait_time", r3)
#
# r1u=np.load("results/passengers_total_wait_units.npy")
# r2u=np.load("results/avg_switch_time.npy")
# r3u=np.load("results/avg_elevator_total_wait_time.npy")
# r1nou=np.load("results/passengers_total_wait_units_no_central.npy")
# r2nou=np.load("results/avg_switch_time_no_central.npy")
# r3nou=np.load("results/avg_elevator_total_wait_time_no_central.npy")
#
# # Perform t-tests
# t_statistic1, p_value1 = ttest_ind(r1u, r1nou)
# t_statistic2, p_value2 = ttest_ind(r2u, r2nou)
# t_statistic3, p_value3 = ttest_ind(r3u, r3nou)
#
# # Print results
# print("Results for r1u and r1nou:")
# print("T-Statistic:", t_statistic1)
# print("P-Value:", p_value1)
# print("")
#
# print("Results for r2u and r2nou:")
# print("T-Statistic:", t_statistic2)
# print("P-Value:", p_value2)
# print("")
#
# print("Results for r3u and r3nou:")
# print("T-Statistic:", t_statistic3)
# print("P-Value:", p_value3)
#
#


# avg_wait_units_list = [avg_wait_units(n_games) for n_games in range(1, 100)]
#
# # Create the graph using matplotlib
# plt.figure(figsize=(10, 6))
#
# # Plot the data
# plt.plot(range(1, 100), avg_wait_units_list, marker='o', linestyle='-', color='b')
#
# # Add labels and title
# plt.xlabel('Number of Games')
# plt.ylabel('Average Total Wait Units')
# plt.title('Average Total Wait Units vs Number of Games')
#
# # # Show the plot
# # plt.grid(True)
# # plt.show()
#
# param_space = [Real(0.0, 1.0, name='param1'),
#                Real(0.0, 1.0, name='param2'),
#                Real(0.0, 1.0, name='param3')]
# result = gp_minimize(stats,                  # Function to minimize
#                      dimensions=param_space,         # Parameter space
#                      n_calls= 50,         # Number of iterations
#                      n_random_starts=10,  # Number of random starts
#                      random_state=1)             # Random seed for reproducibility
# print(result.x, result.fun)
#
# # [0.5366192531498377, 0.0, 0.26511386486482486] 4991.32334553039
# #