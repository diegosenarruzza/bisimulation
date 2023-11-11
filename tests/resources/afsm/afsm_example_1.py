from src.cfsm_bisimulation.models.assertable_finite_state_machines.afsm import AFSM
from src.cfsm_bisimulation.models.assertable_finite_state_machines.assertable_label import AssertableLabel
from z3 import Int

afsm_example_1 = AFSM()

afsm_example_1.add_states('p0', 'p1')
afsm_example_1.set_as_initial('p0')

afsm_example_1.add_transition_between(
    'p0',
    'p1',
    AssertableLabel('f(int x)', Int('x')),
    Int('x') > 0
)
afsm_example_1.add_transition_between(
    'p1',
    'p0',
    AssertableLabel('g(int y)', Int('y')),
    Int('y') > Int('x')
)
