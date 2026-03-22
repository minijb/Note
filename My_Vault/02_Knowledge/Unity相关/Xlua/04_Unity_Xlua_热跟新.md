---
title: Unity Xlua 热跟新
date: 2026-03-16
tags:
  - knowledge
  - unity
type: language
aliases:
  -
description: 添加 `HOTFIX_ENABLE` 宏，（在 Unity3D 的 "File->Build Setting->Scripting Define Symbols" 下添加）。编辑器、各手机平台这个宏要...
draft: false
---

# Unity Xlua 热跟新

1. 打开该特性
    
    添加 `HOTFIX_ENABLE` 宏，（在 Unity3D 的 "File->Build Setting->Scripting Define Symbols" 下添加）。编辑器、各手机平台这个宏要分别设置！如果是自动化打包，要注意在代码里头用 API 设置的宏是不生效的，需要在编辑器设置。
    
    （建议平时开发业务代码不打开 `HOTFIX_ENABLE`，只在构建手机版本或者要在编译器下开发补丁时打开 `HOTFIX_ENABLE`）
    
2. 在菜单中找到 "XLua/Generate Code" 按钮并单击。
    
3. 注入，构建手机包这个步骤会在构建时自动进行，编辑器下开发补丁需要手动执行 "XLua/Hotfix Inject In Editor" 菜单。打印 “hotfix inject finish!” 或者 “had injected!” 才算成功，否则会打印错误信息。
    
    如果已经打印了 “hotfix inject finish!” 或者 “had injected!”，执行 `xlua.hotfix` 仍然报类似 “xlua.access, no field __Hitfix0_Update” 的错误，要么是该类没配置到 Hotfix 列表，要么是注入成功后，又触发了编译，覆盖了注入结果。


`xlua.hotfix(class, [method_name], fix)`

- 描述 ： 注入lua补丁
- class ： C#类，两种表示方法，CS.Namespace.TypeName或者字符串方式"Namespace.TypeName"，字符串格式和C#的Type.GetType要求一致，如果是内嵌类型（Nested Type）是非Public类型的话，只能用字符串方式表示"Namespace.TypeName+NestedTypeName"；
- method_name ： 方法名，可选；
- fix ： 如果传了method_name，fix将会是一个function，否则通过table提供一组函数。table的组织按key是method_name，value是function的方式。

`base(csobj)`

- 描述 ： 子类override函数通过base调用父类实现。
- csobj ： 对象
- 返回值 ： 新对象，可以通过该对象base上的方法

例子（位于HotfixTest2.cs）：

```lua
xlua.hotfix(CS.BaseTest, 'Foo', function(self, p)
    print('BaseTest', p)
    base(self):Foo(p)
end)
```

`util.hotfix_ex(class, method_name, fix)`

- 描述 ： xlua.hotfix的增强版本，可以在fix函数里头执行原来的函数，缺点是fix的执行会略慢。
- method_name ： 方法名；
- fix ： 用来替换C#方法的lua function。

## 标识热更新的类

和其它配置一样，有两种方式

方式一：直接在类里头打Hotfix标签（不建议，示例只是为了方便演示采取这种方式）；

！！注意，方式一在高版本 Unity 不支持

方式二：在一个静态类的静态字段或者属性里头配置一个列表。属性可以用于实现的比较复杂的配置，比如根据命名空间做白名单。

！！注意，高版本 Unity 需要把配置文件放 Editor 目录下

```cs
//如果涉及到Assembly-CSharp.dll之外的其它dll，如下代码需要放到Editor目录
public static class HotfixCfg
{
    [Hotfix]
    public static List<Type> by_field = new List<Type>()
    {
        typeof(HotFixSubClass),
        typeof(GenericClass<>),
    };

    [Hotfix]
    public static List<Type> by_property
    {
        get
        {
            return (from type in Assembly.Load("Assembly-CSharp").GetTypes()
                    where type.Namespace == "XXXX"
                    select type).ToList();
        }
    }
}
```


## Hotfix Flag

定制化生成代码

https://github.com/Tencent/xLua/blob/master/Assets/XLua/Doc/hotfix.md#hotfix-flag

## 建议

- 对所有较大可能变动的类型加上 `Hotfix` 标识；
- 建议用反射找出所有函数参数、字段、属性、事件涉及的 delegate 类型，标注 `CSharpCallLua`；
- 业务代码、引擎 API、系统 API，需要在 Lua 补丁里头高性能访问的类型，加上 `LuaCallCSharp`；
- 引擎 API、系统 API 可能被代码剪裁调（C#无引用的地方都会被剪裁），如果觉得可能会新增 C# 代码之外的 API 调用，这些 API 所在的类型要么加 `LuaCallCSharp`，要么加 `ReflectionUse`；

## 打补丁

- **函数**

`method_name` 传函数名，支持重载，不同重载都是转发到同一个 lua 函数。

比如：

```cs
// 要fix的C#类
[Hotfix]
public class HotfixCalc
{
    public int Add(int a, int b)
    {
        return a - b;
    }

    public Vector3 Add(Vector3 a, Vector3 b)
    {
        return a - b;
    }
｝
```

