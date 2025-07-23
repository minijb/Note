---
tags:
  - unity
  - Csharp
---

**为什么会产生GC**

1. 主要是匿名函数+捕获的锅
2. 匿名函数使用 局部变量的时候，会生成一个闭包类，这就会产生GC
3. 注意：生成的闭包类的生命周期跟着 匿名函数走的。
	1. 如果我们有一个 List 存储匿名函数，这就会造成资源无法释放
	2. 同时生成的闭包类也很大

https://www.cnblogs.com/gougou1981/p/12490534.html
https://zhuanlan.zhihu.com/p/478295269
https://lizijie.github.io/2020/03/10/%E8%AE%B0%E4%B8%80%E6%AC%A1C-%E6%95%B0%E6%8D%AE%E5%8C%85GC%E4%BC%98%E5%8C%96.html


**优化方法：**

1. 及时释放资源
2. 自己写一个 struct 闭包类， 此时在退出当前的局部环境的时候会自动释放资源。(Struct 在栈上， 退出返回会自动释放资源)


