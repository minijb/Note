
**什么是扩展方法**

- 特殊的静态方法， 可以先实例方法一样调用

最常见的就是将 string 进行扩展

```c#
public static class StringExtensions
{
    public static string ToReverse(this string str)
    {
        if (string.IsNullOrEmpty(str))
            return str;

        char[] charArray = str.ToCharArray();
        Array.Reverse(charArray);
        return new string(charArray);
    }
}

// 使用扩展方法
class Program
{
    static void Main()
    {
        string text = "hello";
        string reversed = text.ToReverse(); // 调用扩展方法
        Console.WriteLine(reversed); // 输出：olleh
    }
```


**集合类型的扩展**

```c#
public static class CollectionExtensions
{
    public static string ToFormattedString<T>(this IEnumerable<T> collection)
    {
        return string.Join(", ", collection);
    }
}

// 使用扩展方法
class Program
{
    static void Main()
    {
        var numbers = new List<int> { 1, 2, 3, 4, 5 };
        string result = numbers.ToFormattedString(); // 调用扩展方法
        Console.WriteLine(result); // 输出：1, 2, 3, 4, 5
    }
}
```

### **常用场景**

1. 扩展框架类型：为系统类型（如 `string`, `int`, `DateTime`）添加新方法。
2. 简化代码：提供更简洁的调用方式。
3. 增强 `[LINQ](https://zhida.zhihu.com/search?content_id=252173735&content_type=Article&match_order=1&q=LINQ&zhida_source=entity)` 功能：许多 `LINQ` 方法（如 `Where`, `Select`）本质上是扩展方法。
4. 代码复用：为通用操作创建工具方法，提高可读性和复用性。


| 特性       | 扩展方法               | 静态方法           |
| -------- | ------------------ | -------------- |
| 调用方式     | 像实例方法一样调用          | 类名.方法名调用       |
| 代码可读性    | 更贴近面向对象，语义清晰       | 操作看起来不属于对象行为   |
| 修改现有类型需求 | 不需要修改类型定义          | 不修改类型，但调用语法冗长  |
| 链式调用     | 支持流畅的链式调用          | 不支持链式调用        |
| 开发体验     | 自动提示可扩展方法，使用直观     | 需要记住类名和方法名     |
| 使用场景     | 添加新功能到现有类型，符合对象的语义 | 与特定上下文无关的工具类方法 |
