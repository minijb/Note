
**简介：** 可变长度的 string

**初始化**

```c#
StringBuilder myStringBuilder = new StringBuilder("Hello World!");C
StringBuilder myStringBuilder = new StringBuilder("Hello World!", 25); // 进行扩容 ： 扩容到 25个空格

// 利用 Capacity 属性控制最大对象长度
myStringBuilder.Capacity = 25;

```



## 修改 StringBuilder 字符串

下表列出了可用于修改 **StringBuilder** 内容的方法。

| 方法名称                                                                                                              | 使用                                                 |
| ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [StringBuilder.Append](https://learn.microsoft.com/zh-cn/dotnet/api/system.text.stringbuilder.append)             | 将信息追加到当前 **StringBuilder** 的末尾。                    |
| [StringBuilder.AppendFormat](https://learn.microsoft.com/zh-cn/dotnet/api/system.text.stringbuilder.appendformat) | 将字符串中传递的格式说明符替换为带格式的文本。                            |
| [StringBuilder.Insert](https://learn.microsoft.com/zh-cn/dotnet/api/system.text.stringbuilder.insert)             | 将字符串或对象插入当前 **StringBuilder** 的指定索引中。              |
| [StringBuilder.Remove](https://learn.microsoft.com/zh-cn/dotnet/api/system.text.stringbuilder.remove)             | 从当前 **StringBuilder** 中删除指定数量的字符。                  |
| [StringBuilder.Replace](https://learn.microsoft.com/zh-cn/dotnet/api/system.text.stringbuilder.replace)           | 将当前**StringBuilder**中所有指定字符或字符串的出现替换为另一个指定的字符或字符串。 |
| sb.AppendLine                                                                                                     |                                                    |

[详细文档](https://learn.microsoft.com/zh-cn/dotnet/api/system.text.stringbuilder?view=net-9.0)


#TODO  appendFormat : 实现了 IFormattable 接口

