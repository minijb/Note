---
title: Lua 循环语法
date: 2026-03-16
tags:
  - lua
  - loop
type: language
aliases:
  Lua循环
description: Lua循环语句语法
draft: false
---


### 1. for 循环

```lua
-- 正向遍历
for i = 1, #array do
    print(array[i])
end

-- 指定步长
for i = 1, 10, 2 do
    print(i)
end

-- 反向遍历
for i = #array, 1, -1 do
    print(array[i])
end
```

**优势：**

- 性能最高，执行速度最快
- 可以控制遍历方向（正向/反向）
- 可以控制步长
- 内存占用最小

**劣势：**

- 只能遍历连续的数值索引
- 无法遍历非数值键
- 遇到 nil 值会中断

### 2. ipairs


```lua

local array = {"a", "b", "c", "d"}

for index, value in ipairs(array) do
    print(index, value)
end
```


**优势：**

- 语法简洁明了
- 保证按索引顺序遍历（1, 2, 3...）
- 自动处理边界

**劣势：**

- 遇到第一个 nil 值就停止遍历
- 只能从索引 1 开始
- 无法遍历非连续索引或非数值键


### pairs

```lua
local table = {
    name = "Lua",
    version = "5.4",
    [1] = "first",
    [3] = "third",
    author = "Roberto"
}

for key, value in pairs(table) do
    print(key, value)
end
```


**优势：**

- 可以遍历所有类型的键（数值、字符串等）
- 能够遍历包含 nil 值的表
- 最通用的遍历方式

**劣势：**

- 遍历顺序不确定
- 性能比数值 for 循环稍差
- 无法保证特定的遍历顺序


### next

```lua
local table = {a = 1, b = 2, c = 3}

local key = nil
repeat
    key, value = next(table, key)
    if key then
        print(key, value)
    end
until not key
```

**优势：**

- 提供更精细的控制
- 可以手动控制遍历过程
- pairs 迭代器的底层实现

**劣势：**

- 语法复杂
- 容易出错
- 一般情况不推荐使用

### lua 中table长度获取函数并不靠谱 需要自己定义

```lua
function table_len(t)
	local len = 0
	for k,v in pairs do 
		len = len +1 
	end
end
```

`#` 标志 会自动截断
