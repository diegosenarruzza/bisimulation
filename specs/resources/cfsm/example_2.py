from models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int

cfsm_1 = CommunicatingFiniteStateMachine(['consumer', 'producer'])

cfsm_1.add_states('p0', 'p1')
cfsm_1.set_as_initial('p0')

cfsm_1.add_transition_between(
    'p0',
    'p1',
    'consumer -> producer : add(int x)',
    Int('x') > 0
)

cfsm_2 = CommunicatingFiniteStateMachine(['client', 'shop'])

# state names is not important, cause are not part of match.
# I set different to be not confuse in tests
cfsm_2.add_states('q0', 'q1')
cfsm_2.set_as_initial('q0')

cfsm_2.add_transition_between(
    'q0',
    'q1',
    'client -> shop : add_to_cart(int number)',
    Int('number') > 0
)
