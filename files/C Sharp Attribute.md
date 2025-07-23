---
tags:
  - unity
---
用于在运行中进行信息传递.

**基本语法**

```c#
[attribute(positional_parameters, name_parameter = value, ...)]
element
```

## 自定义特性

四个步骤:

- 声明自定义特性
- 构建特性
- 在目标元素上应用
- 通过反射访问特性

### 声明及构建特性

```c#
// 一个自定义特性 BugFix 被赋给类及其成员
[AttributeUsage(AttributeTargets.Class |
AttributeTargets.Constructor |
AttributeTargets.Field |
AttributeTargets.Method |
AttributeTargets.Property,
AllowMultiple = true)]

public class DeBugInfo : System.Attribute
{
	  private int bugNo;
	  private string developer;
	  private string lastReview;
	  public string message;

}
```

### 应用特性

```c#
[DeBugInfo(49, "Nuha Ali", "10/10/2012", Message = "Unused variable")]
class Rectangle
```


### 通过反射获取并使用这些特性

```c#
 System.Reflection.MemberInfo info = typeof(MyClass);  
 object[] attributes = info.GetCustomAttributes(true);  
 for (int i = 0; i < attributes.Length; i++)  
 {  
	System.Console.WriteLine(attributes[i]);  
 }  
 Console.ReadKey();
```