from models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int, And

x = Int('x')
y = Int('y')

cfsm = CommunicatingFiniteStateMachine(['A1', 'A2'])

cfsm.set_as_initial('q0')
cfsm.add_transition_between('q0', 'q1', 'A1A2!f(int x)')
cfsm.add_transition_between('q1', 'q2', 'A2A1?g(int y)', And([x > 0, y > 0]))
cfsm.add_transition_between('q2', 'q1', 'A1A2!m1()')
cfsm.add_transition_between('q1', 'q3', 'A2A1?g(int y)', y <= 0)
cfsm.add_transition_between('q3', 'q4', 'A1A2!m2()')
