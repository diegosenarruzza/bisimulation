# Precondicion: len(participants_collection_1) == len(participants_collection_2)
def match_participants(participants_collection_1, participants_collection_2):
    matches = []
    participants_size = len(participants_collection_1)

    for i in range(0, participants_size):
        # Armo el primer posible match para los participantes
        match = {}
        for j in range(0, participants_size):
            participant_2_index = (j + i) % participants_size
            match[participants_collection_1[j]] = participants_collection_2[participant_2_index]
        matches.append(match)

    return matches
