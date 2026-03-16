---
tags:
  - unity
  - lua
---
步骤：
- 添加特性
- 在 build setting， player setting ， Script defines symbols 中 添加 `HOTFIX_ENABLE`
- xlua 生成代码
- hotfix 注入 (提前添加 tools 文件)

```lua

-- hotfix 热补丁注入

-- hotfix(类， "函数名", lua 函数)
xlua.hotfix(CS.Hotfix, "Add", function (self, a, b)
    return a + b
end)


-- 静态方法 不需要selfj
xlua.hotfix(CS.Hotfix, "Speak", function (a)
    print(a)   
end)
```


```c#

[Hotfix]
public class Hotfix : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        LuaManager.instance.Init();
        LuaManager.instance.doFile("Main");
        Debug.Log(Add(10,10));
        Speak("has been hotfixed");
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public int Add(int a, int b){
        return 0;
    }

    public static void Speak(string str){
        Debug.Log("123456");
    }
}


```

## 多函数替换

```lua
-- 传入 类名， 并传入一个表
xlua.hotfix(CS.Hotfix, {
    Update = function (self)
        print(os.time())
    end,

    Add = function (self, a, b)
        return (a + b) * 100
    end,

    Speak = function (str)
        print(str)
    end
})
```


## 未继承 mono

```lua
xlua.hotfix(CS.Hotfix_T, {
    -- 析构函数和构造函数，和其他函数不同，先使用 原本的逻辑再使用 lua 逻辑
    [".ctor"] = function () -- 构造函数固定写法
        print("Lua 热补丁构造函数")
    end,

    Speak = function (self, a)
        print("lua : " .. a)
    end,

    Finalize = function () -- 析构函数
        
    end,
})
```


```lua
[Hotfix]
public class Hotfix_T
{
    public Hotfix_T(){
        Debug.Log("Hotfixxxx");
    }

    public void Speak(string str){
        Debug.Log("" + str);
    }

    ~Hotfix_T(){}
}



```


## 替换协程函数

```c#
local util = require 'xlua.util'
xlua.hotfix(CS.HotfixTest,{
    tt1 = function(self)
        return util.cs_generator(function()
            while true do
                coroutine.yield(CS.UnityEngine.WaitForSeconds(3))
                print('Wait for 3 seconds')
            end
        end)
    end;
})
```


## 索引器，属性替换

```c#
xlua.hotfix(CS.HotfixTest ,{
	set_Age = function ()
        print(10000)
    end,
	get_Age = function ()
        return 100000;
    end,
})


xlua.hotfix(CS.HotfixTest ,{ --- 索引器
	set_Item = function ()
        print(10000)
    end,
	get_Item = function ()
        return 100000;
    end,
})
```


## 事件热更新

```c#
[Hotfix]
public class HotfixTest : MonoBehaviour
{
    public int Age {
        get{
            return 100;
        }
        set{
            Debug.Log("100");
        }
    }

    event UnityAction myEvent;
    
    void Start()
    {
        LuaManager.instance.Init();
        LuaManager.instance.doFile("Main");
        myEvent += testtest;
        myEvent -= testtest;
    }



    private void testtest(){

    }
}


```

```lua
xlua.hotfix(CS.HotfixTest, {
    -- add_事件名
    -- remove_事件名

    add_myEvent = function (self, del)
        print(del)
        print("add event")

        -- 不可以
        -- self:myEvent("+", del)
        -- 可以存入 lua 中
    end,

    remove_myEvent = function (self, del)
        print(del)
        print("delete event")
    end,
})
```

## 泛型类的替换

```c#
[Hotfix]
public class HotfixTest2<T>{
    public void test(T str){
        Debug.Log(str);
    }
}

[Hotfix]
public class HotfixTest : MonoBehaviour
{
    public int Age {
        get{
            return 100;
        }
        set{
            Debug.Log("100");
        }
    }

    event UnityAction myEvent;
    
    void Start()
    {
        LuaManager.instance.Init();
        LuaManager.instance.doFile("Main");
        myEvent += testtest;
        myEvent -= testtest;

        HotfixTest2<string> t1 = new HotfixTest2<string>();
        t1.test("100");
        HotfixTest2<int> t2 = new HotfixTest2<int>();
        t2.test(200);
    }



```

```lua

xlua.hotfix(CS.HotfixTest2(CS.System.String), {
    test = function (self, str)
        
        print("hotfix : " .. str)
    end
})
```

只改变了 string 泛型的类