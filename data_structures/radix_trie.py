import numpy as np

from data_structures.node_classes import RadixTrieNode

class RadixTrie:
    """
    Radix Trie Class.
    Features:
    - Stores keys and values in a radix trie structure.
    - Allows adding keys and values.
    - Allows searching for values by key.
    - Provides methods to get the maximum and minimum keys.
    """
    def __init__(self, keys, values, radix=None):
        self.root = RadixTrieNode(0)
        if len(keys) == 0:
            self.radix = radix or 2
            return
        keys, values = zip(*sorted(zip(keys, values)))
        
        self.radix = radix or int(np.sqrt(np.median(keys)))
        for k, v in zip(keys, values):
            self.add(k, v)

    
    def _break_key(self, key):
        stack = []
        while key > 0:
            stack.append(int(key % self.radix))
            key //= self.radix
        return stack[::-1]

        
    def add(self, key, value):
        stack = self._break_key(key)
        node = self.root

        for i in range(len(stack)):
            k = stack[i]
            if k not in node.children:
                node.children[k] = RadixTrieNode(k)
            node = node.children[k]
        if node.value is not None:
            return
        node.value = value
        
        
    def search(self, key):
        stack = self._break_key(key)
        node = self.root

        for k in stack:
            if k not in node.children:
                return None
            node = node.children[k]
        
        return node.value


    def getMaxKey(self):
        node = self.root
        max_key = 0

        while node.children:
            max_child = max(node.children.keys())
            max_key = max_key * self.radix + max_child
            node = node.children[max_child]

        return max_key
    

    def getMinKey(self):
        
        def dfs(node, path):
            if node.value is not None:
                return path

            for k in sorted(node.children.keys()):
                child_path = dfs(node.children[k], path * self.radix + k)
                if child_path is not None:
                    return child_path
            return None
        
        return dfs(self.root, 0)