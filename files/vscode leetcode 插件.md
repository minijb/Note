---
tags:
  - vscode
---

## 区域测试

```c++
// @lcpr case=start
// "PAYPALISHIRINGGGG"\n3\n
// @lcpr case=end
```


### diy 参数

用于调试不同类型的参数和函数

```c++
// @lcpr-div-debug-arg-start
// funName= alternateDigitSum
// paramTypes= ["number"]
// @lcpr-div-debug-arg-end
```

- funName : 函数名称
- paramTypes ： 参数类型
	- 可填入内容为以下字符串
	    - "number"
	        - 类型说明:数字
	    - "number[]"
	        - 类型说明:数字数组
	    - "number[][]"
	        - 类型说明:数字二维数组
	    - "string"
	        - 类型说明:字符串
	    - "string[]"
	        - 类型说明:字符串数组
	    - "string[][]"
	        - 类型说明:字符串二维数组
	    - "ListNode"
	        - 类型说明:链表
	    - "ListNode[]"
	        - 类型说明:链表数组
	    - "character"
	        - 类型说明:字节
	    - "character[]"
	        - 类型说明:字节数组
	    - "character[][]"
	        - 类型说明:字节二维数组
	    - "NestedInteger[]"
	        - 类型说明:数组
	    - "MountainArray"
	        - 类型说明:数组
	    - "TreeNode"
	        - 类型说明:树节点
	    - 