---
tags:
  - unity
  - lua
---
## 调用类

Lua 没办法直接访问c#

```c#
-- 初始化一个对象
local obj1 = CS.UnityEngine.GameObject()
local obj2 = CS.UnityEngine.GameObject("hello")

-- 使用别名
GameObject  = CS.UnityEngine.GameObject
local obj3 = GameObject("hello1")

-- 静态变量直接使用
local obj4 = GameObject.Find("hello")

-- 对象的成员变量
print(obj4.transform.position)
Debug = CS.UnityEngine.Debug.Log

-- 成员方法 必须使用 ：
Vector3 = CS.UnityEngine.Vector3
obj4.transform:Translate(Vector3.right)
Debug(obj4.transform.position)


-- 自定义类
local t = CS.Test() -- 没有命名空间
t:Speak("123")

local t1 = CS.mm.Test() -- 含有命名空间 mm
t1:Speak("567")

-- 继承了 Mono 类， 不能直接使用 new
-- 添加脚本
local obj5 = GameObject("test plugins")
obj5:AddComponent(typeof(CS.CSharpCallLua)) -- 没有泛型
```


lua 中没有 泛型， 只能使用 typeof

## **枚举** 

CS.命名空间.枚举名.枚举成员

```c#
PrimitiveType = CS.UnityEngine.PrimitiveType

local obj = GameObject.CreatePrimitie(PrimitiveType.Cube)
```

**枚举转换**

```c#
E_MyEnum = CS.E_MyEnum
E_MyEnum.__CastFrom(1)
E_MyEnum.__CastFrom("ATK")
```


## 数组，列表，字典


- 其他都很简单
- 特别的是字典，得到值 get_Item, set_Item, TryGetItem

- 数组创建 `CS.System.Array.CreateInstance(typeof(CS.System.Int32),10)`

这两个创建的是一个类，我们需要实例化
- 列表创建 `CS.System.Collections.Generic.List(CS.System.String)`
- 字典创建 `CS.System.Collections.Generic.Dictionary(CS.System.String, CS.UnityEngine.Vector3)`

```lua
local Dic_String_Vector3 = CS.System.Collections.Generic.Dictionary(CS.System.String, CS.UnityEngine.Vector3)
local dic2 = Dic_String_Vector3()

```

```lua
local obj = CS.Main()

print(obj.array.Length)

print(obj.array[0]);

for i = 0, obj.array.Length - 1 do
    print(obj.array[i])
end

-- 创建数组
-- 使用 Array 中的静态方法
local array2 = CS.System.Array.CreateInstance(typeof(CS.System.Int32),10)
print("array2.length" .. array2.Length)




-- 列表方法
obj.list:Add(0)
obj.list:Add(1)

for i = 0, obj.list.Count - 1 do
    print(obj.list[i])
end

-- 创建列表
-- 老方法
-- local list2 = CS.System.Collections.Generic["List`1[System.String]"]()
-- list2.Add(0)
-- print(list2[0])

local list_template = CS.System.Collections.Generic.List(CS.System.String)
local list3 = list_template()
list3:Add(3)
print(list3[0])


-- 字典

obj.dic:Add(1, "123")
print(obj.dic[1])

for k,v in pairs(obj.dic) do
    print(k,v)
end

-- 创建字典
local Dic_String_Vector3 = CS.System.Collections.Generic.Dictionary(CS.System.String, CS.UnityEngine.Vector3)
local dic2 = Dic_String_Vector3()

dic2:Add("123", CS.UnityEngine.Vector3.right)
for i,v in pairs(dic2) do
    print(i,v)
end

print(dic2["123"]) -- error --- nill
print(dic2:get_Item("123")) -- 通过固定方法
-- 同理 需要使用 set_Item

dic2:set_Item("123", nil)
dic2:TryGetValue("123") -- 也可以  返回两个参数
```


## 拓展方法

```c#

[LuaCallCSharp]
public static class Tools{
    public static void Move(this Func obj){
        Debug.Log(obj.name + " Tools");
    }
}



public class Func{
	public string name = "x";
	public void Speak(string str){
		xxx
	} 
	public static void Eat(){
		xxx
	}
}
```


```lua
Func = CS.Func

Func.Eat() -- 静态方法
local  obj =  Func() -- 成员方法
obj:Speak("hello")
obj:Move() -- 必须使用 LuaCallCSharp
```


- 拓展方法 需要加上特性 `[LuaCallCSharp]`
- 推荐需要使用的 C# 类 都加上 `[LuaCallCSharp]` ，提高效率


## ref out

```c#
    public int RefFun(int a, ref int b, ref int c, int d){
        b = a + d;
        c  = a- d;
        return 100;
    }
    public int OutFun(int a, out int b, out int c, int d){
        b = a ;
        c  = a;
        return 200;
    }
    public int RefOutFun(int a, out int b, ref int c, int d){
        b = a ;
        c  = a;
        return 300;
    }
