"""

Contains utility functions used by the game logic.

"""

import random
import numpy as np



def random_seed():
    rand_seed = random.randint(0, 2 ** 32 - 1)  # simplex noise seed
    return rand_seed


def bernoulli_roll(p):
    return np.random.binomial(n=1, p=p)


def taxicab_distance(cord1, cord2):  ## calculate the taxicab distance between the two cords.
    x1, y1 = cord1
    x2, y2 = cord2
    return abs(x1 - x2) + abs(y1 - y2)


def geomtric_median(all_points):
    pass


def weighted_center_of_mass(all_points, weights):  # calculate the center of mass of points on a 2D plane.
    """
    :param all_points: list of points coordinates
    :return: the center of mass of points on a 2D plane with all weights equal to 1.
    """
    mass = sum(weights)
    x_sum, y_sum = 0, 0
    for i in range(all_points):
        x_sum += all_points[i][0] * weights[i]
        y_sum += all_points[i][1] * weights[i]
    return (round(x_sum / mass), round(y_sum / mass))


def center_of_mass(all_points):
    """
    :param all_points: list of points coordinates
    :return: the center of mass of points on a 2D plane with all weights equal to 1.
    """
    mass = len(all_points)
    x_sum, y_sum = 0, 0
    for point in all_points:
        x_sum += point[0]
        y_sum += point[1]
    return (round(x_sum / mass), round(y_sum / mass))


def taxicab_grid_path_maker(cur_loc, target_loc):
    path = [cur_loc]
    x1, y1 = cur_loc
    x2, y2 = target_loc

    direction = (np.sign(x2 - x1), np.sign(y2 - y1))

    while x1 != x2 or y1 != y2:
        if x1 != x2:
            x1 += direction[0]
            path.append((x1, y1))
        if y1 != y2:
            y1 += direction[1]
            path.append((x1, y1))

    return path
