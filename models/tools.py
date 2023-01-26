from itertools import chain, combinations

def powerset(iterable):
  "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
  s = list(iterable)
  return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def collect_variables(assertion):
  variables = set()

  if len(assertion.children()) > 0:
    for child in assertion.children():
      variables = variables.union(collect_variables(child))
  else:
    variables.add(assertion)

  return variables