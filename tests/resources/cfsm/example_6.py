from src.cfsm_bisimulation.models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int, String, And

cfsm_1 = CommunicatingFiniteStateMachine(['Consumer', 'Producer'])

cfsm_1.add_states('p0', 'p1', 'p2', 'p3')
cfsm_1.set_as_initial('p0')

x = Int('x')
y = Int('y')
z = String('z')

cfsm_1.add_transition_between('p0', 'p1', 'ConsumerProducer! f(int x)', x > 0)
cfsm_1.add_transition_between('p1', 'p3', 'ProducerConsumer? g(int y)', And([y > x, x > 0]))
cfsm_1.add_transition_between('p1', 'p2', 'ConsumerProducer! h(string z)')
cfsm_1.add_transition_between('p2', 'p1', 'ConsumerProducer! f(int x)')

cfsm_2 = CommunicatingFiniteStateMachine(['Consumer', 'Producer'])

# state names is not important, cause are not part of match.
# I set different to be not confuse in tests
cfsm_2.add_states('q0', 'q1', 'q2', 'q3')
cfsm_2.set_as_initial('q0')

cfsm_2.add_transition_between('q0', 'q1', 'ConsumerProducer! f(int x)', x > 0)
cfsm_2.add_transition_between('q1', 'q3', 'ProducerConsumer? g(int y)', y > x)
cfsm_2.add_transition_between('q1', 'q2', 'ConsumerProducer! h(string z)')
cfsm_2.add_transition_between('q2', 'q1', 'ConsumerProducer! f(int x)')
