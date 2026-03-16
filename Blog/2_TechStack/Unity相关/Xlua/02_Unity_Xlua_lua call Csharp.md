
new C#对象


你在C#这样new一个对象：

```
var newGameObj = new UnityEngine.GameObject();
```

对应到Lua是这样：

```
local newGameObj = CS.UnityEngine.GameObject()
```

基本类似，除了：

```
1. lua里头没有new关键字；
2. 所有C#相关的都放到CS下，包括构造函数，静态成员属性、方法；
```

如果有多个构造函数呢？放心，xlua支持重载，比如你要调用GameObject的带一个string参数的构造函数，这么写：

```
local newGameObj2 = CS.UnityEngine.GameObject('helloworld')
```

## 访问C#静态属性，方法
### 读静态属性

```
CS.UnityEngine.Time.deltaTime
```

### 写静态属性

```
CS.UnityEngine.Time.timeScale = 0.5
```

### 调用静态方法

```
CS.UnityEngine.GameObject.Find('helloworld')
```

小技巧：如果需要经常访问的类，可以先用局部变量引用后访问，除了减少敲代码的时间，还能提高性能：

```
local GameObject = CS.UnityEngine.GameObject
GameObject.Find('helloworld')
```


> 调用成员方法 : `testobj:DMFunc()`


- 支持父类属性，方法

**参数的输入输出属性(out, ref)**

Lua调用侧的参数处理规则：C#的普通参数算一个输入形参，ref修饰的算一个输入形参，out不算，然后从左往右对应lua 调用侧的实参列表；

Lua调用侧的返回值处理规则：C#函数的返回值（如果有的话）算一个返回值，out算一个返回值，ref算一个返回值，然后从左往右对应lua的多返回值。

**重载方法**

由于 lua 中类型数量较少， 只能支持部分重载

直接通过不同的参数类型进行重载函数的访问，例如：

```lua
testobj:TestFunc(100)
testobj:TestFunc('hello')
```

**默认值**

和C#调用有默认值参数的函数一样，如果所给的实参少于形参，则会用默认值补上。


**可变参数方法**

对于C#的如下方法：

```c#
void VariableParamsFunc(int a, params string[] strs)
```

可以在lua里头这样调用：

```lua
testobj:VariableParamsFunc(5, 'hello', 'john')
```

**枚举值**

枚举类支持__CastFrom方法，可以实现从一个整数或者字符串到枚举值的转换，例如：

```lua
CS.Tutorial.TestEnum.__CastFrom(1)
CS.Tutorial.TestEnum.__CastFrom('E1')
```

**delegate**

C#的delegate调用：和调用普通lua函数一样

+操作符：对应C#的+操作符，把两个调用串成一个调用链，右操作数可以是同类型的C# delegate或者是lua函数。

-操作符：和+相反，把一个delegate从调用链中移除。

> Ps：delegate属性可以用一个luafunction来赋值。

**event**

比如testobj里头有个事件定义是这样：public event Action TestEvent;

增加事件回调

```
testobj:TestEvent('+', lua_event_callback)
```

移除事件回调

```
testobj:TestEvent('-', lua_event_callback)
```

**获取类型（相当于C#的typeof）**

比如要获取UnityEngine.ParticleSystem类的Type信息，可以这样

```
typeof(CS.UnityEngine.ParticleSystem)
```

 **“强”转**

lua没类型，所以不会有强类型语言的“强转”，但有个有点像的东西：告诉xlua要用指定的生成代码去调用一个对象，这在什么情况下能用到呢？有的时候第三方库对外暴露的是一个interface或者抽象类，实现类是隐藏的，这样我们无法对实现类进行代码生成。该实现类将会被xlua识别为未生成代码而用反射来访问，如果这个调用是很频繁的话还是很影响性能的，这时我们就可以把这个interface或者抽象类加到生成代码，然后指定用该生成代码来访问：

```
cast(calc, typeof(CS.Tutorial.Calc))
```

上面就是指定用CS.Tutorial.Calc的生成代码来访问calc对象。