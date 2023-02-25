from models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int

cfsm = CommunicatingFiniteStateMachine('p1', 'p2')

cfsm.add_states('q0', 'q1')
cfsm.set_as_initial('q0')
cfsm.add_transition_between(
    'q0',
    'q1',
    'p1 -> p2 : f(int x)',
    Int('x') > 0
)
# cfsm.add_transition_between(
#     'q1',
#     'q0',
#     'p2 -> p1 : g(int y)',
#     Int('y') > Int('x')
# )