```


```lua

-- 会以多返回值的形式返回lua
-- 如果结果是返回值， 第一个值就是返回值， 其他的对应 ref 
-- ref 需要传入一个 默认值 占位置
-- a return b ref c ref
local a, b, c = obj:RefFun(1, 0 , 0 ,1)
print(a,b,c)

-- 其他都一样， 但是 out 不需要占位
local a,b,c  = obj:OutFun(20,30)
-- 200 20 30

-- 混合使用 对应上面的规则
local a,b,c  = obj:RefOutFun(20,1)
print(a,b,c)
```


## 重载函数

可以直接使用 重载函数。但是 因为只有 number ，对于 多精度 支持不好

推荐使用 反射

```lua

local m1 = typeof(Class):GetMethod("Calc", {typeof(CS.System.Int32)})
local m2 = typeof(Class):GetMethod("Calc", {typeof(CS.System.Single)})

local f1 = xlua.tofunction(m1)
local f1 = xlua.tofunction(m2)
```


## 委托+事件

```lua

-- ******************** 委托
local fun = xxx

obj.del = fun
obj.del = obj.del + fun

-- 不推荐临时声明
-- 执行
obj.del()
obj.del = nil
--清空后 第一次 需要 =
obj.del = fun


-- ******************** 事件 和委托不一样
local fun2 = xxx
obj:eventAction("+", fun2)
obj:DoEvent()
obj:eventAction("-", fun2)

obj:ClearEvent() -- 只能外部清空
```


```c#
public event Action eventAction;

public void DoEvent(){
	eventAction?.Invoke();
}

public void ClearEvent(){
	eventAction = null;
}
```


## 二位数组

```lua
local array = CS.obj.array;

array:GetValue(0,0);// 得到值

-- 不能 [0][0] [0,0]
```


```c#
public int[,]  array = new int[2,3]{{xxx},{xxx}};

// 得到长度

array.GetLength(0);// 行
array.GetLength(1);// 列
```


## null nil 的比较

nil 不等于 null

```lua
rig:Equals(nil)

function IsNull(obj)
	if obj == nil or obj:Equals(nil) then
	return false
end
```

![8xYieJPXwS4CRpT.png](https://s2.loli.net/2024/07/22/8xYieJPXwS4CRpT.png)


也可以在 C# 中 写一个类

```c
[LuaCallCSharp]
public static bool Tools{
	public static bool IsNull(this Object obj){
		return obj == null;
	}
}
```



## 让系统类型和 Lua 能互相访问

[CSharpCallLua] --- 委托 和 接口
[LuaCallCSharp] ---- 拓展方法 + Lua 中用到的类


第三方库无法更改


```c#
public class ...

[CSharpCallLua]
public static List<Type> cSharpCallLuaList  = new List<Type>(){
	typeof(UnityAction<float>);
}

[LuaCallCSharp]
public static List<Type> LuaCallCSharpList  = new List<Type>(){
	typeof(GameObject);
}

// 这里 UnityAction<float> 是一个 内置的 Slider 委托，我们不能加上 [CSharpCallLua]
```


写好后 生成代码 


## 协程

```lua
--xlua提供的一个工具表
--一定是要通过require调用之后 才能用
util = require("xlua.util")
--C#中协程启动都是通过继承了Mono的类 通过里面的启动函数StartCoroutine

GameObject = CS.UnityEngine.GameObject
WaitForSeconds = CS.UnityEngine.WaitForSeconds
--在场景中新建一个空物体  然后挂一个脚本上去 脚本继承mono使用它来开启协程
local obj = GameObject("Coroutine")
local mono = obj:AddComponent(typeof(CS.CSharpCallLua))

--希望用来被开启的协程函数 
fun = function()
	local a = 1
	while true do
		--lua中 不能直接使用 C#中的 yield return 
		--就使用lua中的协程返回
		coroutine.yield(WaitForSeconds(1))
		print(a)
		a = a + 1
		if a > 10 then
			--停止协程和C#当中一样
			mono:StopCoroutine(b)
		end
	end
end
--我们不能直接将 lua函数传入到开启协程中！！！！！
--如果要把lua函数当做协程函数传入
--必须 先调用 xlua.util中的cs_generator(lua函数)
mono:StartCoroutine(util.cs_generator(fun))



```


## 调用泛型方法

![8sWi5dTGzjxf6YF.png](https://s2.loli.net/2024/07/22/8sWi5dTGzjxf6YF.png)

il2cpp 不支持  --- 引用类型才可以使用

![Kd4qm5E6VGz3CHM.png](https://s2.loli.net/2024/07/22/Kd4qm5E6VGz3CHM.png)
