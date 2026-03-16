---
tags:
  - unity
  - lua
---
## 语法

注释 `-- --[[ --]]`

nil 空类型

type 函数 得到类型

- 简单数据类型
	- number
	- string
	- boolean
	- nil
- 复杂类型
	- function
	- table
	- userdata
	- thread -- 协同程序


## 字符串

**索引从1开始**

中文字符占三个长度

- 长度 `#str`
- 跨行 `[[]]`
- 拼接 `"123".."123"`
- 格式化 `string.format("xxx%dxxx",18)`
	- %d : 数字
	- %a : 字符
	- %s : 字符串

- 转为字符串 `tostring(x)`

**公共方法**

不原地修改

- 转大写 `strint.upper(str)`
- 转小写 `string.lower(str)`
- 反转 `string.reverse(str)`
- 索引查找 `string.find(str， "Cde")`  如果有多个返回多个返回值 
- 截取 `string.sub(str,3) .sub(str, left, right)`
- 重复 `string.rep(str,2)`
- 修改 `string.gsub(str, "CD", "xx")` 返回 修改后的字符串 + 修改的次数
- 转 ASCII `string.byte("Lua",1)` 
- ASCII 转字符 `string.char(a)`


## 运算符

字符串如果是数值， 可以与 数字进行运算， 会自动转成 number

条件

`> < >= <= == ~=`

`and or not`  存在短路

没有 三目和位运算

## 条件

```lua

if xxx then
else if xxx then
else then
end

```

## 循环

```lua
while xxx do
end


--- do while
num = 0 
repeat

until num > 5 -- 满足条件跳出


for i = 2,5 do --默认加1
end

for i = 2,5,2 do --默认加1
end
```


## function

```lua
function xx()
end

a = function ()
end

-- 空参数 使用 nill

-- 返回多个参数

return a,b


-- 变长参数

function A(...)
	arg = {...}
	for i = 1,#arg do
		xxx
	end
end

-- 嵌套

function B()
	AA = function()
		print("123")
	end
	return AA
end

A_B = B()
A_B()


-- 闭包

function F(x)
	-- 改变参数的什么周期
	return function(y)
		return x+y
	end
end

ff = F(10)
ff(5) -- 15

```

**不支持重载**

## table

```c#
a = {1,2,3,4,5,nil,6}
-- 从 1 开始
#a  -- 空会被忽略 --- 6

-- 自定义索引

aa = {[0] = 1,2,3,[-1]=100, 5}
```



## 迭代器遍历

```lua
aa = {[0] = 1,2,3,[-1]=100, 5}

-- 从1 开始向后遍历， 小于等于0找不到
-- 只能找到连续的
for i,k in ipairs(a) do
	xxx
end

-- 找到所有的key
for i,k in pairs(a) do
	xxx
end


```

## 字典

```lua
aa = {["name"] = 1,["xxx"] = 2,3,[-1]=100, 5}
a["name"]
a.name

-- .不能是数字

--新增 
a['hello'] = 100
-- 删除
a.name = nil


```


## 类

```lua

Student = {
	age = 1,
	sex = true,
	getAge = function(this)
		return this.age
	end
}

function Student.Speak()
	xxx
end

-- 默认包调用这 作为第一个参数
Student:getAge ()


function Stduent:Learn()
	print(self.age)
end
```


## 表的公共参数

```lua
t1 = {1,2,3,}
t2 = {3,4,5}

-- 原地操作 t2 插入到 t1
tabel.insert(t1,t2)
-- 移除最后一个内容
table.remove(t1)

table.sort(t1) -- 升序

table.sort(t1, function(a,b)  -- 降序
	if a > b then
	return true
	end
end
)


ta = {"123","456"}
str = table.concat(tb, ",") -- 用于拼接字符串

```


## 多脚本

-  默认全局变量

```lua
local d = "Xxx"

require("脚本名") --- 执行其他脚本， 同时 local 不能再其他脚本中执行

-- 脚本可以返回一个一个表或者函数

-- 卸载
package.loaded["xxx"] -- 查看是否被加载
package.loaded["xxx"] = nil -- 卸载

-- _G 总表， 所有全局变量都存储在这
-- local 不会再 _G
```

```lua
local a = {}

return a
```


## 特殊用法

