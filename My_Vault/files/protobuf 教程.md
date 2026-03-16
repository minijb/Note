---
tags:
  - unity
  - protobuf
---
## proto 3 风格

```proto
syntax = "proto3";

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 results_per_page = 3;
}
```

第一行指定版本，之后指定键值对
每一个键值对都有一个编号，编号唯一

指定字段标签

```proto
    optional string key = 1;
    optional int32 value = 2;
```

optional
- 字段已设置，并且包含显式设置或从线路解析的值。它将序列化到线路。
- 字段未设置，并将返回默认值。它不会序列化到线路

repeated
- 此字段类型可以在格式良好的消息中重复零次或多次。将保留重复值的顺序。

map
- 这是一个配对键/值字段类型

## 转化类型

| .proto 类型 | 注释                                             | C++ 类型 | Java/Kotlin 类型[1] | Python 类型[3]                         | Go 类型   | Ruby 类型                | C# 类型      | PHP 类型            | Dart 类型 |
| --------- | ---------------------------------------------- | ------ | ----------------- | ------------------------------------ | ------- | ---------------------- | ---------- | ----------------- | ------- |
| double    |                                                | double | double            | float                                | float64 | Float                  | double     | float             | double  |
| float     |                                                | float  | float             | float                                | float32 | Float                  | float      | float             | double  |
| int32     | 使用可变长度编码。对编码负数效率不高 - 如果您的字段可能具有负值，请改用 sint32。  | int32  | int               | int                                  | int32   | Fixnum 或 Bignum（视需要而定） | int        | integer           | int     |
| int64     | 使用可变长度编码。对编码负数效率不高 - 如果您的字段可能具有负值，请改用 sint64。  | int64  | long              | int/long[4]                          | int64   | Bignum                 | long       | integer/string[6] | Int64   |
| uint32    | 使用可变长度编码。                                      | uint32 | int[2]            | int/long[4]                          | uint32  | Fixnum 或 Bignum（视需要而定） | uint       | integer           | int     |
| uint64    | 使用可变长度编码。                                      | uint64 | long[2]           | int/long[4]                          | uint64  | Bignum                 | ulong      | integer/string[6] | Int64   |
| sint32    | 使用可变长度编码。有符号 int 值。与常规 int32 相比，它们更有效地对负数进行编码。 | int32  | int               | int                                  | int32   | Fixnum 或 Bignum（视需要而定） | int        | integer           | int     |
| sint64    | 使用可变长度编码。有符号 int 值。与常规 int64 相比，它们更有效地对负数进行编码。 | int64  | long              | int/long[4]                          | int64   | Bignum                 | long       | integer/string[6] | Int64   |
| fixed32   | 始终为四个字节。如果值通常大于 228，则比 uint32 更有效。             | uint32 | int[2]            | int/long[4]                          | uint32  | Fixnum 或 Bignum（视需要而定） | uint       | integer           | int     |
| fixed64   | 始终为八个字节。如果值通常大于 256，则比 uint64 更有效。             | uint64 | long[2]           | int/long[4]                          | uint64  | Bignum                 | ulong      | integer/string[6] | Int64   |
| sfixed32  | 始终为四个字节。                                       | int32  | int               | int                                  | int32   | Fixnum 或 Bignum（视需要而定） | int        | integer           | int     |
| sfixed64  | 始终为八个字节。                                       | int64  | long              | int/long[4]                          | int64   | Bignum                 | long       | integer/string[6] | Int64   |
| bool      |                                                | bool   | boolean           | bool                                 | bool    | TrueClass/FalseClass   | bool       | boolean           | bool    |
| string    | 字符串必须始终包含 UTF-8 编码或 7 位 ASCII 文本，并且不能长于 232。   | string | String            | str/unicode[5]                       | string  | String (UTF-8)         | string     | string            | String  |
| bytes     | 可能包含不长于 232 的任何任意字节序列。                         | string | ByteString        | str (Python 2)  <br>bytes (Python 3) | []byte  | String (ASCII-8BIT)    | ByteString | string            | List    |
## 默认值

- 对于字符串，默认值为空字符串。
- 对于字节，默认值为空字节。
- 对于布尔值，默认值是 false。
- 对于数字类型，默认值是零。
- 对于枚举，默认值是**第一个定义的枚举值**，它必须是 0。

## 枚举

