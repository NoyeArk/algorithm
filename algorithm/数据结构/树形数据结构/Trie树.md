# Trie树

## 1. 定义

Trie树，又称字典树，是一种树形数据结构，用于高效地存储和检索字符串。它具有以下特点：

1. 根节点不包含字符，除根节点外每一个节点都只包含一个字符
2. 从根节点到某一节点，路径上经过的字符连接起来，为该节点对应的字符串
3. 每个节点的所有子节点包含的字符都不相同

## 2. 模板实现

```python
class Trie:
    def __init__(self):
        self.son = {}

    def insert(self, word: str) -> None:
        cur = self.son
        for c in word:
            if c not in cur:
                cur[c] = {}
            cur = cur[c]

    def search(self, word: str) -> bool:
        cur = self.son
        for c in word:
            if c not in cur:
                return False
            cur = cur[c]
        return True

    def startsWith(self, prefix: str) -> bool:
        cur = self.son
        for c in prefix:
            if c not in cur:
                return False
            cur = cur[c]
        return True
```

## 3. 例题

- [LCR 062. 实现 Trie (前缀树)](/leetcode/8-119经典题变种挑战/挑战%2010：前缀树/LCR%20062.%20实现%20Trie%20(前缀树).md)