```lua
xlua.hotfix(CS.HotfixCalc, 'Add', function(self, a, b)
    return a + b
end)
```


静态函数和成员函数的区别是，成员函数会加一个 self 参数，这个 self 在 Stateless 方式下是 C# 对象本身（对应 C# 的 this）

普通参数对于 lua 的参数，ref 参数对应 lua 的一个参数和一个返回值，out参数对于lua的一个返回值。

泛化函数的打补丁规则和普通函数一样。


- **构造函数**

构造函数对应的 `method_name` 是 ".ctor"。
和普通函数不一样的是，构造函数的热补丁并不是替换，而是执行原有逻辑后调用lua。


- **属性**
对于名为 “AProp” 的属性，会对应一个 getter，`method_name` 等于 `get_AProp`，setter 的 `method_name` 等于 `set_AProp`。

- **`[]`操作符**
赋值对应 `set_Item`，取值对应 `get_Item`。第一个参数是 self，赋值后面跟 key，value，取值只有 key 参数，返回值是取出的值。

- **其它操作符**

C#的操作符都有一套内部表示，比如 `+` 号的操作符函数名是 `op_Addition`（其它操作符的内部表示可以去请参照相关资料），覆盖这函数就覆盖了 C# 的 `+` 号操作符。


- **事件**

比如对于事件“AEvent”，+= 操作符是 add_AEvent，-=对应的是 remove_AEvent。这两个函数均是第一个参数是self，第二个参数是操作符后面跟的delegate。

通过 `xlua.private_accessible`（版本号大于2.1.11不需要调用 `xlua.private_accessible`）来直接访问事件对应的私有 delegate 的直接访问后，可以通过对象的"&事件名"字段直接触发事件，例如 `self['&MyEvent']()`，其中MyEvent是事件名。

- **析构函数**

method_name 是 "Finalize"，传一个 self 参数。

和普通函数不一样的是，析构函数的热补丁并不是替换，而是开头调用 lua 函数后继续原有逻辑。

- **泛化类型**

其它规则一致，需要说明的是，每个泛化类型实例化后都是一个独立的类型，只能针对实例化后的类型分别打补丁。比如：

```cs
public class GenericClass<T>
{
｝
```

你只能对 `GenericClass<double>`，`GenericClass<int>` 这些类，而不是对 `GenericClass` 打补丁。

对 `GenericClass<double>` 打补丁的实例如下：

```cs
luaenv.DoString(@"
    xlua.hotfix(CS.GenericClass(CS.System.Double), {
        ['.ctor'] = function(obj, a)
            print('GenericClass<double>', obj, a)
        end;
        Func1 = function(obj)
            print('GenericClass<double>.Func1', obj)
        end;
        Func2 = function(obj)
            print('GenericClass<double>.Func2', obj)
            return 1314
        end
    })
");
```

- **Unity协程**

通过 `util.cs_generator` 可以用一个 function 模拟一个 `IEnumerator`，在里头用 `coroutine.yield`，就类似 C# 里头的 yield return。比如下面的 C# 代码和对应的 hotfix 代码是等同效果的

```cs
[XLua.Hotfix]
public class HotFixSubClass : MonoBehaviour {
    IEnumerator Start()
    {
        while (true)
        {
            yield return new WaitForSeconds(3);
            Debug.Log("Wait for 3 seconds");
        }
    }
}
```

```cs
luaenv.DoString(@"
    local util = require 'xlua.util'
    xlua.hotfix(CS.HotFixSubClass,{
        Start = function(self)
            return util.cs_generator(function()
                while true do
                    coroutine.yield(CS.UnityEngine.WaitForSeconds(3))
                    print('Wait for 3 seconds')
                end
            end)
        end;
    })
");
```

- **整个类**

如果要替换整个类，不需要一次次的调用 `xlua.hotfix` 去替换，可以整个一次完成。只要给一个 table，按 `method_name = function` 组织即可

```lua
xlua.hotfix(CS.StatefullTest, {
    ['.ctor'] = function(csobj)
        return util.state(csobj, {evt = {}, start = 0, prop = 0})
    end;
    set_AProp = function(self, v)
        print('set_AProp', v)
        self.prop = v
    end;
    get_AProp = function(self)
        return self.prop
    end;
    get_Item = function(self, k)
        print('get_Item', k)
        return 1024
    end;
    set_Item = function(self, k, v)
        print('set_Item', k, v)
    end;
    add_AEvent = function(self, cb)
        print('add_AEvent', cb)
        table.insert(self.evt, cb)
    end;
    remove_AEvent = function(self, cb)
       print('remove_AEvent', cb)
       for i, v in ipairs(self.evt) do
           if v == cb then
               table.remove(self.evt, i)
               break
           end
       end
    end;
    Start = function(self)
        print('Start')
        for _, cb in ipairs(self.evt) do
            cb(self.start, 2)
        end
        self.start = self.start + 1
    end;
    StaticFunc = function(a, b, c)
       print(a, b, c)
    end;
    GenericTest = function(self, a)
       print(self, a)
    end;
    Finalize = function(self)
       print('Finalize', self)
    end
})
```