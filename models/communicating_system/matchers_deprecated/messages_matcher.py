import numpy as np


# Precondicion: len(messages_collection_1) == len(messages_collection_2)
def match_messages(messages_collection_1, messages_collection_2):
    grid = generate_messages_matches_grid(messages_collection_1, messages_collection_2)
    return collect_message_matches_from_grid(
        messages_collection_1,
        messages_collection_2,
        grid
    )


def generate_messages_matches_grid(messages_collection_1, messages_collection_2):
    grid = np.empty((len(messages_collection_1), len(messages_collection_2)), dtype=object)

    for i in range(0, len(messages_collection_1)):
        message_1 = messages_collection_1[i]
        for j in range(0, len(messages_collection_2)):
            message_2 = messages_collection_2[j]
            grid[i][j] = (i, j, valid_messages_match_between(message_1, message_2))

    return grid


def collect_message_matches_from_grid(messages_collection_1, messages_collection_2, grid):
    matches = []

    # esto solo pasa cuando encontro algun match para todos los mensajes (sino la grilla no se reduce)
    if len(grid) == 0:
        matches.append([])

    # Siempre fijo la primer fila y pivoteo sobre la columna.
    # Si no encuentro algun True en la primer fila, entonces no va a haber matching posible,
    # ya que quiere decir que existe una etiqueta en la primer coleccion que no se empareja con ninguna de la segunda
    for j in range(0, len(grid)):
        m1_index, m2_index, is_valid = grid[0][j]
        if is_valid:
            base_match = (messages_collection_1[m1_index], messages_collection_2[m2_index])

            left_sub_grid = grid[1:len(grid), 0:j]
            right_sub_grid = grid[1:len(grid), j + 1:len(grid)]
            sub_grid = np.concatenate((left_sub_grid, right_sub_grid), axis=1)

            sub_matches = collect_message_matches_from_grid(messages_collection_1, messages_collection_2, sub_grid)

            for sub_match in sub_matches:
                sub_match.insert(0, base_match)
                matches.append(sub_match)

    return matches


def valid_messages_match_between(message_1, message_2):
    message_1_argument_types = list(map(lambda var: var.sort(), message_1.payload))
    message_2_argument_types = list(map(lambda var: var.sort(), message_2.payload))

    return message_1_argument_types == message_2_argument_types