```lua
-- 多变量赋值

a,b,c = 1,2,"123"

-- 多返回值同理

print(0 and 1) -- 1

-- 伪三目

local res = (x>y) and x or y
```

只有再 nil 和 false 的时候才判断位假， 否在都位真

## 协同

```lua
fun = function()
	xxx
end

co1 = coroutine.create(fun) -- 创建 thread

co2 = coroutine.wrap(fun) -- 创建 函数

-- 运行
coroutine.resume(co1) -- 对应 create
co2() -- 对应wrap

-- 挂起

fun2 = function()
	i= 0
	while true do
		i= i+1
		coroutine.yield(i)-- 挂起
	end
end


co3 = coroutine.create(fun)
isOk, tempI = coroutine.resume(co3) -- 这里运行 知道挂起
isOk, tempI = coroutine.resume(co3)
-- 返回多个参数， 第一个 是否启动成功， 第二个， 返回对应的值

co2 = coroutine.wrap(fun)
tempI = co2() -- 这种只有一个参数 ， 及 tempI


------- 状态

corotine.Status(xxx)

- dead 
- running
- suspended 暂停
```

## 元表

对子表进行操作的时候会对元表内的东西
**特定操作默认使用 :  也就是第一个参数是自身**

```lua
-- set 元表

meta = {}
mytable = {}

setmetatable(myTable, meta)
getmetatable(xxx)
rawget(table, "index") -- 会去找自己上的不找元表上的索引
rawget(table, "index", 2) -- 忽视 __newIndex

-- 特定操作 __tostring 
-- 子表 作为 字符串 使用 的时候默认使用 原表的 __tostring 方法
meta = {
	__tostring = function()
		return xxx
	end
}

mytable = {
	name = "xxx"
}


-- 特定操作 __call
-- 子表 作为 函数 使用 的时候默认使用 原表的 __tostring 方法
meta = {
	__call  = function(a, b)
		return xxx
	end
}

-- 特定操作 运算符重载
meta = {
	__add = function(t1, t2)
		return xxx
	end
	-- __sub __mul __div __mod __pow __eq __lt __le __concat
}

-- __index __newIndex

-- __index 当子表找不到索引， 到 原表中 __index 指向的表
-- __newIndex 当子表赋值一个不存在的索引的时候 到 原表中 __newIndex 指向的表



```


## 对象

```lua
Object = {}

Object.id = 1

function Object:new()
-- 返回表
	local obj = {}
	self.__index = self
	setmetatable(obj, self)
	return obj
end

function Object:test()
	print("xxx")
end

local myObj = Object:new()
myObj:test()
myObj.id = 2
-- Object.id = 1

```


**继承**

```lua
function Object:subClass(className)
-- 再 G 中新建一个表， 然后使用 设置原表
	_G[className] = {}
	local obj = _G[className]
	setmetatable(obj, self)
	self.__index = self
	obj.base = self
end

Object:subclass("subObj");
local subObj = subObj:new()
print(subObj.id)
print(Object.id)
```

**多态**



```lua


function Object:subClass(className)
-- 再 G 中新建一个表， 然后使用 设置原表
	_G[className] = {}
	local obj = _G[className]
	setmetatable(obj, self)
	self.__index = self
	obj.base = self -- 多态的关键
end

Object:subclass("GameObject");

GameObject.posX = 0
GameObject.posY = 0

function GameObject:Move()
	self.posX = self.posX + 1
	self.posY = self.posY + 1
    print(self.posX)
    print(self.posY)
end

GameObject:subClass("Player")

function Player:Move()
-- base : 为Gameject , 我们把 Gameobjct 作为第一个参数放入
	-- self.base:Move() error
	self.base.Move(self)
end


local p1 = Player:new()
local p2 = Player:new()
p1:Move()
p2:Move()

```


## 标准库

```lua
local nowTime= os.date("*t")
for k,v in pairs(nowTime) do
	xxx
end

print(os.time(xxxxx))



-- 运算

math.abs()
math.deg(math.pi) -- 弧度转角度
math.cos
math.floor
math.ceil

math.max
math.min

math.modf(1.2) -- 拆分 整数 和小鼠

math.randomseed(os.time())
math.random(100)

math.sqrt()


package.path = package.path .. ";xxxx"
```


## 垃圾回收

```lua
collectgarbage("count") -- 返回字节数

collectgarbage("collect") -- 有定时的也可以手动


```