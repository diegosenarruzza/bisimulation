from models.assertable_finite_state_machines.afsm import AFSM
from models.assertable_finite_state_machines.assertable_label import AssertableLabel
from z3 import Int

afsm_example_3_2 = AFSM()

afsm_example_3_2.add_states('q0', 'q1', 'q2', 'q3', 'q4')
afsm_example_3_2.set_as_initial('q0')

afsm_example_3_2.add_transition_between(
    'q0',
    'q1',
    AssertableLabel('f(int x)', Int('x')),
    Int('x') != 0
)
afsm_example_3_2.add_transition_between(
    'q1',
    'q2',
    AssertableLabel('g'),
    Int('x') > 0
)
afsm_example_3_2.add_transition_between('q2', 'q4', AssertableLabel('h'))
afsm_example_3_2.add_transition_between(
    'q1',
    'q3',
    AssertableLabel('g'),
    Int('x') < 0
)
afsm_example_3_2.add_transition_between('q3', 'q4', AssertableLabel('h'))
