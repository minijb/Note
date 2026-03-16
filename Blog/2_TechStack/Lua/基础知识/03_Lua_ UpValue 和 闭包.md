
一个 UpValue 是指一个函数内部被引用量为外部局部变量，而不是函数参数。

及时外部函数执行结束了，引用这个局部变量的内部函数人可以访问和修改这个值。

```lua
print("\nexample 3:");
function counter()
    local count = 0;
    return function()
        count = count + 1;
        return count;
    end
end

func = counter();
print(func());
print(func());
print(func());
```


### 1. 共享

多个闭包引用一个外部局部变量，实际为共享同一个 UpValue

### 2. 关闭和开启

一个闭包被创建的时候开启，没有任何必报引用的时候关闭--资源回收。 

### 3. 存储

lua 会正常一个全局栈，  所有upvalue 会指向该栈中的值。如果对应的参数离开作用域，栈中的值也会被释放。