

## 1. @alias 类型别敏

用于创建自定义类型，枚举类型或简化复杂类型表达式

```lua
-- 简单别名
---@alias <别名> <类型表达式>

-- 枚举别名
---@alias <别名>
---| '<值1>' [# 描述1]
---| '<值2>' [# 描述2]
---| ...

-- 泛型别名
---@alias <别名><<泛型参数列表>> <类型表达式>
```


例子:

[github example](https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/docs/emmylua_doc/annotations_CN/alias.md)

## 2. @class 类定义

```lua
-- 基础类定义
---@class <类名>[: <父类1>[, <父类2>...]]

-- 精确类定义（禁止动态添加字段）
---@class (exact) <类名>[: <父类>...]

-- 部分类定义（允许扩展现有类）
---@class (partial) <类名>
```


[git example](https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/docs/emmylua_doc/annotations_CN/class.md)


## 3. @field 字段定义

为类定义字段，支持访问控制、可选性和索引签名。

```lua
-- 具名字段
---@field [<访问控制>] <字段名>[?] <类型> [描述]

-- 索引签名字段
---@field [<访问控制>] [<键类型>] <值类型> [描述]
```

- `public` - 公共字段（默认）
- `private` - 私有字段（仅类内部访问）
- `protected` - 受保护字段（类及子类可访问）
- `package` - 包内字段（同包内可访问）

可选字段（使用 ? 标记）

```lua
---@class UserProfile
---@field avatar? string 头像URL（可选）
---@field bio? string 个人简介（可选）
---@field phone? string 电话号码（可选）
```


任意字符串键位
```lua
---@class Configuration
---@field host string 主机地址
---@field port number 端口号
---@field [string] any 其他配置项（任意字符串键）
```

## 4. @type - 类型声明

```lua
-- 基础类型声明
---@type string
local userName = "张三"

---@type number
local userAge = 25

---@type boolean
local isActive = true

-- 联合类型
---@type string | number
local mixedValue = "可以是字符串或数字"

-- 可选类型
---@type string?
local optionalString = nil  -- 等价于 string | nil

-- 数组类型
---@type string[]
local nameList = {"张三", "李四", "王五"}

---@type number[]
local scores = {95, 87, 92, 88}

-- 复杂数组类型
---@type (string | number)[]
local mixedArray = {"张三", 25, "李四", 30}

-- 字典类型
---@type table<string, number>
local ageMap = {
    ["张三"] = 25,
    ["李四"] = 30,
    ["王五"] = 28
}

---@type table<number, string>
local idToName = {
    [1001] = "张三",
    [1002] = "李四",
    [1003] = "王五"
}

-- 元组类型
---@type [string, number, boolean]
local userInfo = {"张三", 25, true}

-- 表字面量类型
---@type {name: string, age: number, email: string}
local user = {
    name = "张三",
    age = 25,
    email = "zhangsan@example.com"
}

-- 嵌套表结构
---@type {user: {id: number, name: string}, permissions: string[]}
local userWithPermissions = {
    user = {id = 1001, name = "张三"},
    permissions = {"read", "write", "delete"}
}

-- 函数类型
---@type fun(x: number, y: number): number
local addFunction = function(x, y)
    return x + y
end

---@type fun(name: string, age: number): {name: string, age: number}
local createUser = function(name, age)
    return {name = name, age = age}
end

-- 异步函数类型
---@type async fun(url: string): string
local fetchData = async function(url)
    -- 异步获取数据
    return await httpGet(url)
end

-- 类类型
---@class User
---@field id number
---@field name string

---@type User
local currentUser = {
    id = 1001,
    name = "张三"
}

-- 类数组
---@type User[]
local userList = {
    {id = 1001, name = "张三"},
    {id = 1002, name = "李四"}
}

-- 泛型类型
---@class Container<T>
---@field items T[]

---@type Container<string>
local stringContainer = {
    items = {"hello", "world"}
}

---@type Container<number>
local numberContainer = {
    items = {1, 2, 3, 4, 5}
}

-- 复杂泛型组合
---@type table<string, Container<User>>
local userContainerMap = {
    ["admins"] = {items = {{id = 1, name = "管理员"}}},
    ["users"] = {items = {{id = 2, name = "普通用户"}}}
}

-- 枚举类型
---@alias Status 'active' | 'inactive' | 'pending'

---@type Status
local currentStatus = 'active'

-- 回调函数类型
---@type fun(error: string?, result: any?): nil
local callback = function(error, result)
    if error then
        print("错误:", error)
    else
        print("结果:", result)
    end
end

-- 事件处理器类型
---@type table<string, fun(...)>
local eventHandlers = {
    ["click"] = function(x, y)
        print("点击位置:", x, y)
    end,
    ["keypress"] = function(key)
        print("按键:", key)
    end
}

-- Promise类型
---@class Promise<T>
---@field then fun(self: Promise<T>, onResolve: fun(value: T), onReject?: fun(error: any))

---@type Promise<string>
local dataPromise = fetchUserDataAsync(1001)

-- 条件类型使用
---@type boolean
local isLoggedIn = checkLoginStatus()

---@type User | nil
local user = isLoggedIn and getCurrentUser() or nil

-- 索引签名类型
---@type {[string]: any}
local dynamicObject = {
    someKey = "someValue",
    anotherKey = 123,
    yetAnother = true
}

-- 只读类型（约定）
---@type {readonly name: string, readonly id: number}
local readonlyUser = {name = "张三", id = 1001}

-- 使用示例和类型检查
if user then
    -- 在这个块中，user的类型是 User（非nil）
    print("用户名:", user.name)
    print("用户ID:", user.id)
end

-- 类型断言使用
---@type string
local stringValue = tostring(mixedValue)  -- 确保转换为字符串

-- 循环中的类型使用
---@type string
for _, name in ipairs(nameList) do
    print("姓名:", name)  -- name被推断为string类型
end
```

