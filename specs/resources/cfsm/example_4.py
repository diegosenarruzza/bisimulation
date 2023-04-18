from models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int

cfsm_1 = CommunicatingFiniteStateMachine(['consumer', 'adder', 'remover'])

cfsm_1.add_states('p0', 'p1', 'p2')
cfsm_1.set_as_initial('p0')

x = Int('x')

cfsm_1.add_transition_between('p0', 'p1', 'consumer -> adder : add(int x)', x != 0)

cfsm_1.add_transition_between('p1', 'p2', 'consumer -> remover : remove(int y)')

cfsm_2 = CommunicatingFiniteStateMachine(['client', 'wallet', 'bank'])

# state names is not important, cause are not part of match.
# I set different to be not confuse in tests
cfsm_2.add_states('q0', 'q1', 'q2', 'q3')
cfsm_2.set_as_initial('q0')

amount = Int('amount')

cfsm_2.add_transition_between('q0', 'q1', 'client -> wallet : deposit(int amount)', amount > 0)
cfsm_2.add_transition_between('q0', 'q2', 'client -> wallet : deposit(int amount)', amount < 0)

cfsm_2.add_transition_between('q1', 'q3', 'client -> bank : withdraw(int another_amount)')
cfsm_2.add_transition_between('q2', 'q3', 'client -> bank : withdraw(int another_amount)')
