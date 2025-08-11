"""
Module for creating and modifying queues.
"""
from collections import deque


class Queue:
  """
  Creates a queue from a list of values of user input.
  Features:
  - Enqueues a value or multiple values onto the queue (front or back).
  - Dequeues a value or multiple values off the queue (front or back).
  - Allows for a max size to be set and updated.
  - Allows for queue to be rotated.
  - Serialize for frontend.
  """

  def __init__(self, values, max_size=None):
    self.max_size = max_size
    if max_size is not None:
      if max_size < len(values):
        raise ValueError("Initial values exceed max size")
      self.que = deque(values, maxlen=max_size)
    else:
      self.que = deque(values)

  def __str__(self):
    return f'Queue({list(self.que)})'

  def enqueueFront(self, values):
    if self.max_size and isinstance(values,
                                    list) and len(values) > self.max_size:
      raise ValueError("Enqueue values exceed max size")
    self.que.extend(values)

  def enqueueBack(self, values):
    if self.max_size and isinstance(values,
                                    list) and len(values) > self.max_size:
      raise ValueError("Enqueue values exceed max size")
    self.que.extendleft(values)

  def dequeueFront(self, count=1):
    if count > len(self.que):
      raise ValueError("Dequeue count exceeds queue size")
    return [self.que.pop() for _ in range(count)]

  def dequeueBack(self, count=1):
    if count > len(self.que):
      raise ValueError("Dequeue count exceeds queue size")
    return [self.que.popleft() for _ in range(count)]

  def rotate(self, n):
    if n > 10000:
      raise ValueError("Rotation count exceeds max limit")
    self.que.rotate(n)

  def to_dict(self):
    return {
        "type": "queue",
        "values": list(self.que),
    }
