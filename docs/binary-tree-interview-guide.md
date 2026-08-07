# 二叉树面试全攻略

> 一篇搞定所有难度的二叉树算法面试。每个算法：可直接默写的 Python 代码 + 一行复杂度。

## 目录

- [0. 节点定义](#0-节点定义)
- [1. 遍历 (Traversal)](#1-遍历-traversal)
- [2. 核心属性算法](#2-核心属性算法)
- [3. 判定类问题](#3-判定类问题)
- [4. 路径问题](#4-路径问题)
- [5. BST 专题](#5-bst-专题)
- [6. 构造与修改](#6-构造与修改)
- [7. 最近公共祖先 LCA](#7-最近公共祖先-lca)
- [8. 序列化与反序列化](#8-序列化与反序列化)
- [9. 经典进阶 (Hard)](#9-经典进阶-hard)
- [10. 心法总结](#10-心法总结)
- [附录: 题号速查](#附录-题号速查)

---

## 0. 节点定义

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# N 叉树
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children or []
```

---

## 1. 遍历 (Traversal)

四种顺序：前序 (根左右) / 中序 (左根右) / 后序 (左右根) / 层序 (BFS)。

### 1.1 递归版 (背这个就够)

```python
def preorder(root):  # 前序
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def inorder(root):   # 中序
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def postorder(root): # 后序
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]
# time: O(n)  space: O(h)
```

### 1.2 迭代版 - 通用栈模板

**关键技巧**：前序最简单；中序用栈一路向左压到底；后序可用"根右左"反转得到"左右根"。

```python
def preorder_iter(root):
    if not root: return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.right: stack.append(node.right)  # 先压右
        if node.left:  stack.append(node.left)   # 再压左
    return res

def inorder_iter(root):
    stack, res, cur = [], [], root
    while cur or stack:
        while cur:                  # 一路向左压栈
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        res.append(cur.val)
        cur = cur.right
    return res

def postorder_iter(root):           # 反转的前序变种
    if not root: return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)        # 根右左
        if node.left:  stack.append(node.left)
        if node.right: stack.append(node.right)
    return res[::-1]                # 反转得左右根
# time: O(n)  space: O(h)
```

### 1.3 层序遍历 BFS

```python
from collections import deque

def levelOrder(root):
    if not root: return []
    res, q = [], deque([root])
    while q:
        level, n = [], len(q)
        for _ in range(n):          # 关键: 按层切
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res
# time: O(n)  space: O(w)  w = 最大宽度
```

### 1.4 Morris 遍历 (空间 O(1))

用线索化指针实现 O(1) 空间中序。面试冷门但加分。

```python
def morris_inorder(root):
    res, cur = [], root
    while cur:
        if not cur.left:
            res.append(cur.val)
            cur = cur.right
        else:
            prev = cur.left
            while prev.right and prev.right != cur:  # 找前驱
                prev = prev.right
            if not prev.right:        # 建线索
                prev.right = cur
                cur = cur.left
            else:                     # 已建过, 断线索
                prev.right = None
                res.append(cur.val)
                cur = cur.right
    return res
# time: O(n)  space: O(1)
```

---

## 2. 核心属性算法

### 2.1 最大深度 / 树高

```python
def maxDepth(root):
    if not root: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
# time: O(n)  space: O(h)
```

### 2.2 最小深度 (根到最近叶子)

```python
def minDepth(root):
    if not root: return 0
    if not root.left:  return 1 + minDepth(root.right)
    if not root.right: return 1 + minDepth(root.left)
    return 1 + min(minDepth(root.left), minDepth(root.right))
# time: O(n)  space: O(h)
```

### 2.3 节点总数

```python
def countNodes(root):
    if not root: return 0
    return 1 + countNodes(root.left) + countNodes(root.right)
# time: O(n)  space: O(h)
```

### 2.4 完全二叉树节点数 (利用满性, < O(n))

```python
def countNodes_complete(root):
    if not root: return 0
    l, r, hl, hr = root, root, 0, 0
    while l: l, hl = l.left, hl + 1
    while r: r, hr = r.right, hr + 1
    if hl == hr: return (1 << hl) - 1   # 满树 2^h - 1
    return 1 + countNodes_complete(root.left) + countNodes_complete(root.right)
# time: O(log²n)  space: O(logn)
```

### 2.5 叶子节点数

```python
def countLeaves(root):
    if not root: return 0
    if not root.left and not root.right: return 1
    return countLeaves(root.left) + countLeaves(root.right)
# time: O(n)  space: O(h)
```

### 2.6 第 k 层节点数

```python
def countLevelK(root, k):           # 根为第 1 层
    if not root or k < 1: return 0
    if k == 1: return 1
    return countLevelK(root.left, k-1) + countLevelK(root.right, k-1)
# time: O(n)  space: O(h)
```

### 2.7 树的直径 (任意两节点最长路径边数)

**经典模板**: 后序 + 全局变量。

```python
def diameterOfBinaryTree(root):
    self.ans = 0
    def depth(node):
        if not node: return 0
        l, r = depth(node.left), depth(node.right)
        self.ans = max(self.ans, l + r)      # 经过 node 的最长路径
        return 1 + max(l, r)
    depth(root)
    return self.ans
# time: O(n)  space: O(h)
```

### 2.8 最长同值路径

```python
def longestUnivaluePath(root):
    self.ans = 0
    def dfs(node):
        if not node: return 0
        l, r = dfs(node.left), dfs(node.right)
        lp = l + 1 if node.left and node.left.val == node.val else 0
        rp = r + 1 if node.right and node.right.val == node.val else 0
        self.ans = max(self.ans, lp + rp)
        return max(lp, rp)
    dfs(root)
    return self.ans
# time: O(n)  space: O(h)
```

### 2.9 二叉树最大宽度 (含空节点)

```python
def widthOfBinaryTree(root):
    self.ans = 0
    q = deque([(root, 0)])
    while q:
        n = len(q)
        first = q[0][1]
        for _ in range(n):
            node, idx = q.popleft()
            if node.left:  q.append((node.left, 2*idx))
            if node.right: q.append((node.right, 2*idx+1))
        self.ans = max(self.ans, idx - first + 1)
    return self.ans
# time: O(n)  space: O(w)
```

---

## 3. 判定类问题

### 3.1 判平衡 (AVL 条件)

```python
def isBalanced(root):
    def check(node):
        if not node: return 0
        l, r = check(node.left), check(node.right)
        if l == -1 or r == -1 or abs(l - r) > 1: return -1
        return 1 + max(l, r)
    return check(root) != -1
# time: O(n)  space: O(h)
```

### 3.2 判对称

```python
def isSymmetric(root):
    def same(a, b):
        if not a and not b: return True
        if not a or not b: return False
        return a.val == b.val and same(a.left, b.right) and same(a.right, b.left)
    return not root or same(root.left, root.right)
# time: O(n)  space: O(h)
```

### 3.3 判两棵树相同

```python
def isSameTree(p, q):
    if not p and not q: return True
    if not p or not q: return False
    return p.val == q.val \
        and isSameTree(p.left, q.left) \
        and isSameTree(p.right, q.right)
# time: O(n)  space: O(h)
```

### 3.4 判子树 (subtree-of-another-tree)

```python
def isSubtree(root, sub):
    if not root: return not sub
    return isSameTree(root, sub) or isSubtree(root.left, sub) or isSubtree(root.right, sub)
# time: O(n*m)  space: O(h)
```

### 3.5 判完全二叉树

```python
def isCompleteTree(root):
    q, seen_null = deque([root]), False
    while q:
        node = q.popleft()
        if not node:
            seen_null = True
        else:
            if seen_null: return False     # 空后又有非空
            q.append(node.left)
            q.append(node.right)
    return True
# time: O(n)  space: O(w)
```

### 3.6 判满二叉树

```python
def isFull(root):
    if not root: return True
    if not root.left and not root.right: return True
    if root.left and root.right:
        return isFull(root.left) and isFull(root.right)
    return False
# time: O(n)  space: O(h)
```

---

## 4. 路径问题

### 4.1 根到叶路径和 = target

```python
def hasPathSum(root, target):
    if not root: return False
    if not root.left and not root.right:
        return root.val == target
    return hasPathSum(root.left, target - root.val) \
        or hasPathSum(root.right, target - root.val)
# time: O(n)  space: O(h)
```

### 4.2 打印所有根到叶路径

```python
def binaryTreePaths(root):
    res = []
    def dfs(node, path):
        if not node: return
        path += [str(node.val)]
        if not node.left and not node.right:
            res.append("->".join(path))
        else:
            dfs(node.left, path)
            dfs(node.right, path)
        path.pop()
    dfs(root, [])
    return res
# time: O(n²)  space: O(h²)
```

### 4.3 任意路径最大和 (hard 经典)

**模板**: 后序 + 子树贡献。

```python
def maxPathSum(root):
    self.ans = float('-inf')
    def gain(node):
        if not node: return 0
        l = max(gain(node.left), 0)     # 负贡献舍弃
        r = max(gain(node.right), 0)
        self.ans = max(self.ans, node.val + l + r)
        return node.val + max(l, r)     # 只能选一侧向上
    gain(root)
    return self.ans
# time: O(n)  space: O(h)
```

### 4.4 路径和 = target (任意节点起, 向下)

前缀和 + DFS。

```python
def pathSum(root, target):
    from collections import defaultdict
    self.cnt = 0
    prefix = defaultdict(int)
    prefix[0] = 1
    def dfs(node, cur):
        if not node: return
        cur += node.val
        self.cnt += prefix[cur - target]
        prefix[cur] += 1
        dfs(node.left, cur); dfs(node.right, cur)
        prefix[cur] -= 1                   # 回溯!
    dfs(root, 0)
    return self.cnt
# time: O(n)  space: O(n)
```

### 4.5 左叶子之和

```python
def sumOfLeftLeaves(root):
    def is_leaf(n): return n and not n.left and not n.right
    if not root: return 0
    ans = root.left.val if is_leaf(root.left) else 0
    return ans + sumOfLeftLeaves(root.left) + sumOfLeftLeaves(root.right)
# time: O(n)  space: O(h)
```

### 4.6 根到叶数字串求和

```python
def sumNumbers(root):
    self.total = 0
    def dfs(node, cur):
        if not node: return
        cur = cur * 10 + node.val
        if not node.left and not node.right:
            self.total += cur
        dfs(node.left, cur); dfs(node.right, cur)
    dfs(root, 0)
    return self.total
# time: O(n)  space: O(h)
```

---

## 5. BST 专题

性质: 中序遍历**严格递增**。

### 5.1 判合法 BST

```python
def isValidBST(root):
    def check(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return check(node.left, lo, node.val) and check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))
# time: O(n)  space: O(h)
```

### 5.2 BST 第 k 小 (中序)

```python
def kthSmallest(root, k):
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0: return cur.val
        cur = cur.right
# time: O(h+k)  space: O(h)
```

### 5.3 BST 搜索

```python
def searchBST(root, val):
    while root:
        if val == root.val: return root
        root = root.left if val < root.val else root.right
    return None
# time: O(h)  space: O(1)
```

### 5.4 BST 插入

```python
def insertIntoBST(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left = insertIntoBST(root.left, val)
    else:             root.right = insertIntoBST(root.right, val)
    return root
# time: O(h)  space: O(h)
```

### 5.5 BST 删除

```python
def deleteNode(root, key):
    if not root: return None
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        if not root.right: return root.left
        if not root.left:  return root.right
        succ = root.right
        while succ.left: succ = succ.left        # 找后继
        root.val = succ.val
        root.right = deleteNode(root.right, succ.val)
    return root
# time: O(h)  space: O(h)
```

### 5.6 BST 中序下一个节点 (后继)

```python
def inorderSuccessor(root, p):
    succ = None
    while root:
        if p.val < root.val:
            succ = root
            root = root.left
        else:
            root = root.right
    return succ
# time: O(h)  space: O(1)
```

### 5.7 恢复被交换的两个节点 (recover-bst)

```python
def recoverTree(root):
    self.prev = self.first = self.second = None
    def inorder(node):
        if not node: return
        inorder(node.left)
        if self.prev and self.prev.val > node.val:
            if not self.first: self.first = self.prev
            self.second = node
        self.prev = node
        inorder(node.right)
    inorder(root)
    self.first.val, self.second.val = self.second.val, self.first.val
# time: O(n)  space: O(h)
```

### 5.8 BST 众数 (出现最多的值)

```python
def findMode(root):
    self.prev = self.cnt = self.maxc = 0
    self.res = []
    def dfs(n):
        if not n: return
        dfs(n.left)
        self.cnt = self.cnt + 1 if self.prev == n.val else 1
        self.prev = n.val
        if self.cnt > self.maxc:
            self.maxc, self.res = self.cnt, [n.val]
        elif self.cnt == self.maxc:
            self.res.append(n.val)
        dfs(n.right)
    dfs(root)
    return self.res
# time: O(n)  space: O(h)
```

### 5.9 BST 两节点之和

```python
def findTarget(root, k):
    seen = set()
    def dfs(n):
        if not n: return False
        if k - n.val in seen: return True
        seen.add(n.val)
        return dfs(n.left) or dfs(n.right)
    return dfs(root)
# time: O(n)  space: O(n)
```

### 5.10 BST 区间和

```python
def rangeSumBST(root, lo, hi):
    if not root: return 0
    if root.val < lo:  return rangeSumBST(root.right, lo, hi)
    if root.val > hi:  return rangeSumBST(root.left, lo, hi)
    return root.val + rangeSumBST(root.left, lo, hi) + rangeSumBST(root.right, lo, hi)
# time: O(n)  space: O(h)
```

---

## 6. 构造与修改

### 6.1 前序 + 中序 重建

```python
def buildTree_pre_in(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    self.i = 0
    def build(lo, hi):
        if lo > hi: return None
        val = preorder[self.i]; self.i += 1
        root = TreeNode(val)
        root.left  = build(lo, idx[val] - 1)
        root.right = build(idx[val] + 1, hi)
        return root
    return build(0, len(inorder) - 1)
# time: O(n)  space: O(n)
```

### 6.2 中序 + 后序 重建

```python
def buildTree_in_post(inorder, postorder):
    idx = {v: i for i, v in enumerate(inorder)}
    self.i = len(postorder) - 1
    def build(lo, hi):
        if lo > hi: return None
        val = postorder[self.i]; self.i -= 1     # 后序从后往前
        root = TreeNode(val)
        root.right = build(idx[val] + 1, hi)     # 先右后左
        root.left  = build(lo, idx[val] - 1)
        return root
    return build(0, len(inorder) - 1)
# time: O(n)  space: O(n)
```

### 6.3 翻转二叉树

```python
def invertTree(root):
    if not root: return None
    root.left, root.right = root.right, root.left
    invertTree(root.left); invertTree(root.right)
    return root
# time: O(n)  space: O(h)
```

### 6.4 合并两棵树

```python
def mergeTrees(t1, t2):
    if not t1: return t2
    if not t2: return t1
    t1.val += t2.val
    t1.left  = mergeTrees(t1.left, t2.left)
    t1.right = mergeTrees(t1.right, t2.right)
    return t1
# time: O(n)  space: O(h)
```

### 6.5 展开为右链表 (flatten)

```python
def flatten(root):
    cur = root
    while cur:
        if cur.left:
            prev = cur.left
            while prev.right: prev = prev.right    # 左子树最右节点
            prev.right = cur.right                  # 接右子树
            cur.right = cur.left
            cur.left = None
        cur = cur.right
# time: O(n)  space: O(1)
```

### 6.6 填充每个节点 next 右指针

```python
def connect(root):
    cur = root
    while cur and cur.left:
        head = cur
        while head:
            head.left.next = head.right
            if head.next:
                head.right.next = next.head.left if False else head.next.left
            head = head.next
        cur = cur.left
    return root
# 修正版 (完美二叉树):
def connect_perfect(root):
    if not root: return None
    if root.left:
        root.left.next = root.right
        if root.next:
            root.right.next = root.next.left
        connect_perfect(root.left)
        connect_perfect(root.right)
    return root
# time: O(n)  space: O(1) (递归版 O(h))
```

---

## 7. 最近公共祖先 LCA

### 7.1 普通二叉树 LCA

```python
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q: return root
    l = lowestCommonAncestor(root.left, p, q)
    r = lowestCommonAncestor(root.right, p, q)
    if l and r: return root          # 一边一个 -> 当前就是 LCA
    return l or r
# time: O(n)  space: O(h)
```

### 7.2 BST 的 LCA (利用有序性)

```python
def lowestCommonAncestor_BST(root, p, q):
    while root:
        if root.val < p.val and root.val < q.val: root = root.right
        elif root.val > p.val and root.val > q.val: root = root.left
        else: return root            # 分叉点
# time: O(h)  space: O(1)
```

### 7.3 最深叶子节点的 LCA

```python
def lcaDeepestLeaves(root):
    def dfs(node, depth):
        if not node: return (None, depth)
        l, dl = dfs(node.left, depth + 1)
        r, dr = dfs(node.right, depth + 1)
        if dl == dr: return (node, dl)
        return (l, dl) if dl > dr else (r, dr)
    return dfs(root, 0)[0]
# time: O(n)  space: O(h)
```

---

## 8. 序列化与反序列化

### 8.1 前序 + null 标记

```python
def serialize(root):
    res = []
    def dfs(n):
        if not n:
            res.append("#"); return
        res.append(str(n.val))
        dfs(n.left); dfs(n.right)
    dfs(root)
    return ",".join(res)

def deserialize(data):
    it = iter(data.split(","))
    def build():
        v = next(it)
        if v == "#": return None
        node = TreeNode(int(v))
        node.left = build(); node.right = build()
        return node
    return build()
# time: O(n)  space: O(n)
```

### 8.2 层序序列化

```python
from collections import deque
def serialize_level(root):
    if not root: return "#"
    res, q = [], deque([root])
    while q:
        n = q.popleft()
        res.append(str(n.val) if n else "#")
        if n:
            q.append(n.left); q.append(n.right)
    return ",".join(res)
# time: O(n)  space: O(n)
```

---

## 9. 经典进阶 (Hard)

### 9.1 打家劫舍 III (树形 DP)

```python
def rob(root):
    def dfs(n):
        if not n: return (0, 0)      # (偷当前, 不偷当前)
        l, r = dfs(n.left), dfs(n.right)
        take = n.val + l[1] + r[1]
        skip = max(l) + max(r)
        return (take, skip)
    return max(dfs(root))
# time: O(n)  space: O(h)
```

### 9.2 监控二叉树

```python
def minCameraCover(root):
    self.cnt = 0
    def dfs(n):
        if not n: return 2                # 空节点视为已覆盖
        l, r = dfs(n.left), dfs(n.right)
        if l == 0 or r == 0:              # 有孩子未覆盖
            self.cnt += 1
            return 1                      # 当前放监控
        if l == 1 or r == 1:              # 孩子有监控
            return 2                      # 当前被覆盖
        return 0                          # 当前未被覆盖
    if dfs(root) == 0: self.cnt += 1      # 根未被覆盖, 补一个
    return self.cnt
# time: O(n)  space: O(h)
```

### 9.3 两节点间最短路径长度 (转 LCA + 深度差)

```python
def findDistance(root, p, q):
    lca = lowestCommonAncestor(root, p, q)   # 见 7.1
    def depth(n, target, d):
        if not n: return -1
        if n == target: return d
        l = depth(n.left, target, d+1)
        return l if l != -1 else depth(n.right, target, d+1)
    return depth(lca, p, 0) + depth(lca, q, 0)
# time: O(n)  space: O(h)
```

### 9.4 路径和方案打印 (任意路径)

在 4.4 基础上记录路径。

```python
def pathSum_paths(root, target):
    res, path = [], []
    from collections import defaultdict
    prefix = defaultdict(list)
    prefix[0].append(-1)               # 占位, 表示从根开始
    def dfs(n, cur, depth):
        if not n: return
        path.append(n.val)
        cur += n.val
        for _ in range(len(prefix[cur - target])):
            start = prefix[cur - target][0]
            res.append(path[start+1:])  # 实际需更细致实现
        prefix[cur].append(depth)
        dfs(n.left, cur, depth+1); dfs(n.right, cur, depth+1)
        prefix[cur].pop(); path.pop()
    dfs(root, 0, 0)
    return res
# 简化记忆版: 见 4.4
```

### 9.5 所有距离为 K 的节点

```python
def distanceK(root, target, k):
    from collections import defaultdict, deque
    g = defaultdict(list)
    def build(a, b):
        if not a: return
        if b: g[a.val].append(b.val); g[b.val].append(a.val)
        build(a.left, a); build(a.right, a)
    build(root, None)
    q, seen = deque([(target.val, 0)]), {target.val}
    res = []
    while q:
        node, d = q.popleft()
        if d == k: res.append(node); continue
        for nb in g[node]:
            if nb not in seen:
                seen.add(nb); q.append((nb, d+1))
    return res
# time: O(n)  space: O(n)
```

### 9.6 节点值等于子节点之和 (find-bottom-left)

```python
def findBottomLeftValue(root):
    q = deque([root])
    while q:
        node = q.popleft()
        if node.right: q.append(node.right)  # 先右后左, 最后一个就是左下
        if node.left:  q.append(node.left)
    return node.val
# time: O(n)  space: O(w)
```

---

## 10. 心法总结

### 10.1 三种遍历的选用

| 场景 | 用什么 |
|------|--------|
| 自顶向下传信息 (如路径和) | **前序** + 参数 |
| 依赖左右子树结果 (如树高、直径) | **后序** + 返回值 |
| 按层处理 (如 BFS、最短距离) | **层序** + queue |
| BST 有序性 | **中序** = 升序 |

### 10.2 两种递归范式

**范式 A - 自顶向下 (前序)**

```python
def dfs(node, state_from_parent):
    # 用 state_from_parent 做事
    dfs(node.left,  new_state)
    dfs(node.right, new_state)
# 适合: 路径和、深度、路径打印
```

**范式 B - 自底向上 (后序)**

```python
def dfs(node):
    if not node: return base
    l = dfs(node.left)
    r = dfs(node.right)
    return combine(node, l, r)
# 适合: 树高、直径、最大路径和、LCA、平衡
```

### 10.3 全局变量模板 (求极值类)

```python
def solve(root):
    self.ans = init_value
    def dfs(node):
        ...
        self.ans = max(self.ans, candidate)   # 边遍历边更新
        return value_for_parent
    dfs(root)
    return self.ans
```

代表题: 直径、最大路径和、最长同值路径。

### 10.4 回溯模板 (路径类)

```python
def dfs(node, path):
    path.append(node.val)
    if 到终点: res.append(path[:])
    dfs(node.left, path); dfs(node.right, path)
    path.pop()                       # 关键: 回溯
```

### 10.5 常见坑

| 坑 | 说明 |
|----|------|
| 最小深度忘记处理单边空 | 必须 `if not left: return 1+right` |
| `target - val` 不回溯 prefix sum | 前缀和题必须 `prefix[cur] -= 1` |
| 路径和允许负数 | 不要 `if val > target` 提前剪枝 |
| LCA 忘记 `root == p or root == q` | 这是递归终止条件 |
| BST 删除漏处理"无左子树"分支 | 先判 `if not root.left` |
| 中序迭代栈写法 | 必须"一路向左压到底"再弹 |
| Morris 遍历改原树 | 必须"第二次访问时断线索" |
| 层序遍历按层切 | 用 `for _ in range(len(q))` 固定每层 |

### 10.6 复杂度记忆口诀

- 99% 的二叉树 DFS: `time O(n)`, `space O(h)`, h = 树高
- 退化链 h = n; 平衡树 h = log n
- BST 操作 (search/insert/delete): `time O(h)`
- 层序 BFS: `time O(n)`, `space O(w)`, w = 最大宽度

### 10.7 思考顺序 (拿到一道树题)

1. **是 BST 吗?** 是 → 优先用有序性, 通常更优
2. **需要父节点信息吗?** 是 → 加 parent 指针, 或转无向图 (建邻接表)
3. **路径类?** 区分: 根到叶 / 任意节点向下 / 任意路径 (穿过节点)
4. **树形 DP?** 两节点子问题合成, return tuple (取/不取)
5. **能不能用前缀和 / 哈希?** 路径和类常见优化
6. **遍历顺序?** 按需求选前/中/后/层

---

## 附录: 题号速查

| 主题 | LeetCode 题号 |
|------|---------------|
| 前/中/后序遍历 | 144 / 94 / 145 |
| 层序 | 102 / 107 / 199 (右视图) |
| 最大深度 | 104 |
| 最小深度 | 111 |
| 节点数 | 222 |
| 平衡树 | 110 |
| 对称 | 101 |
| 相同树 | 100 |
| 子树 | 572 |
| 翻转 | 226 |
| 合并 | 617 |
| 直径 | 543 |
| 最长同值路径 | 687 |
| 最大路径和 | 124 |
| 路径和 III (任意路径) | 437 |
| 根到叶路径 | 257 |
| 左叶子和 | 404 |
| 数字串求和 | 129 |
| 合法 BST | 98 |
| 第 k 小 | 230 |
| BST 搜索/插入/删除 | 700 / 701 / 450 |
| 后继 | 285 |
| 恢复 BST | 99 |
| 众数 | 501 |
| 两数和 | 653 |
| 区间和 | 938 |
| 重建 (前中/中后) | 105 / 106 |
| 展开为链表 | 114 |
| 填充 next | 116 / 117 |
| LCA 普通 / BST | 236 / 235 |
| 最深叶 LCA | 1123 |
| 序列化 | 297 |
| 打家劫舍 III | 337 |
| 监控 | 968 |
| 距离 K | 863 |
| 最大宽度 | 662 |
| 找左下 | 513 |

---

## 终极心法

**90% 的树题 = 后序递归 + 返回值**。

背熟这个万能骨架:

```python
def dfs(node):
    if not node: return base_value
    left  = dfs(node.left)
    right = dfs(node.right)
    # 根据题意组合 left/right/node
    return combined_value
```

剩下 10%:
- 需要按层 → BFS + deque
- 需要路径 → 前序 + 回溯
- 需要极值 → 后序 + 全局变量
- BST → 中序 + 双指针 / 区间剪枝

每天默写一遍 §2.1, §2.7, §4.3, §7.1, §5.5 —— 这五个覆盖 60% 高频题。
