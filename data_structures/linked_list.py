# /home/runner/workspace/data_structures/linked_list.py
"""
Module for creating and modifying linked lists.
"""
from data_structures.node_classes import listNode

class linkedList:
    """
    Doubly linked list keyed by `key` with value `value`.
    Maintains nodes in ascending key order on insert.
    """

    def __init__(self, keys, values):
        self.head = None
        self.tail = None
        for key, val in zip(keys, values):
            self.add(key, val)

    def search(self, key):
        """Return the value for key, or None if not found."""
        curr = self.head
        while curr and curr.key != key:
            curr = curr.next
        return curr.value if curr else None  # return node.value for benches

    def add(self, key, value):
        """Insert (key, value) keeping list sorted by key."""
        if not self.head:
            self.add_Head(key, value)
            return

        curr = self.head
        while curr and curr.key < key:
            curr = curr.next

        if not curr:               # insert at tail
            self.add_Tail(key, value)
            return

        if curr == self.head:      # insert at head
            self.add_Head(key, value)
            return

        # insert before curr
        new_node = listNode(key, value)
        prev = curr.prev
        prev.next = new_node
        new_node.prev = prev
        new_node.next = curr
        curr.prev = new_node

    def add_Tail(self, key, value):
        new_node = listNode(key, value)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def add_Head(self, key, value):
        new_node = listNode(key, value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def delete(self, key):
        curr = self.head
        while curr and curr.key != key:
            curr = curr.next
        if not curr:
            return
        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next
        if curr.next:
            curr.next.prev = curr.prev
        else:
            self.tail = curr.prev

    def getMaxKey(self):
        return self.tail.key if self.tail else None

    def getMinKey(self):
        return self.head.key if self.head else None
