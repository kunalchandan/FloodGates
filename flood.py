# Important imports
import numpy as np

# Game
import game

# Our solvers
import solvers

# Drawing
import os
import shutil
import glob
import matplotlib.pyplot as plt
from PIL import Image

MAP_COLOUR = 'viridis'
ZFILL = 3


def draw_solve(new_map: np.array, owned: np.array, solver, folder):
    ideal_sol = solver(0, [], new_map.copy(), owned.copy())
    print(f"Solution by {folder} solver")
    print(ideal_sol)
    plt.imshow(new_map, cmap=MAP_COLOUR, interpolation='nearest')
    plt.savefig('./solve/{}/{}.png'.format(folder, str(0).zfill(ZFILL)))
    for i, move in enumerate(ideal_sol):
        # Try colour
        # ## Best guess for colour
        guess_colour = move
        # Fill colour of owned cells
        new_map[owned] = guess_colour
        # Gather ownership of other cells
        owned = game.flood(new_map, owned, move)
        plt.imshow(new_map, cmap=MAP_COLOUR, interpolation='nearest')
        plt.savefig('./solve/{}/{}.png'.format(folder,str(i+1).zfill(ZFILL)))


# Animate the solution in the solve folder into a gif
def animate_solve():
    fp_in = "./solve/*.png"
    fp_out = "./solve/solve.gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=200, loop=0)


if __name__ == '__main__':
    new_map = np.random.randint(game.COLOURS, size=(game.WIDTH, game.HEIGHT))
    print("New Map")
    print(new_map)
    owned = np.zeros((game.WIDTH, game.HEIGHT), dtype=np.bool)
    # Start and flood to the surrounding neighbours with the same colour
    owned[game.START] = True
    owned = game.flood(new_map, owned, new_map[game.START])
    [[os.remove(f'./solve/{a}/{b}') for b in os.listdir(f'./solve/{a}/')] for a in ['greedy', 'brute'] if os.path.exists(f'./solve/{a}/')]
    [os.makedirs(f'./solve/{a}/') for a in ['greedy', 'brute'] if not os.path.exists(f'./solve/{a}/')]
    print("Greedy Solve")
    draw_solve(new_map.copy(), owned.copy(), solvers.greedy_perimeter_solve, 'greedy')
    print("Brute Solve")
    draw_solve(new_map.copy(), owned.copy(), solvers.yield_brute_force_given_state, 'brute')
    for i in range(1000):
        
