from models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import String

cfsm_1 = CommunicatingFiniteStateMachine(['client', 'service'])

cfsm_1.add_states('p0', 'p1', 'p2')
cfsm_1.set_as_initial('p0')

user = String('user')

cfsm_1.add_transition_between('p0', 'p1', 'client -> service : login(string user)')
cfsm_1.add_transition_between('p1', 'p2', 'service -> client : success()', user == 'root')
cfsm_1.add_transition_between('p1', 'p2', 'service -> client : success()', user == 'user')
cfsm_1.add_transition_between('p2', 'p0', 'client -> service : signUp()')

cfsm_2 = CommunicatingFiniteStateMachine(['client', 'db'])

# state names is not important, cause are not part of match.
# I set different to be not confuse in tests
cfsm_2.add_states('q0', 'q1', 'q2', 'q3')
cfsm_2.set_as_initial('q0')

username = String('username')

cfsm_2.add_transition_between('q0', 'q1', 'client -> db : login(string username)')
cfsm_2.add_transition_between('q1', 'q2', 'db -> client : ok()', username == 'root')
cfsm_2.add_transition_between('q1', 'q3', 'db -> client : ok()', username == 'user')
cfsm_2.add_transition_between('q2', 'q0', 'client -> db : signOff()')
cfsm_2.add_transition_between('q3', 'q0', 'client -> db : signOff()')
