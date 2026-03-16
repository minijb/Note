
在 Lua 中，**所有类型都是值传递**，但对于 table、function、userdata、thread 这些类型，传递的是**引用值**（即对象的引用）。

### 1. 值传递（真正的值拷贝）

```lua
-- 基本类型：nil, boolean, number, string
local a = 10
local b = a  -- 创建真正的副本
b = 20
print(a)  -- 输出: 10 (不受影响)

local s1 = "hello"
local s2 = s1  -- 创建字符串副本
s2 = "world"
print(s1)  -- 输出: hello (不受影响)
```

### 2. 引用传递（传递对象引用）


```lua
-- 复杂类型：table, function, userdata, thread
local t1 = {name = "Lua", version = 5.4}
local t2 = t1  -- 传递引用，指向同一个对象
t2.version = 5.5
print(t1.version)  -- 输出: 5.5 (受影响)

-- 函数也是引用传递
local function f1() return "original" end
local f2 = f1
f2 = function() return "modified" end
-- f1 不受影响，因为 f2 被重新赋值了新的引用
```


### 3. 函数参数传递

同理，基础类型值传递， table等复杂类型引用传递


### 4. 拷贝问题

因为table是引用，因此需要考虑拷贝问题

使用递归的方式进行拷贝，遇到基础类型直接复制， 遇到table则进行递归

```lua
-- 浅拷贝函数
function shallowCopy(original)
    local copy = {}
    for key, value in pairs(original) do
        copy[key] = value
    end
    return copy
end

-- 深拷贝函数（递归）
function deepCopy(original)
    if type(original) ~= "table" then
        return original
    end
    local copy = {}
    for key, value in pairs(original) do
        copy[key] = deepCopy(value)
    end
    return copy
end

-- 使用示例
local t1 = {a = 1, b = {x = 10, y = 20}}
local t2 = shallowCopy(t1)
local t3 = deepCopy(t1)

t2.b.x = 999  -- 会影响 t1，因为 b 是引用
t3.b.x = 888  -- 不会影响 t1，因为是深拷贝

print(t1.b.x)  -- 999
print(t3.b.x)  -- 888
```