## 5.  @enum 枚举类型

```lua
-- 值枚举（使用表的值）
---@enum <枚举名>

-- 键枚举（使用表的键）
---@enum (key) <枚举名>
```



```lua
-- 基础值枚举
---@enum HTTPStatus
local HTTPStatus = {
    OK = 200,
    NOT_FOUND = 404,
    INTERNAL_ERROR = 500,
    BAD_REQUEST = 400,
    UNAUTHORIZED = 401
}

-- 字符串值枚举
---@enum LogLevel
local LogLevel = {
    DEBUG = "debug",
    INFO = "info",
    WARN = "warn",
    ERROR = "error",
    FATAL = "fatal"
}

-- 键枚举（使用表的键作为枚举值）
---@enum (key) Permission
local Permission = {
    READ = true,
    WRITE = true,
    DELETE = true,
    ADMIN = true
}

-- 混合类型枚举
---@enum TaskStatus
local TaskStatus = {
    PENDING = 0,
    RUNNING = "running",
    COMPLETED = true,
    FAILED = false
}

-- 使用枚举的函数
---@param status HTTPStatus HTTP状态码
---@return string 状态描述
function getStatusMessage(status)
    if status == HTTPStatus.OK then
        return "请求成功"
    elseif status == HTTPStatus.NOT_FOUND then
        return "资源未找到"
    elseif status == HTTPStatus.INTERNAL_ERROR then
        return "服务器内部错误"
    else
        return "未知状态"
    end
end

---@param level LogLevel 日志级别
---@param message string 日志消息
function writeLog(level, message)
    local timestamp = os.date("%Y-%m-%d %H:%M:%S")
    print(string.format("[%s] %s: %s", timestamp, level, message))
end

---@param user table 用户对象
---@param permission Permission 权限类型
---@return boolean 是否有权限
function hasPermission(user, permission)
    return user.permissions and user.permissions[permission] == true
end

-- 复杂枚举示例
---@enum DatabaseAction
local DatabaseAction = {
    -- CRUD操作
    CREATE = "create",
    READ = "read",
    UPDATE = "update",
    DELETE = "delete",

    -- 批量操作
    BATCH_INSERT = "batch_insert",
    BATCH_UPDATE = "batch_update",
    BATCH_DELETE = "batch_delete",

    -- 查询操作
    QUERY = "query",
    COUNT = "count",
    EXISTS = "exists"
}

---@enum EventType
local EventType = {
    -- 用户事件
    USER_LOGIN = "user.login",
    USER_LOGOUT = "user.logout",
    USER_REGISTER = "user.register",

    -- 系统事件
    SYSTEM_START = "system.start",
    SYSTEM_STOP = "system.stop",
    SYSTEM_ERROR = "system.error",

    -- 数据事件
    DATA_CHANGED = "data.changed",
    DATA_DELETED = "data.deleted"
}

-- 带有方法的枚举
---@enum Color
local Color = {
    RED = "#FF0000",
    GREEN = "#00FF00",
    BLUE = "#0000FF",
    BLACK = "#000000",
    WHITE = "#FFFFFF"
}

-- 为枚举添加方法
---@param color Color 颜色值
---@return number 红色分量
function Color.getRed(color)
    return tonumber(color:sub(2, 3), 16) or 0
end

---@param color Color 颜色值
---@return number 绿色分量
function Color.getGreen(color)
    return tonumber(color:sub(4, 5), 16) or 0
end

---@param color Color 颜色值
---@return number 蓝色分量
function Color.getBlue(color)
    return tonumber(color:sub(6, 7), 16) or 0
end

-- 数值枚举
---@enum Priority
local Priority = {
    LOW = 1,
    NORMAL = 2,
    HIGH = 3,
    URGENT = 4,
    CRITICAL = 5
}

---@param p1 Priority 优先级1
---@param p2 Priority 优先级2
---@return Priority 更高的优先级
function getHigherPriority(p1, p2)
    return p1 > p2 and p1 or p2
end

-- 位标志枚举
---@enum FileMode
local FileMode = {
    READ = 1,      -- 0001
    WRITE = 2,     -- 0010
    EXECUTE = 4,   -- 0100
    DELETE = 8     -- 1000
}

---@param mode1 FileMode 文件模式1
---@param mode2 FileMode 文件模式2
---@return FileMode 组合模式
function combineFileMode(mode1, mode2)
    return mode1 | mode2
end

---@param mode FileMode 文件模式
---@param permission FileMode 要检查的权限
---@return boolean 是否包含该权限
function hasFilePermission(mode, permission)
    return (mode & permission) ~= 0
end

-- 使用示例
print(getStatusMessage(HTTPStatus.OK))           -- "请求成功"
writeLog(LogLevel.ERROR, "系统错误")              -- 写入错误日志

-- 权限检查
local user = {
    permissions = {
        [Permission.READ] = true,
        [Permission.WRITE] = true
    }
}
print(hasPermission(user, Permission.READ))      -- true
print(hasPermission(user, Permission.DELETE))    -- false

-- 颜色操作
local red = Color.getRed(Color.RED)               -- 255
local green = Color.getGreen(Color.GREEN)         -- 255

-- 优先级比较
local highestPriority = getHigherPriority(Priority.LOW, Priority.HIGH)  -- Priority.HIGH

-- 文件权限组合
local readWrite = combineFileMode(FileMode.READ, FileMode.WRITE)         -- 3
print(hasFilePermission(readWrite, FileMode.READ))                      -- true
print(hasFilePermission(readWrite, FileMode.EXECUTE))                   -- false
```

