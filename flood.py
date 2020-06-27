# Important imports
import numpy as np

# Drawing
import glob
import matplotlib.pyplot as plt
from PIL import Image

# CONSTANTS
COLOURS = 4
WIDTH = 64
HEIGHT = 64
START = (0, 0)


# Get the area of the map that is owned
def area(owned_state: np.array) -> int:
    return np.sum(owned_state)

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


# Solve via brute force by checking all possible paths.
def yield_brute_force_given_state(num_guesses: int, prev_guesses: list, field_state: np.array, owned: np.array) -> list:
    if not_filled(owned):
        num_guesses += 1
        costs = []
        best_branches = []
        for guess in range(COLOURS):
            # if the guess is the same as what we have
            if guess == field_state[START]:
                continue

            new_field = field_state.copy()
            new_field[owned] = guess
            # if guess does not get any more tiles
            if area(owned) == area(flood(new_field, owned, guess)):
                continue
            # print("Area Owned: {}" .format(area(owned)))
            # print("Area Flood: {}".format(area(flood(new_field, owned, guess))))
            new_owned = flood(new_field, owned, guess)
            prev_guesses.append(guess)
            best_branch = yield_brute_force_given_state(num_guesses+1,
                                                        prev_guesses.copy(),
                                                        new_field,
                                                        new_owned)
            prev_guesses.pop()
            cost = len(best_branch)
            best_branches.append(best_branch)
            costs.append(cost)
        # Get the first branch that was the shortest
        min_cost, branch = min(zip(costs, best_branches))
        return branch
    else:
        return prev_guesses


def draw_brute_solve(new_map, owned):
    print(new_map)
    ideal_sol = yield_brute_force_given_state(0, [], new_map.copy(), owned.copy())
    print(ideal_sol)
    for i, move in enumerate(ideal_sol):
        # Try colour
        # ## Best guess for colour
        guess_colour = move
        # print(new_map, guess_colour)

        # Fill colour of owned cells
        new_map[owned] = guess_colour

        # Gather ownership of other cells
        owned = flood(new_map, owned, move)

        plt.imshow(new_map, cmap='Paired', interpolation='nearest')
        plt.savefig('./solve/{}.png'.format(str(i).zfill(3)))
        # plt.show()
    

    plt.imshow(new_map, cmap='Paired', interpolation='nearest')
    plt.savefig('./solve/{}.png'.format(str(i+1).zfill(3)))
    # plt.show()


# Animate the solution in the solve folder into a gif
def animate_solve():
    fp_in = "./solve/*.png"
    fp_out = "./solve/solve.gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=200, loop=0)


if __name__ == '__main__':
    new_map = np.random.randint(COLOURS, size=(WIDTH, HEIGHT))
    owned = np.zeros((WIDTH, HEIGHT), dtype=np.bool)
    owned[START] = True
    draw_brute_solve(new_map, owned)
