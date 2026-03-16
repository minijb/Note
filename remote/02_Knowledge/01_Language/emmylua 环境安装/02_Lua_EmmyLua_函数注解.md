

## 1. @param 参数定义

```lua
---@param <参数名>[?] <类型表达式> [描述]
```

- `?` - 可选参数标记
- `...` - 可变参数标记
- 支持联合类型
- 支持泛型参数

[github example](https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/docs/emmylua_doc/annotations_CN/param.md)


## 2. @return 返回值定义

```lua
-- 基础语法
---@return <类型> [变量名] [描述]

-- 带注释的语法
---@return <类型> [变量名] # 描述

-- 多返回值
---@return <类型1> [名称1] [描述1]
---@return <类型2> [名称2] [描述2]
```

[github example](https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/docs/emmylua_doc/annotations_CN/return.md)

## 3. @overload 重载

```lua
---@overload fun(<参数列表>): <返回值>
```


[github example](https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/docs/emmylua_doc/annotations_CN/overload.md)


## 4. @async 异步函数标记

```lua
---@async
```


[github example](https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/docs/emmylua_doc/annotations_CN/async.md)

## 5. @nodiscard 

返回值不可以被忽略

```lua
---@nodiscard
```

[github example](https://github.com/EmmyLuaLs/emmylua-analyzer-rust/blob/main/docs/emmylua_doc/annotations_CN/nodiscard.md)

