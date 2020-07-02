# Important
import numpy as np

# Game
import game


# Greedy perimeter Solve
def greedy_perimeter_solve(num_guesses: int, prev_guesses: list, field_state: np.array, owned: np.array) -> list:
    while game.not_filled(owned):
        num_guesses += 1

        guesses = []
        new_perimeters = []
        for guess in range(game.COLOURS):
            if guess == field_state[game.START]:
                continue

            new_field = field_state.copy()
            new_owned = owned.copy()
            new_field[owned] = guess
            if game.area(owned) == game.area(game.flood(new_field, new_owned, guess)):
                continue

            new_owned = game.flood(new_field, new_owned, guess)
            guesses.append(guess)
            new_perimeters.append(game.perimeter(new_owned))

        max_per, best_guess = max(zip(new_perimeters, guesses))

        field_state[owned] = best_guess
        owned = game.flood(field_state, owned, best_guess)
        prev_guesses.append(best_guess)
        print(num_guesses)

    print(owned)
    return prev_guesses


# Solve via brute force by checking all possible paths.
def yield_brute_force_given_state(num_guesses: int, prev_guesses: list, field_state: np.array, owned: np.array) -> list:
    if game.not_filled(owned):
        num_guesses += 1
        costs = []
        best_branches = []
        action = []
        for guess in range(game.COLOURS):
            # if the guess is the same as what we have
            if guess == field_state[game.START]:
                continue

            new_field = field_state.copy()
            new_field[owned] = guess
            # if guess does not get any more tiles
            if game.area(owned) == game.area(game.flood(new_field, owned, guess)):
                continue
            # print("Area Owned: {}" .format(area(owned)))
            # print("Area Flood: {}".format(area(flood(new_field, owned, guess))))
            new_owned = game.flood(new_field, owned, guess)
            prev_guesses.append(guess)
            best_branch = yield_brute_force_given_state(num_guesses+1,
                                                        prev_guesses.copy(),
                                                        new_field,
                                                        new_owned)
            prev_guesses.pop()
            cost = len(best_branch)
            best_branches.append(best_branch)
            action.append(guess)
            costs.append(cost)
        # Get the first branch that was the shortest
        min_cost, branch, action = min(zip(costs, best_branches, action))
        return branch
    else:
        return prev_guesses

