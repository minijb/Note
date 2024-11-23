---
tags:
  - 面试
  - lua
---
### lua中的table + pairs/ipairs

lua的table其实由**数组段**和**hash**两部分组成

所以当ipairs遍历table时，从键值对索引值`[1]`开始连续递增，当键值对索引值`[ ]`断开或遇到nil时==退出，所以上面的例子中ipairs遍历出的结果是2，4，3。

```lua
local t = {[1]=1,2,[3]=3,4,[5]=5,[6]=6}

-- 哈希 : {[1]=1,[3]=3,[5]=5.[6]=6}
-- 数组 : {2,4}

print('ipairs')
for index, value in ipairs(t) do
    print( tostring(index) .. " " .. tostring(value))
end
--- 2, 4, 3


print('pairs')
for key, value in pairs(t) do
    print(value)
end


```

而pairs遍历时，会遍历表中的所有键值对，先按照索引值输出所有数组后，在输出其它键值对，且元素是根据[哈希算法](https://so.csdn.net/so/search?q=%E5%93%88%E5%B8%8C%E7%AE%97%E6%B3%95&spm=1001.2101.3001.7020)来排序的，得到的不一定是连续的，所以pairs遍历出的结果是2，4，3，6，5。


### metatable / 元方法

允许该表table行为，行为关联元方法，类似一种“操作指南”，包含各种操作行为的解决方案

```lua
A = {}
B = {}
setmetatable(
    A,
    {
        __index = B, --索引查询
        __newindex = B, --索引更新
        __add = B, --加法
        __sub = B, --减
        __mul = B, --乘
        __div = B, --除
        __mod = B, --取模
        __pow = B, --乘幂
        __unm = B, --取反
        __concat = B, --连接
        __len = B, --长度
        __eq = B, --相等
        __lt = B, --小于
        __le = B, --小于等于
        __call = B, --执行方法调用
        __tostring = B, --字符串输出
        __metatable = B	 --保护元表
    }
)
```


最为父对象的时候 需要 `__index`

```lua
father = {  
    prop1=2  
}  
father.__index = father -- 把father的__index方法指向它本身
son = {  
    prop2=1  
}  
setmetatable(son, father) --把son的metatable设置为father  
print (son.prop1)
--输出结果为2

```

Lua并不是直接在fahter中找到名为prop1的成员，而是先调用father的__index方法），如果__index方法为nil，则直接返回nil。如果__index指向了一张表（上面的例子中father的__index指向了自己本身），那么就会到__index方法所指向的这个表中去查找名为prop1的成员。


## 面对对象

```lua
--类：属性，构造函数，成员，属性等等
--类的声明，属性，初始值
class = {x = 0, y = 0}
--设置元表的索引，要模拟类，这一步最重要
class.__index = class --表的元表索引是自己
--构造方法，习惯性命名new（）
function class:new(x, y)
    local t = {} --初始化t，如果没有这一句，会导致类所建立的对象一旦发生改变，其它对象都会改变
    setmetatable(t, class) --设置t的元表为class ， 把class设为t的原型
    t.x = x --属性值初始化
    t.y = y
    return t --返回自身
end
--这里定义类的其它方法，self标识是非常重要的核心点，冒号：隐藏了self参数
function class:test()
    print(self.x, self.y)
end
function class:plus()
    self.x = self.x + 1
    self.y = self.y + 1
end
```


## C#与Lua的交互细节

### **gameObj.transform.position = pos 十分耗费性能**

**取的过程**

1. GameObjectWrap.get_tranform 中进行查找
	1. 把 lua 中 gameobject 变为 C# 中可以辨认的 ID
	2. 用这个 id 通过 ObjectTranslator.TryGetValue 获得 c# 中的 gameobject 对象
2. 随后 ObjectTranslator 会给 transform 分配一个id，(在lua中用来代表 tranform) --- 用于之后的查找
3. luaDLL 在 lua 中分配一个 userdata， 把id放进去，--- 用于即将返回给lua 的transform
	1. 附加上 metatable， 此时才可以使用 .position
	2. 返回transform

**简单一句话** ： `.` 取 Object ：

1. 在 ObjectTranslator 中 将 **lua** 中 gameobjec 转化为 C# 看得懂的 **id**
2. 通过 id 得到 c# 中的 transform
3. 在 **userData** 中 存入 **id**
4. 将 **userData** 中 附上 **metatable** ，才可以 使用 transform.**position**

**之后就是 position 的赋值问题** ：  new Vector 这种方式 性能很差， 推荐使用 三个 float


### lua 引用 c#对象 ，代价高

c#不能作为指针直接给lua操作。因此使用 id 来表示一个对象 (unity + lua), C# 中通过 dictionary 来对应 id和 object 。
坏处 ： 每次使用 object 都会有查找的过程，对于经常使用的对象还好
- （未持有）对于临时对象，刚分配的 userdata，和 dictionary 索引因为 lua 的引用被 GC ，下一次，又会重复以上的准备过程，导致反复分配和GC 如 transform.position. 之后没有使用 会被lua 释放，之后 在 update 中的时候，就会重新分配

**因此不推荐串行 使用 (很多次.)， 对于 Object 类推荐持有**
### unity Vector3和 Quaternion 更加昂贵

主流方案事 使用纯 lua 代码， vector3 就是 {x,y,z} 

问题 ： 传值设计到 lua 类型和 c# 类型的转换
流程： 
1. c# 拿到 vector3 的 x,y,z
2. push 三个之到 lua 栈 
3. 构建表，将表赋值
4. 将表 push 到返回值内

一个传参 3次push参数，表内存分配，3次表插入， 。 --- **推荐添加一个函数如下 ： 直接使用 传入三个float就可以了**

```c#
void SetPos(GameObject obj, Vector3 pos);
void SetPos(GameObject obj, float x, float y, float z);
```


### 传参要避免的类型

- 最严重:  vector3 Quaternion 这种unity的值类型，**数组**
- 次严重 bool string 各种 object
- 建议 ： int float double

**次严重** ： c# 和 c 之间的传递问题 ， bool string 事 Non-Bittable 的， string  要考虑内存转换
**严重** : lua 和 C# 对象对应时的瓶颈  数组 最严重， 因此要逐个赋值


### 频繁调用的函数 参数不要超过四个

### 优先使用 static 函数到处，减少使用成员方法

object 需要查找 userdata 和 c#的引用， static 方法可以减少这种消耗。

```c#

class LuaUtil{
	static void SetPos(GameObject obj , float x, float y , float z ) { 
	obj.transfrom.position = new Vector3(x,y,z);
}
```

在 lua 中调用 `LuaUtil.SetPos(xxx)` 避免transform 的来回返回，以及临时 transform 被 GC

### lua拿着 C#对象 导致 C#对象无法释放。

Object 对象 使用过一个 dictionary 将 userData 和 C# 中的 Object 关联的。 **只要 lua 中的 userdata 没被回收， C# object 会被 Dictionary 持有引用** ， 导致无法回收。 

**常见的为** ： component ，如果 lua 引用，此时 Destory ，还会残留在 mono 堆中


可以通过遍历 ulua 中 ObjectTranslator 类 的 dcitionary --- 手动 nil

https://blog.csdn.net/weixin_42186870/article/details/121276271


### 上面的方案 ：lua 中 只使用 自己管理的id，不使用 C# 的 object

### 合理使用 out 关键字 返回复杂类型

```c#
vector3 GetPos(xxx)
void GetPos(GameObject obj, out float x, out float y, out float z);
```


getfloat3(get_field + to number 3次) 变为  isnumber + tonumber 
表查找 变为 访问栈 

## 闭包 

**UpValue**
- lua 中有全局栈， 所有的upvalue 指向栈里的值。离开作用域值会被释放。
- 闭包运行的时候 ，会找到upvalue 指针， 找到需要的外部需要的变量
- 有两个状态  open close

**闭包**
- 简洁 + 捕获外部变量形成不同的调用环境
- 会通过 upvalue 循环 linkedlist 找到需要的值

## 全局变量泛滥

配置 `_G` 的 `__newindex __index`

## 值类型传递产生GC

会产生拆装箱 从而导致 GC

```c#
[GCOptimize]
```

默认传递的值转化为 object O
优化后 使用 指定类型

## 热更新原理


require 会阻止多次加载先用的模块。

1. 保存 `_G` 中的 老模块 table
2. `package.loaded[module_name]` 对应的 模块 = nil
3. 获取新模块
4. 将 old_modle table 的值设为新模块的
5. 装填到 `package.loaded[module_name]`

![wAlxfn7LZh4EevX.png](https://s2.loli.net/2024/08/15/wAlxfn7LZh4EevX.png)

## lua的弱引用

将表  作为 table 的 key ， 将 表 nil， 使用  `collectgarbage`  表不会被回收， key2 为 nil， 但是指向的东西没有被回收。

```lua
t = {}

setmetatable(t, {__mode = "k"})

key2 = {name = "key2"}

t[key2] = 1;
key2 = nil

collectgarbage();

for k,v in pairs(t) do
	print(key,name .. ':' .. v)
end

-- 无法遍历 t 中的 key2.name
```

使用 `setmetatable(a, {__mode = "k"})` 解决

| 操作符 | 说明                                   |
| :-: | :----------------------------------- |
|  k  | 表的key为弱引用， 没有 key 的引用， table 资源也会被删除 |
|  v  | 表的value为弱引用                          |
| kv  | 都是弱引用                                |

如果 key2 被回收了 ， 此时 t 中 对应的项目会被回收


## Rehash + table 的结构

table 分为 数组部分和哈希部分

内粗大小动态分配， 如果空间不够就会分配， 如果太少就会缩少

做的事
- 计算 array part key
- 计算 hash part key
- 计算新设的 key 之后 array part 部分的数量
- 计算一个新的array part 部分需要分配的内存大小
- resize


```c
static void rehash (lua_State *L, Table *t, const TValue *ek) {  
  int nasize, na;  
  //#define MAXBITS		26  
  int nums[MAXBITS+1];    
  int i;  
  int totaluse;  
  // 初始化nums数组[1,MAXBITS]  
  // 注意一下0分片其实没有使用  
  for (i=0; i<=MAXBITS; i++) nums[i] = 0;    
  // 计算数组部分的已经使用(不为nil)的节点  
  nasize = numusearray(t, nums);    
  totaluse = nasize;    
  // 计算哈希表部分键值为数值的节点的数量  
  totaluse += numusehash(t, nums, &nasize);    
  // 统计额外的新的节点(ek)所在分片的值(0或者1)  
  nasize += countint(ek, nums);  
  totaluse++;  
  // 重新计算Table表的数组部分的长度  
  na = computesizes(nums, &nasize);  
  // 重新分配Table的数组部分长度和哈希列表的长度  
  // nasize为数组的最佳容量值(2的倍数容量)  
  // 哈希列表的长度为totaluse(总长度)-na(实际的数组长度)  
  resize(L, t, nasize, totaluse - na);  
}
```


Lua分配这两部分空间的原则也很简单，即优先计算数组部分，剩下的部分全放到散列表里。而如何决定数组部分的大小，Lua的作者们在《The Implementation of Lua 5.0》中已经说得很明白了：

数组的空间至少有一半以上被利用（保证空间的利用率）
数组的后半部分内至少有一个元素（避免只要一半空间就能装满却多浪费了一倍空间的情况）
为此，我们在重散列的过程中需要知道：

一共有多少个有效的整数key（value不为空）—— 变量na
这些整数key的分布情况 —— nums数组
所有的key的数量（用于计算散列表部分的容量）—— 变量totaluse
所以，rehash的逻辑也很清晰：

通过numusearray统计数组部分内包含的整数key数量和分布情况
通过numusehash统计散列表部分内包含的整数key数量和分布情况，并得到总共key的数量
通过computesizes计算应该分配给数组部分的空间大小
通过luaH_resize按照之前计算的结果重新分配空间


**总结**

- 尽量提前分配大小，
- 建议： `local tb = {nil, nil, nil}`
- 对于数组，尽量不包含 nil， 否则会出错
- 删除元素的呢与 对应的 key 赋值 nil， 但是删除 table 的有一个元素，不会触发表的重构行为， 即 rehash


## rawset rawget

直接操作表，可以忽略原表中的元方法。

```lua
rawset(table, key ,value); --绕过 __newindex
value = rawget(table, key); -- 绕过 __index 
```

## 调试原理

使用一个 钩子函数 Hook , 如果设置了钩子函数就够自动调用

```lua
void lua_sethook(lua_State *L, lua_Hook f, int  mask, int count)
```



- debug.gethook
- debug.sethook
- debug.getinfo
- debug.getlocal
- debug.setlocal
	- 得到和修改 局部变量的值


## Lua 内存管理

内存分配器 分配固定大小的内存块，使用内存块列表存储

周期性的进行回收，分为两个阶段: **标记阶段 + 清除阶段**

**标记阶段：** 从根集 root set 的地方出发， 逐步遍历可达到对象，标记为活动对象。 **root set** 包括啊全局变量，当前执行函数的局部变量
清楚阶段：清楚没有被标记的对象。
分代回收
可以手动管理

使用 三色标记法来进行清楚

https://dreamanddead.github.io/lua-5.1-source-guide/docs/gc/

改进后的 gc 过程如下：

- 初始阶段，所有对象标识为白色；
- 标记阶段的开始，将所有从 root 可达的对象标记为灰色；
- 标记阶段，逐个取出灰色对象，将其所有可达的白色对象标记为灰色，最后将自身标记为黑色；
- 清除阶段，当不存在灰色对象时，开始清除白色对象，将所有黑色对象标记回白色。

改进后的算法，标记阶段可以增量式的运行，随时暂停和继续。
## Xlua

### 1. xlua 步骤

1. 安装插件
2. 在settings 里 的 Scripting Define Symbols 添加 `HOTFIX_ENABLE` 宏 用于支持热更新
3. 对于有较大可能变动的类型或者函数上添加 `[HOTFIX]` 标签
4. 新建一个 空 gameobject 用于 存放 Lua热更新的管理脚本
5. `xlua.hotfix(xxxx, xxx, function)` 进行热更新
6. 点击 Xlua/Generate Code 自动收集 `HOTFIX` 标签的类并生成代码
7. 点击 inject in Editor 会对所有 HOTFIX 标签类进行注入
8. 运行游戏

### 2. 热更新原理

1. 点击生成代码后，跟根据内置的模板代码生成器，在GEN目录下生成一个 DelegatesGensBridge.cs 文件，其中有个 `__Gen_Delegate_Imp` 函数会映射到 xlua.hotfix 中的function。

```c#
namespace XLua
{
    public partial class DelegateBridge : DelegateBridgeBase
    {
        // DelegateBridge类的关键函数__Gen_Delegate_Imp*
        public void __Gen_Delegate_Imp0(object p0)
        {
            RealStatePtr L = luaEnv.rawL;
            // luaReference就是指向xlua.hotfix(CS.XXX, "Start", function(self))的function
            int errFunc = LuaAPI.pcall_prepare(L, errorFuncRef, luaReference);
            ObjectTranslator translator = luaEnv.translator;
            translator.PushAny(L, p0);
            PCall(L, 1, 0, errFunc);
            LuaAPI.lua_settop(L, errFunc - 1);
        }
    }
 }
```


2. 执行注入后， 会只用 Mono.Cecli 库对当前工厂进行 IL 注入， IL是 .Net 平台上的 C# 中间代码，中间代码会经过虚拟机编译成机器码给CPU。
3. 注入后的代码

```c#
[Hotfix(HotfixFlag.Stateless)]
public class Test : MonoBehaviour
{
    // 构造函数对应的DelegateBridge变量
    private static DelegateBridge _c__Hotfix0_ctor;
    private static DelegateBridge __Hotfix0_Start;
    private static DelegateBridge __Hotfix0_Update;
    private static DelegateBridge __Hotfix0_TestFunc;

    public Test()
        : this()
        {
            _c__Hotfix0_ctor?.__Gen_Delegate_Imp0(this);
        }

    private void Start()
    {
        DelegateBridge _Hotfix0_Start = __Hotfix0_Start;
        // 如果lua脚本里定义了热更新函数，就执行对应的热更新函数逻辑。
        if (_Hotfix0_Start != null)
        {
            _Hotfix0_Start.__Gen_Delegate_Imp0(this);
        }
        else
        {
            Debug.Log((object)"test");
        }
    }

    private void Update()
    {
        __Hotfix0_Update?.__Gen_Delegate_Imp0(this);
    }

    private void TestFunc()
    {
        __Hotfix0_TestFunc?.__Gen_Delegate_Imp0(this);
    }
}
```

使用这些 DelegateBrige 变量来进行热更新。
- 如果添加了对应的热更新函数， DelegateBridge 变量不为空， 并将 DelegateBridge 变量中的的 `__Gen_Delegate_Imp0` 指向 `xlua.hotfix(xxx)` , 如果为空，则 执行原有逻辑

实际上就是在运行的时候使用 lua 替换原本的 C# 函数