from models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int

cfsm = CommunicatingFiniteStateMachine(['customer', 'service'])

cfsm.add_states('q0', 'q1')
cfsm.set_as_initial('q0')
cfsm.add_transition_between(
    'q0',
    'q1',
    'customer -> service : f(int x)',
    Int('x') > 0
)
