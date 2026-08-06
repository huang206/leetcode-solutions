# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            res.append(node.val)  # O(1) 均摊，不拷贝
            dfs(node.right)

        dfs(root)
        return res


# time complexity: O(n)
# space complexity: O(logn)
