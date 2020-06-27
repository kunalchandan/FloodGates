# Game
import game


# Solve via brute force by checking all possible paths.
def yield_brute_force_given_state(num_guesses: int, prev_guesses: list, field_state: np.array, owned: np.array) -> list:
    if game.not_filled(owned):
        num_guesses += 1
        costs = []
        best_branches = []
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
            costs.append(cost)
        # Get the first branch that was the shortest
        min_cost, branch = min(zip(costs, best_branches))
        return branch
    else:
        return prev_guesses

