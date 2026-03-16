---
tags:
  - algo
---

**性质1**: 

- 左子树的深度等于右子树 --- 左为满，右为完全
- 左子树的深度大于右子树 --- 左为完全，右为满

一个完全二叉树的左右子树都是完全二叉树

- 不断递归之后 --- 最后都是满二叉树 --- 只剩一个节点



**性质2**：

<span style="background:#40a9ff">可以和位运算进行结合</span>

https://leetcode.cn/problems/count-complete-tree-nodes/solutions/181466/c-san-chong-fang-fa-jie-jue-wan-quan-er-cha-shu-de/

简单来说就是  

```cpp
bool exist(TreeNode* root, int level, int k){
	int bits =  1 << (level-1);

	TreeNode* node = root;
	while(node!=nullptr && bits > 0){
		if(!(bits&k)){
			node = node -> left;
		}else{
			node = node -> right;
		}

		bits >>= 1;
	}

	return node != nullptr;
}
```

- level 为树的深度
- k 为 第 N 个节点
- root 为 根节点

![[tree.excalidraw]]