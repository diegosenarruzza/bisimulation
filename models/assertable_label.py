class AssertableLabel:

  def __init__(self, string_label, variable):
    self.string_label = string_label
    self.variable = variable

  def __eq__(self, other_label):
    return self.string_label == other_label.string_label

  def __repr__(self):
    return self.string_label