## 6. @generic 泛型定义

```lua
---@generic <泛型名1>[: <约束类型1>] [, <泛型名2>[: <约束类型2>]...]
```


例子

```lua
-- 基础泛型函数
---@generic T
---@param value T 输入值
---@return T 相同类型的输出值
function identity(value)
    return value
end

-- 使用示例
local str = identity("hello")      -- str的类型是string
local num = identity(42)           -- num的类型是number

-- 多泛型参数
---@generic K, V
---@param map table<K, V> 映射表
---@return K[] 所有键的数组
function getKeys(map)
    local keys = {}
    for k in pairs(map) do
        table.insert(keys, k)
    end
    return keys
end

---@generic K, V
---@param map table<K, V> 映射表
---@return V[] 所有值的数组
function getValues(map)
    local values = {}
    for _, v in pairs(map) do
        table.insert(values, v)
    end
    return values
end

-- 泛型约束
---@generic T : table
---@param obj T 表对象
---@return T 深拷贝的对象
function deepClone(obj)
    if type(obj) ~= "table" then
        return obj
    end

    local copy = {}
    for k, v in pairs(obj) do
        copy[k] = deepClone(v)
    end
    return copy
end

-- 数组操作泛型
---@generic T
---@param array T[] 输入数组
---@param predicate fun(item: T): boolean 过滤条件
---@return T[] 过滤后的数组
function filter(array, predicate)
    local result = {}
    for _, item in ipairs(array) do
        if predicate(item) then
            table.insert(result, item)
        end
    end
    return result
end

---@generic T, R
---@param array T[] 输入数组
---@param mapper fun(item: T): R 映射函数
---@return R[] 映射后的数组
function map(array, mapper)
    local result = {}
    for _, item in ipairs(array) do
        table.insert(result, mapper(item))
    end
    return result
end

---@generic T, R
---@param array T[] 输入数组
---@param reducer fun(acc: R, item: T): R 归约函数
---@param initialValue R 初始值
---@return R 归约结果
function reduce(array, reducer, initialValue)
    local accumulator = initialValue
    for _, item in ipairs(array) do
        accumulator = reducer(accumulator, item)
    end
    return accumulator
end

-- 泛型类定义
---@class List<T>
---@field private items T[] 存储的项目
local List = {}

---@generic T
---@return List<T>
function List.new()
    return setmetatable({items = {}}, {__index = List})
end

---@param item T
function List:add(item)
    table.insert(self.items, item)
end

---@param index number
---@return T?
function List:get(index)
    return self.items[index]
end

---@return number
function List:size()
    return #self.items
end

---@generic R
---@param mapper fun(item: T): R
---@return List<R>
function List:map(mapper)
    local result = List.new()
    for _, item in ipairs(self.items) do
        result:add(mapper(item))
    end
    return result
end

-- 泛型工厂函数
---@generic T
---@param constructor fun(): T 构造函数
---@return fun(): T 工厂函数
function createFactory(constructor)
    return function()
        return constructor()
    end
end

-- Promise类型泛型
---@class Promise<T>
---@field private value T?
---@field private state 'pending' | 'resolved' | 'rejected'
local Promise = {}

---@generic T
---@param executor fun(resolve: fun(value: T), reject: fun(reason: any))
---@return Promise<T>
function Promise.new(executor)
    local promise = setmetatable({
        value = nil,
        state = 'pending'
    }, {__index = Promise})

    local function resolve(value)
        if promise.state == 'pending' then
            promise.value = value
            promise.state = 'resolved'
        end
    end

    local function reject(reason)
        if promise.state == 'pending' then
            promise.value = reason
            promise.state = 'rejected'
        end
    end

    executor(resolve, reject)
    return promise
end

---@generic R
---@param onResolve fun(value: T): R
---@return Promise<R>
function Promise:then(onResolve)
    if self.state == 'resolved' then
        return Promise.new(function(resolve)
            resolve(onResolve(self.value))
        end)
    end
    -- 简化实现，实际应该处理异步情况
    return Promise.new(function() end)
end

-- 高阶函数泛型
---@generic T
---@param fn fun(...): T 要记忆化的函数
---@return fun(...): T 记忆化的函数
function memoize(fn)
    local cache = {}
    return function(...)
        local key = table.concat({...}, ",")
        if cache[key] == nil then
            cache[key] = fn(...)
        end
        return cache[key]
    end
end

-- 类型安全的泛型容器
---@class Container<T>
---@field private data T[]
---@field private maxSize number
local Container = {}

---@generic T
---@param maxSize number
---@return Container<T>
function Container.new(maxSize)
    return setmetatable({
        data = {},
        maxSize = maxSize or math.huge
    }, {__index = Container})
end

---@param item T
---@return boolean 是否添加成功
function Container:push(item)
    if #self.data < self.maxSize then
        table.insert(self.data, item)
        return true
    end
    return false
end

---@return T? 弹出的项目
function Container:pop()
    return table.remove(self.data)
end

---@return T? 首个项目
function Container:peek()
    return self.data[#self.data]
end

-- 使用示例
local numbers = {1, 2, 3, 4, 5}
local strings = {"a", "b", "c"}

-- 过滤偶数
local evenNumbers = filter(numbers, function(n) return n % 2 == 0 end)  -- {2, 4}

-- 字符串转换为大写
local upperStrings = map(strings, function(s) return s:upper() end)      -- {"A", "B", "C"}

-- 计算数组总和
local sum = reduce(numbers, function(acc, n) return acc + n end, 0)      -- 15

-- 创建字符串列表
---@type List<string>
local stringList = List.new()
stringList:add("hello")
stringList:add("world")

-- 映射为长度列表
local lengthList = stringList:map(function(s) return #s end)             -- List<number>

-- 创建用户容器
---@type Container<{name: string, age: number}>
local userContainer = Container.new(100)
userContainer:push({name = "张三", age = 25})
userContainer:push({name = "李四", age = 30})

local user = userContainer:pop()  -- {name: "李四", age: 30}
```