class Solution:
    def maximumAverageSubtree(self, node, parent = None): 
        if not node: 
            return 0, 0, 0
        lCnt, lSum, lAvg = self.maximumAverageSubtree(node.left, node)
        rCnt, rSum, rAvg = self.maximumAverageSubtree(node.right, node)
        ret = max((node.val + lSum + rSum) / (lCnt + rCnt + 1), lAvg, rAvg) 
        return (lCnt + rCnt + 1, lSum + rSum + node.val, ret) if parent else ret