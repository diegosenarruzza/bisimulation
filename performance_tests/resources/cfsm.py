from models.communicating_system.cfsm import CommunicatingFiniteStateMachine as CFSM
from z3 import Int, String

cfsm = CFSM(['P1', 'P2', 'P3'])

cfsm.set_as_initial('q0')

cfsm.add_transition_between('q0', 'q1', 'P1P2! f1(int x1)')
cfsm.add_transition_between('q0', 'q2', 'P2P1? f2(bool x2)')
cfsm.add_transition_between('q1', 'q3', 'P1P2! f1(int x1)')
cfsm.add_transition_between('q2', 'q3', 'P2P1? f2(bool x2)')

x3_1 = Int('x3.1')
x3_2 = Int('x3.2')
cfsm.add_transition_between('q3', 'q4', 'P1P3! f3(int x3.1, int x3.2)', x3_1 != x3_2)

x4_2 = String('x4.2')
cfsm.add_transition_between('q3', 'q5', 'P1P3! f4(bool x4.1, string x4.2)', x4_2 != '')

initial_index = 5
