# Important imports
import numpy as np

# Game
import game

# Our solvers
import solvers as solver

# Drawing
import glob
import matplotlib.pyplot as plt
from PIL import Image


def draw_brute_solve(new_map, owned):
    # print(new_map)
    ideal_sol = solver.yield_brute_force_given_state(0, [], new_map.copy(), owned.copy())
    # print(ideal_sol)
    for i, move in enumerate(ideal_sol):
        # Try colour
        # ## Best guess for colour
        guess_colour = move
        # print(new_map, guess_colour)

        # Fill colour of owned cells
        new_map[owned] = guess_colour

        # Gather ownership of other cells
        owned = game.flood(new_map, owned, move)

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
    new_map = np.random.randint(game.COLOURS, size=(game.WIDTH, game.HEIGHT))
    owned = np.zeros((game.WIDTH, game.HEIGHT), dtype=np.bool)
    owned[game.START] = True
    draw_brute_solve(new_map, owned)
