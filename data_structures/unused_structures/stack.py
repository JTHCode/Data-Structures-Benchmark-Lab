"""
Module for creating and modifying stacks.
"""


class Stack:
  """
  Creates a stack from a list of values of user input.
  Features:
  - Pushes a value onto the stack.
  - Pops a value off the stack.
  - Peek at top value of the stack.
  - Serialize for frontend.
  """

  def __init__(self, values=None):
    if values is None:
      values = []
    self.stack = values

  def __str__(self):
    return f'Stack({self.stack})'

  def push(self, value):
    self.stack.append(value)

  def pop(self):
    if len(self.stack) == 0:
      return None
    return self.stack.pop()

  def peek(self):
    if not self.stack:
      return None
    return self.stack[-1]

  def to_dict(self):
    return {"type": "stack", "values": self.stack}
