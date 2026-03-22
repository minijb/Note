---
title: Unity Xlua 资源加载和Csharp访问lua
date: 2026-03-16
tags:
  - knowledge
  - csharp
  - unity
type: language
aliases:
  -
description: luaenv.DoString("print('hello world')")
draft: false
---

# Unity Xlua 资源加载和Csharp访问lua

## 1. lua脚本加载

**执行lua**

```c#
luaenv.DoString("print('hello world')")
DoString("require 'byfile'")
```

**加载lua文件**

```c#
 public delegate byte[] CustomLoader(ref string filepath);
 public void LuaEnv.AddLoader(CustomLoader loader)
```

```csharp
void Start()
{
	_env = new LuaEnv();
	_env.AddLoader(CustomMyLoader);
	_env.DoString("require helloworld");
}

private byte[] CustomMyLoader(ref string fileName)
{
	string luaPath = Application.dataPath + "/LuaScripts/" + fileName + ".lua.txt";
	string strLuaContent = File.ReadAllText(luaPath);
	byte[] result = System.Text.Encoding.UTF8.GetBytes(strLuaContent);
	return result;
}

private void OnDestroy()
{
	_env.Dispose();
}
```

## 2. Csharp 访问 lua


### 2.1 **获取全局类型**

```c#
// 基础类型
luaenv.Global.Get<int>("a")
luaenv.Global.Get<string>("b")
luaenv.Global.Get<bool>("c")
```


### 2.2 **获得table类型**  -- 对应的就是c#中的类系统

1. **映射到 class 和 是 struct**

定义一个class，**有对应于table的字段的public属性**，而且有无参数构造函数即可

比如对于{f1 = 100, f2 = 100}可以定义一个包含public int f1;public int f2;的class。 这种方式下xLua会帮你new一个实例，并把对应的字段赋值过去。

- table的属性可以多于或者少于class的属性。可以嵌套其它复杂类型。 
- 要注意的是，这个过程是值拷贝，如果class比较复杂代价会比较大。
- 而且修改class的字段值不会同步到table，反过来也不会。

> 使用 GCOptimize生成可以减低开销

2. **映射到interface**

这种方式依赖于生成代码（如果没生成代码会抛InvalidCastException异常），代码生成器会生成这个interface的实例，如果get一个属性，生成代码会get对应的table字段，如果set属性也会设置对应的字段。甚至可以通过interface的方法访问lua的函数。


3. **更轻量级的by value方式：映射到Dictionary<>，List<>** 
不想定义class或者interface的话，可以考虑用这个，前提table下key和value的类型都是一致的。

4. **另外一种by ref方式：映射到LuaTable类**
这种方式好处是不需要生成代码，但也有一些问题，比如慢，比方式2要慢一个数量级，比如没有类型检查。

### 2.3 访问 function

**使用 function ， 映射到 delegate** 

```c#
private Action luaStart;
scriptScopeTable.Get("start", out luaStart);
Action e = luaenv.Global.Get<Action>("e");

// Use this for initialization
void Start()
{
	if (luaStart != null)
	{
		luaStart();
	}
}
```
参数、返回值类型支持哪些呢？都支持，各种复杂类型，out，ref修饰的，甚至可以返回另外一个delegate。

**映射到LuaFunction**
    
这种方式的优缺点刚好和第一种相反。 使用也简单，LuaFunction上有个变参的Call函数，可以传任意类型，任意个数的参数，返回值是object的数组，对应于lua的多返回值。

## 3. 建议

1. 访问lua全局数据，特别是table以及function，代价比较大，建议尽量少做，比如在初始化时把要调用的lua function获取一次（映射到delegate）后，保存下来，后续直接调用该delegate即可。table也类似。
    
2. 如果lua侧的实现的部分都以delegate和interface的方式提供，使用方可以完全和xLua解耦：由一个专门的模块负责xlua的初始化以及delegate、interface的映射，然后把这些delegate和interface设置到要用到它们的地方。


## 4. 细节


映射 interface

```c#
[CSharpCallLua]
public interface ItfD
{
	int f1 { get; set; }
	int f2 { get; set; }
	int add(int a, int b);
}

ItfD d3 = luaenv.Global.Get<ItfD>("d"); //映射到interface实例，by ref，这个要求interface加到生成列表，否则会返回null，建议用法
```


多返回值 + 复杂返回值

```c#
[CSharpCallLua]
public delegate int FDelegate(int a, string b, out DClass c);

function f(a, b)
	print('a', a, 'b', b)
	return 1, {f1 = 1024}
end


FDelegate f = luaenv.Global.Get<FDelegate>("f");
DClass d_ret;
int f_ret = f(100, "John", out d_ret);//lua的多返回值映射：从左往右映射到c#的输出参数，输出参数包括返回值，out参数，ref参数
Debug.Log("ret.d = {f1=" + d_ret.f1 + ", f2=" + d_ret.f2 + "}, ret=" + f_ret);

GetE ret_e = luaenv.Global.Get<GetE>("ret_e");//delegate可以返回更复杂的类型，甚至是另外一个delegate
e = ret_e();
e();

```

## 5. By value 和  By ref

| 特性维度     | 🔢 By Value (按值)                                                            | 🔗 By Reference (按引用)                                                      |
| -------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **传递机制** | 创建数据的**独立副本**[](http://km.ciozj.com/Detail.Aspx?AI=48855&CI=230)            | 传递原始数据的**引用（地址）**[](http://km.ciozj.com/Detail.Aspx?AI=48855&CI=230)       |
| **数据同步** | **不会**影响原始数据[](http://www.madio.net/thread-61994-1-1.html)                  | 对引用的操作会**直接修改**原始数据[](http://www.madio.net/thread-61994-1-1.html)          |
| **性能表现** | 通常**较轻量**[](https://blog.csdn.net/weixin_34034261/article/details/93582458) | 通常**更慢**[](https://blog.csdn.net/weixin_34034261/article/details/93582458) |
| **类型安全** | 依赖 C# 泛型，**类型安全**                                                           | 使用 `object[]`，**类型不安全**                                                    |
| **适用场景** | 简单的、只读的、不关心 Lua 中原数据变化的数据                                                   | 需要在 C# 和 Lua 间**同步数据变更**的场                                                 |

在 xLua 中，典型的 By Value 方式包括：

- **映射到 `Dictionary<string, object>` 或 `List<object>`**：适用于 Lua 中的 table。
- **映射到 `LuaFunction`**：适用于 Lua 中的函数，通过 `Call` 方法调用，返回值是 `object[]` 数组。
- class

在 xLua 中，典型的 By Reference 方式包括：

- **映射到 `LuaTable` 类**：可以直接访问和修改 Lua 中原始 table 的字段和方法。
- **映射到 Delegate（委托）**：适用于 Lua 中的函数。这种方式性能更好，而且是类型安全的。


//映射到有对应字段的class，by value
//映射到`Dictionary<string, double>`，by value
//映射到`List<double>`，by value
//映射到interface实例，by ref，这个要求interface加到生成列表，否则会返回null，建议用法
//映射到LuaTable，by ref
//映射到一个delgate，要求delegate加到生成列表，否则返回null，建议用法