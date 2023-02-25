from models.afsm import AFSM
from models.assertable_label import AssertableLabel
from z3 import Int

afsm_example_2_2 = AFSM()

afsm_example_2_2.add_states('q0', 'q1')
afsm_example_2_2.set_as_initial('q0')

afsm_example_2_2.add_transition_between(
    'q0',
    'q1',
    AssertableLabel('f(int x)', Int('x')),
    Int('x') > 0
)
afsm_example_2_2.add_transition_between(
    'q0',
    'q1',
    AssertableLabel('f(int x)', Int('x')),
    Int('x') < 0
)
