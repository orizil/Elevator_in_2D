"""

Contains functions for choosing random cells on the grid. Used for controlling where passengers can spawn.

"""

import opensimplex
import numpy as np


def create_2d_p_grid(width, height,seed, scale=0.5, threshold=0.6):
    """
    :param scale: controls the frequency of the noise
    :param threshold: controls the amount of projected-to-zero points on the grid
    :return: probability grid with even probabilities (uniform)
    """

    # Create an OpenSimplex noise object with a random seed
    noise_obj = opensimplex.OpenSimplex(seed=seed)

    # Generate the noise values for each point in the heatmap
    heatmap = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            noise_value = (noise_obj.noise2(x * scale, y * scale) + 1) / 2
            if noise_value >= threshold:
                heatmap[y][x] = 1
            else:
                heatmap[y][x] = 0

    # Normalize the heatmap and return the grid
    return heatmap / np.sum(heatmap)

def choose_point(p_grid):
    """
    :param p_grid: a probability grid
    :return: cell indices (x,y) of the grid
    """
    # Flatten the heatmap and choose a random index
    p_grid=np.transpose(p_grid)
    flattened_probs = p_grid.flatten()
    random_index = np.random.choice(len(flattened_probs), p=flattened_probs)
    unravel_indices = np.unravel_index(random_index, p_grid.shape)

    return unravel_indices