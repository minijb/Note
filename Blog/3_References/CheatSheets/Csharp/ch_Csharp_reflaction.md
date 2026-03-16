
## 1. 获取类型

```c#
// =============1. typeof 编译时已知类型（静态类型）=============
Type stringType = typeof(string);     // 内置类型


// =============2. GetType() 方法 运行时通过对象实例获取类型（需要对象实例）。
int num = 42;
Type intType = num.GetType();          // 获取 int 类型


// =============3. Type.GetType(string typeName) 通过字符串
// 基础类型（在 mscorlib 中）
Type intType = Type.GetType("System.Int32");
// 当前程序集中的类型
Type localType = Type.GetType("MyNamespace.MyClass");
// 其他程序集中的类型（需程序集全名）
Type externalType = Type.GetType(
    "MyNamespace.MyClass, MyAssembly, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"
);

// =============4. 通过程序集反射获取
// 获取当前执行程序集
Assembly currentAssembly = Assembly.GetExecutingAssembly();

// 获取所有类型
Type[] allTypes = currentAssembly.GetTypes();

// 按名称获取特定类型
Type specificType = currentAssembly.GetType("MyNamespace.MyClass");

// 从外部 DLL 加载
Assembly externalAssembly = Assembly.LoadFrom("MyLib.dll");
Type externalType = externalAssembly.GetType("MyNamespace.ExternalClass");

//============= 5. 通过泛型参数获得
public class GenericClass<T>
{
    public void PrintType()
    {
        Type typeParam = typeof(T);  // 获取 T 的实际类型
        Console.WriteLine(typeParam);
    }
}

// ================ 6. dynamic 对象运行时的类型
dynamic dynamicObj = GetDynamicObject();
Type runtimeType = dynamicObj?.GetType(); // 可能为 null

//7. 特殊类型获取
// 数组类型：
Type arrayType = new int[10].GetType();      // typeof(int[])
Type elementType = arrayType.GetElementType(); // 获取元素类型 (int)

//泛型构造类型：
Type closedGeneric = typeof(List<int>);      // 闭合泛型类型
Type openGeneric = closedGeneric.GetGenericTypeDefinition(); // 原始泛型 List<>

//可空类型：
csharp
Type nullableType = typeof(int?);             // System.Nullable<int>
Type underlyingType = Nullable.GetUnderlyingType(nullableType); // int


```

| **方法**                 | **是否需要实例** | **编译时/运行时** | **典型场景**      |
| ---------------------- | ---------- | ----------- | ------------- |
| `typeof(T)`            | ❌          | 编译时         | 静态类型已知        |
| `obj.GetType()`        | ✔️         | 运行时         | 获取对象实际类型（多态）  |
| `Type.GetType("Name")` | ❌          | 运行时         | 动态加载类型（需完整名称） |
| 程序集反射                  | ❌          | 运行时         | 扫描程序集或加载外部类型  |

## 2. 常用反射方法

[doc](https://learn.microsoft.com/zh-cn/dotnet/api/system.type?view=net-6.0)

### 2.1 判断是什么

`isXXX` 

常用:
- `isClass`
- `isMethod`

### 2.2 获取东西

`getXXX`

常见：






#TODO 