在定义消息类型时，您可能希望其某个字段仅具有预定义值列表中的一个值。例如，假设您想为每个 `SearchRequest` 添加一个 `corpus` 字段，其中语料库可以是 `UNIVERSAL`、`WEB`、`IMAGES`、`LOCAL`、`NEWS`、`PRODUCTS` 或 `VIDEO`。您可以通过向消息定义中添加一个 `enum` 来非常简单地实现此目的，其中每个可能的枚举值都有一个常量。

```proto
enum Corpus {
  CORPUS_UNSPECIFIED = 0;
  CORPUS_UNIVERSAL = 1;
  CORPUS_WEB = 2;
  CORPUS_IMAGES = 3;
  CORPUS_LOCAL = 4;
  CORPUS_NEWS = 5;
  CORPUS_PRODUCTS = 6;
  CORPUS_VIDEO = 7;
}

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 results_per_page = 3;
  Corpus corpus = 4;
}
```


## Any

`Any` 消息类型允许您将消息用作嵌入式类型，而无需其 .proto 定义。`Any` 包含一个任意序列化的消息作为 `bytes`，以及一个充当该消息类型的全局唯一标识符并解析为该消息类型的 URL。要使用 `Any` 类型，您需要 [导入](https://protobuf.com.cn/programming-guides/proto3/#other) `google/protobuf/any.proto`。

```proto
import "google/protobuf/any.proto";

message ErrorStatus {
  string message = 1;
  repeated google.protobuf.Any details = 2;
}
```


## Oneof

如果您有一个包含许多字段的消息，并且最多只能同时设置一个字段，则可以通过使用 oneof 特性来强制执行此行为并节省内存。
Oneof 字段类似于常规字段，除了 oneof 中的所有字段共享内存之外，并且最多只能同时设置一个字段。设置 oneof 的任何成员会自动清除所有其他成员。您可以使用特殊的 `case()` 或 `WhichOneof()` 方法（取决于您选择的语言）来检查 oneof 中设置的值（如果有）。

请注意，如果设置了_多个值，则按 proto 中的顺序确定的最后一个设置值将覆盖所有前一个值_。

```proto
message SampleMessage {
  oneof test_oneof {
    string name = 4;
    SubMessage sub_message = 9;
  }
}
```


## 包

您可以向 `.proto` 文件添加可选的 `package` 说明符，以防止协议消息类型之间的名称冲突。

```proto
package foo.bar;
message Open { ... }
```

- 在 **C++** 中，生成的类被包装在 C++ 命名空间内。例如，`Open` 将位于命名空间 `foo::bar` 中。
- 在 **Java** 和 **Kotlin** 中，包用作 Java 包，除非您在 `.proto` 文件中明确提供 `option java_package`。
- 在 **Python** 中，`package` 指令被忽略，因为 Python 模块是根据它们在文件系统中的位置组织的。
- 在 **Go** 中，`package` 指令被忽略，生成的 `.pb.go` 文件位于以相应的 `go_proto_library` Bazel 规则命名的包中。对于开源项目，您**必须**提供 `go_package` 选项或设置 Bazel `-M` 标志。
- 在**Ruby**中，生成的类被包装在嵌套的 Ruby 命名空间中，并转换为所需的 Ruby 大写风格（首字母大写；如果第一个字符不是字母，则添加前缀`PB_`）。例如，`Open` 将位于命名空间 `Foo::Bar` 中。
- 在**PHP**中，包在转换为 PascalCase 后用作命名空间，除非您在 `.proto` 文件中明确提供了 `option php_namespace`。例如，`Open` 将位于命名空间 `Foo\Bar` 中。
- 在**C#**中，包在转换为 PascalCase 后用作命名空间，除非您在 `.proto` 文件中明确提供了 `option csharp_namespace`。例如，`Open` 将位于命名空间 `Foo.Bar` 中。

## 实例

```proto
syntax = "proto3";
 
message pb_user_info {
    string user_id = 1;
    string leader_id = 2;
    repeated string members = 3;
    int32 status = 4;
}
```


```c#
var userInfo = new pb_user_info
{
    LeaderId = "123",
    Status = 5,
    UserId = "newbie"
};
userInfo.Members.Add("张三");
userInfo.Members.Add("李四");

//序列化获取二进制数据
var bytes = userInfo.ToByteArray();


//反序列化获取对象
var ub = new pb_user_info();
ub.MergeFrom(bytes);

Console.WriteLine($"ub.UserId={ub.UserId}");
Console.WriteLine($"userInfo.Status={userInfo.Status}");
Console.WriteLine($"userInfo.LeaderId={userInfo.LeaderId}");
Console.WriteLine($"userInfo.Members={string.Join(",", userInfo.Members)}");
```


https://blog.csdn.net/e295166319/article/details/52806791