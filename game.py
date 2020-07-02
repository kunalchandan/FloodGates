import numpy as np

# CONSTANTS
COLOURS = 4
WIDTH = 3
HEIGHT = 3
START = (0, 0)


# Get the area of the map that is owned
def area(owned_state: np.array) -> int:
    return np.sum(owned_state)


# Get Perimeter of owned map
def perimeter(owned_state: np.array) -> int:
    # for pad in np.reshape(np.eye(4), (4, 2, 2)):
    perim = 0
    perim += area(owned_state & (owned_state ^ np.pad(owned_state, ((1, 0), (0, 0)), mode='constant')[:-1, :]))
    perim += area(owned_state & (owned_state ^ np.pad(owned_state, ((0, 1), (0, 0)), mode='constant')[1:, :]))
    perim += area(owned_state & (owned_state ^ np.pad(owned_state, ((0, 0), (1, 0)), mode='constant')[:, :-1]))
    perim += area(owned_state & (owned_state ^ np.pad(owned_state, ((0, 0), (0, 1)), mode='constant')[:, 1:]))
    return perim


# Check if all filled
def not_filled(own: np.array):
    return not np.all(own)


# Get ownership of all other cells adjacent (in up down left right) with the same colour
def flood(field: np.array, own: np.array, guess_colour: int) -> np.array:
    cur_area = area(own)
    for i in range(max(WIDTH, HEIGHT)):
        # Checks each direction by padding and checking colour with ownership in each direction
        own[np.pad(own &
                     np.pad(field == guess_colour,
                            ((0, 1), (0, 0)),
                            mode='constant')[1:, :],
                   ((1, 0), (0, 0)), mode='constant')[:-1, :]] = True
        own[np.pad(own &
                     np.pad(field == guess_colour,
                            ((0, 0), (0, 1)),
                            mode='constant')[:, 1:],
                   ((0, 0), (1, 0)), mode='constant')[:, :-1]] = True
        own[np.pad(own &
                     np.pad(field == guess_colour,
                            ((1, 0), (0, 0)),
                            mode='constant')[:-1, :],
                   ((0, 1), (0, 0)), mode='constant')[1:, :]] = True
        own[np.pad(own &
                     np.pad(field == guess_colour,
                            ((0, 0), (1, 0)),
                            mode='constant')[:, :-1],
                   ((0, 0), (0, 1)), mode='constant')[:, 1:]] = True
        # Prevent excess checking
        if area(own) == cur_area:
            break
        else:
            cur_area = area(own)
    return own

