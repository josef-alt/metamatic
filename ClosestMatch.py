from typing import Dict
import time

# very basic trie implementation
# todo thread safety
class _TrieNode:
    def __init__(self):
        self.end = False
        self.children = {}
    
class Trie:
    """Rudimentary trie data structure for finding string near-matches"""

    def __init__(self):
        self.root = _TrieNode()
        self.entries = 0

    def insert(self, word: str) -> None:
        """Inserts word into trie"""
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = _TrieNode()
            node = node.children[letter]
        node.end = True
        self.entries += 1        
    
    def find_exact(self, word: str) -> bool:
        """Returns true iff word is found in the trie"""
        return self._find_exact(self.root, word)
    
    def _find_exact(self, pos: _TrieNode, word: str) -> bool:
        if not word:
            return False
        
        if word[0] not in pos.children:
            return False

        if len(word) == 1:
            return pos.children[word].end
            
        return self._find_exact(pos.children[word[0]], word[1:])

    def _find(self, pos, word, curr, prev, results, max_cost):
        row = [ prev[0] + 1 ]

        for i in range(1, len(word) + 1):
            cost = 1 + min(row[i - 1], prev[i])
            if word[i - 1] == curr[-1]:
                cost = min(cost, prev[i - 1])
            row.append(cost)
            
        if pos.end and row[-1] <= max_cost:
            results.append((row[-1], curr))
        if min(row) <= max_cost:
            for (next_letter, node) in pos.children.items():
                self._find(node, word, curr + next_letter, row, results, min(max_cost, row[-1]))
        
    def find_nearest(self, word) -> str:
        """Returns the most similar word according to Levenshtein(?) distance"""
        results = []
        for (first_letter, node) in self.root.children.items():
            self._find(node, word, first_letter, range(len(word) + 1), results, len(word))
        return results