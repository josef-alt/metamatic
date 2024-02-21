from typing import Dict

# very basic trie implementation
# todo thread safety
class _TrieNode:
    def __init__(self):
        self.end = False
        self.children = {}
    
class Trie:
    """Rudimentary trie data structure for finding string near-matches"""
    root: _TrieNode
    entries: int

    def __init__(self):
        self.root = _TrieNode()
        self.entries = 0

    def insert(self, word: str) -> None:
        """Inserts word into trie"""
        self._insert(self.root, word)

    # could eliminate helper
    def _insert(self, pos: _TrieNode, word: str) -> None:
        if not word:
            pos.end = True
            return
        if word[0] not in pos.children:
            pos.children[word[0]] = _TrieNode()
        self._insert(pos.children[word[0]], word[1:])
    
    def find_exact(self, word: str) -> bool:
        """Returns true iff word is found in the trie"""
        return self._find_exact(self.root, word)
    
    def _find_exact(self, pos: _TrieNode, word: str) -> bool:
        if not word:
            return pos.end
        if word[0] not in pos.children:
            return False
        return self._find_exact(pos.children[word[0]], word[1:])

    def find_nearest(self, word) -> str:
        """Returns the most similar word according to Levenshtein(?) distance"""
        return 1