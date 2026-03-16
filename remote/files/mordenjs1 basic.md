---
tags:
  - js
---
## 导入js代码

```html
<script type="text/javascript"><!--
    ...
//--></script>


<script src="/path/to/script.js"></script>
```

> 使用严格模式 `"use strict";`

## 变量

三种命名方式 let,const,var

var 
- 没有块级作用域
- 可以重新声明

### number

number: 整数，浮点数，`Infinity`：无限大 和 `NaN` : 计算错误。

NaN 和任何东西计算都是 NaN

### BigInt 类型

```js
// 尾部的 "n" 表示这是一个 BigInt 类型
const bigInt = 1234567890123456789012345678901234567890n;
```

### string

在 JavaScript 中，有三种包含字符串的方式。

1. 双引号：`"Hello"`.
2. 单引号：`'Hello'`.
3. 反引号：`` `Hello` ``.

双引号和单引号都是“简单”引用，在 JavaScript 中两者几乎没有什么差别。

反引号是 **功能扩展** 引号。它们允许我们通过将变量和表达式包装在 `${…}` 中，来将它们嵌入到字符串中。

```js
let name = "John";

// 嵌入一个变量
alert( `Hello, ${name}!` ); // Hello, John!

// 嵌入一个表达式
alert( `the result is ${1 + 2}` ); // the result is 3
```

### Boolean

### null

### undefined

如果一个变量已被声明，但未被赋值，那么它的值就是 `undefined`：

```js
let age;

alert(age); // 弹出 "undefined"
```

### Object and Symbol

`object` 则用于储存数据集合和更复杂的实体。
`symbol` 类型用于创建对象的唯一标识符。

### typeof 返回数据类型

```js
typeof undefined // "undefined"

typeof 0 // "number"

typeof 10n // "bigint"

typeof true // "boolean"

typeof "foo" // "string"

typeof Symbol("id") // "symbol"

typeof Math // "object"  (1)

typeof null // "object"  (2)

typeof alert // "function"  (3)
```

## 交互 alert , prompt and confirm

```js
alert("Hello");
// 显示一个带有文本消息的模态窗口，还有 input 框和确定/取消按钮
let result = prompt(title, [default]);
// 显示一个带有 `question` 以及确定和取消两个按钮的模态窗口
let result = confirm(question);
```

## 类型转化

**字符串** : `value = String(value);`
**数字 and boolean**: 

在算术函数和表达式中，会自动进行 number 类型转换。

```js
alert( "6" / "2" ); // 3, string 类型的值被自动转换成 number 类型后进行计算
let num = Number(str); // 变成 number 类型 123
Boolean("hello")
```



https://zh.javascript.info/operators