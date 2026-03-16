---
tags:
  - Csharp
---
## 转化字节数组

`BitConverter` : 

| 型                                                                                   | 到字节转换                                                                                                                                                                                                                                                                                                                                                                | 从字节转换                                                                                                                                                                                                                                               |
| ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Boolean](https://learn.microsoft.com/zh-cn/dotnet/api/system.boolean?view=net-8.0) | [GetBytes(Boolean)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-boolean))                                                                                                                                                                                                             | [ToBoolean](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.toboolean?view=net-8.0)                                                                                                                                                |
| [Char](https://learn.microsoft.com/zh-cn/dotnet/api/system.char?view=net-8.0)       | [GetBytes(Char)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-char))                                                                                                                                                                                                                   | [ToChar](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.tochar?view=net-8.0)                                                                                                                                                      |
| [Double](https://learn.microsoft.com/zh-cn/dotnet/api/system.double?view=net-8.0)   | [GetBytes(Double)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-double))  <br>  <br>- 或 -  <br>  <br>[DoubleToInt64Bits(Double)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.doubletoint64bits?view=net-8.0#system-bitconverter-doubletoint64bits(system-double)) | [ToDouble](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.todouble?view=net-8.0)  <br>  <br>- 或 -  <br>  <br>[Int64BitsToDouble](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.int64bitstodouble?view=net-8.0) |
| [Int16](https://learn.microsoft.com/zh-cn/dotnet/api/system.int16?view=net-8.0)     | [GetBytes(Int16)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-int16))                                                                                                                                                                                                                 | [ToInt16](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.toint16?view=net-8.0)                                                                                                                                                    |
| [Int32](https://learn.microsoft.com/zh-cn/dotnet/api/system.int32?view=net-8.0)     | [GetBytes(Int32)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-int32))                                                                                                                                                                                                                 | [ToInt32](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.toint32?view=net-8.0)                                                                                                                                                    |
| [Int64](https://learn.microsoft.com/zh-cn/dotnet/api/system.int64?view=net-8.0)     | [GetBytes(Int64)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-int64))                                                                                                                                                                                                                 | [ToInt64](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.toint64?view=net-8.0)                                                                                                                                                    |
| [Single](https://learn.microsoft.com/zh-cn/dotnet/api/system.single?view=net-8.0)   | [GetBytes(Single)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-single))                                                                                                                                                                                                               | [ToSingle](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.tosingle?view=net-8.0)                                                                                                                                                  |
| [UInt16](https://learn.microsoft.com/zh-cn/dotnet/api/system.uint16?view=net-8.0)   | [GetBytes(UInt16)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-uint16))                                                                                                                                                                                                               | [ToUInt16](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.touint16?view=net-8.0)                                                                                                                                                  |
| [UInt32](https://learn.microsoft.com/zh-cn/dotnet/api/system.uint32?view=net-8.0)   | [GetBytes(UInt32)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-uint32))                                                                                                                                                                                                               | [ToUInt32](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.touint32?view=net-8.0)                                                                                                                                                  |
| [UInt64](https://learn.microsoft.com/zh-cn/dotnet/api/system.uint64?view=net-8.0)   | [GetBytes(UInt64)](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.getbytes?view=net-8.0#system-bitconverter-getbytes(system-uint64))                                                                                                                                                                                                               | [ToUInt64](https://learn.microsoft.com/zh-cn/dotnet/api/system.bitconverter.touint64?view=net-8.0)                                                                                                                                                  |

`Toxxx(bytes, start[int])`

## 合并数组

```c#
string[] s1 = new string[4];
string[] s2 = new string[2] { "1", "3"};
string[] s3 = new string[2] { "3", "4"};
s2.CopyTo(s1, 0);
s3.CopyTo(s1, 2);
```

从指定的目标数组索引处开始，将当前一维数组的所有元素复制到指定的一维数组中。 索引指定为 32/64 位整数。

## string 和 byte 之间的转换

string转byte[]:
`byte[] byteArray = System.Text.Encoding.Default.GetBytes ( str );`
 
byte[]转string：
`string str = System.Text.Encoding.Default.GetString ( byteArray );`
 
string转ASCII byte[]:
`byte[] byteArray = System.Text.Encoding.ASCII.GetBytes ( str );`
 
ASCII byte[]转string:
`string str = System.Text.Encoding.ASCII.GetString ( byteArray );`

## 字符串分割

`string[] b = a.Split('|');`