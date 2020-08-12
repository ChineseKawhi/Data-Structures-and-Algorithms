class Node:
    def __init__(self, key):
        self.key = key
        self.children = {}
        self.hasValue = False

class Trie:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node('_')
        

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        cur = self.root
        for i in range(len(word)):
            if(word[i] in cur.children):
                cur = cur.children[word[i]]
            else:
                n = Node(word[i])
                cur.children[word[i]] = n
                cur = n
        cur.hasValue = True

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        node = self._searchPrefix(word)
        return node is not None and node.hasValue

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        return self._searchPrefix(prefix) is not None
    
    def _searchPrefix(self, prefix):
        cur = self.root
        for i in range(len(prefix)):
            if(prefix[i] in cur.children):
                cur = cur.children[prefix[i]]
            else:
                return None
        return cur