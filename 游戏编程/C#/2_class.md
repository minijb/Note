# Class

两种成员类型：instance，static

instance----可以由对象对用

static----可以由类调用`public static xxx xxx(){}`

## 1. 构造函数

```c#
public class Name{
    public Name(xxx){
        
    }
}
```

构造函数时可以重载的

```c#
using System.Collections.Generic;

namespace app1
{
    public class Customer
    {
        public int Id;
        public string Name;
        public List<Customer> customers;
        public Customer()
        {
            customers = new List<Customer>();
        }
//：表示在执行当前函数的时候先执行：后面的语句
        public Customer(int id) : this()
        {
            this.Id = id;
        }
    }
}

```

