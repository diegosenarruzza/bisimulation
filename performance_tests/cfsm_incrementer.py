import random
from z3 import Int
from models.communicating_system.cfsm import CommunicatingFiniteStateMachine as CFSM


class CFSMIncrementer:

    def __init__(self):
        self.types = ['int', 'bool', 'string']

    def copy(self, cfsm: CFSM) -> CFSM:
        copy_cfsm = CFSM(list([cfsm.main_participant] + cfsm.participants))
        for state_id, transitions in cfsm.transitions_by_source_id.items():
            for transition in transitions:
                copy_cfsm.add_transition_between(
                    transition.source.id,
                    transition.target.id,
                    str(transition.label),
                    transition.assertion.expression
                )

        copy_cfsm.set_as_initial(cfsm.initial_state.id)
        return copy_cfsm

    def randomize(self, cfsm):
        randomized_cfsm = self.copy(cfsm)

        random_state_ids = random.sample(list(randomized_cfsm.states), len(randomized_cfsm.states))
        randomized_cfsm.states = {state_id: randomized_cfsm.states[state_id] for state_id in random_state_ids}

        for state_id, transitions in randomized_cfsm.transitions_by_source_id.items():
            randomized_cfsm.transitions_by_source_id[state_id] = random.sample(transitions, len(transitions))

        random_transitions_by_source_id = random.sample(list(randomized_cfsm.transitions_by_source_id), len(randomized_cfsm.transitions_by_source_id))
        randomized_cfsm.transitions_by_source_id = {state_id: randomized_cfsm.transitions_by_source_id[state_id] for state_id in random_transitions_by_source_id}

        return randomized_cfsm

    def increment(self, cfsm: CFSM, size: int, index: int) -> (CFSM, int):
        new_cfsm = self.copy(cfsm)
        main_participant = new_cfsm.main_participant
        rest_of_participants = new_cfsm.participants

        current_state_ids = list(new_cfsm.states.keys())

        for i in range(size):
            source_state_id = random.choice(current_state_ids)
            target_state_id = f'q{len(new_cfsm.states) + i}'
            participant = random.choice(rest_of_participants)

            payload_arity = random.randint(1, 3) # entre 1 y 3 parametros
            payload = [f'{random.choice(self.types)} x{index}.{i}' for i in range(payload_arity)]
            message = f"f{index}({','.join(payload)})"

            action = f'{main_participant}{participant}! {message}'
            new_cfsm.add_transition_between(source_state_id, target_state_id, action)
            index += 1

        return new_cfsm, index

    def increment_splitting_transitions_in_new_states(self, cfsm: CFSM, size: int, index: int) -> (CFSM, int):
        new_cfsm = self.copy(cfsm)
        main_participant = new_cfsm.participants[0]
        rest_of_participants = new_cfsm.participants[1:]

        current_state_ids = list(new_cfsm.states.keys())

        for i in range(int(size/2)):
            source_state_id = random.choice(current_state_ids)
            target_state_id = f'q{len(new_cfsm.states) + i}'
            participant = random.choice(rest_of_participants)

            payload_arity = random.randint(1, 3) # entre 1 y 3 parametros
            payload = [f'{random.choice(self.types)} x{index}.{i}' for i in range(payload_arity)]
            integer_variable_name = f'x{index}.{len(payload)}'

            message = f"f{index}({','.join(payload + [f'int {integer_variable_name}'])})"

            action = f'{main_participant}{participant}! {message}'
            new_cfsm.add_transition_between(source_state_id, target_state_id, action, Int(integer_variable_name) > 0)
            new_cfsm.add_transition_between(source_state_id, target_state_id, action, Int(integer_variable_name) < 0)
            index += 1

        return new_cfsm, index

    def increment_splitting_transitions_in_new_states(self, cfsm: CFSM, size: int, index: int) -> (CFSM, int):
        new_cfsm = self.copy(cfsm)
        main_participant = new_cfsm.participants[0]
        rest_of_participants = new_cfsm.participants[1:]

        current_state_ids = list(new_cfsm.states.keys())

        for i in range(int(size/2)):
            source_state_id = random.choice(current_state_ids)
            target_state_id_1 = f'q{len(new_cfsm.states) + i}[1]'
            target_state_id_2 = f'q{len(new_cfsm.states) + i}[2]'

            participant = random.choice(rest_of_participants)

            payload_arity = random.randint(1, 3) # entre 1 y 3 parametros
            payload = [f'{random.choice(self.types)} x{index}.{i}' for i in range(payload_arity)]
            integer_variable_name = f'x{index}.{len(payload)}'

            message = f"f{index}({','.join(payload + [f'int {integer_variable_name}'])})"

            action = f'{main_participant}{participant}! {message}'
            new_cfsm.add_transition_between(source_state_id, target_state_id_1, action, Int(integer_variable_name) > 0)
            new_cfsm.add_transition_between(source_state_id, target_state_id_2, action, Int(integer_variable_name) < 0)
            index += 1

        return new_cfsm, index
