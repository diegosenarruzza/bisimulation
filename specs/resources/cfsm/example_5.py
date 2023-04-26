from models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int

cfsm_1 = CommunicatingFiniteStateMachine(['Consumer', 'Producer'])

cfsm_1.add_states('p0', 'p1', 'p2')
cfsm_1.set_as_initial('p0')

x = Int('x')

cfsm_1.add_transition_between('p0', 'p1', 'ConsumerProducer! add(int x)', x == 0)

cfsm_1.add_transition_between('p1', 'p2', 'ConsumerProducer! remove(int y)')

cfsm_2 = CommunicatingFiniteStateMachine(['Client', 'Wallet', 'Bank'])

# state names is not important, cause are not part of match.
# I set different to be not confuse in tests
cfsm_2.add_states('q0', 'q1', 'q2', 'q3', 'q4')
cfsm_2.set_as_initial('q0')

amount = Int('amount')

cfsm_2.add_transition_between('q0', 'q1', 'ClientWallet! deposit(int amount)', amount > 0)
cfsm_2.add_transition_between('q0', 'q2', 'ClientWallet! deposit(int amount)', amount < 0)
cfsm_2.add_transition_between('q0', 'q3', 'ClientWallet! deposit(int amount)', amount == 0)

cfsm_2.add_transition_between('q1', 'q4', 'ClientBank! withdraw(int another_amount)')
cfsm_2.add_transition_between('q2', 'q4', 'ClientBank! withdraw(int another_amount)')
cfsm_2.add_transition_between('q3', 'q4', 'ClientBank! withdraw(int another_amount)')
