---
tags:
  - Csharp
---
https://www.cnblogs.com/JimmyZheng/archive/2012/03/17/2402814.html

**字节序列**
字节对象都被存储为连续的字节序列，字节按照一定的顺序进行排序组成了字节序列

## Stream

抽象化的方法:

**1:  CanRead: 只读属性**，判断该流是否能够读取：
**2:  CanSeek: 只读属性**，判断该流是否支持跟踪查找
**3:  CanWrite: 只读属性**，判断当前流是否可写
**4:  void Flush()**:<font color="#ff0000"> 当我们使用流写文件时，数据流会先进入到缓冲区中，而不会立刻写入文件，当执行这个方法后，缓冲区的数据流会立即注入基础流</font>
在使用Stream的时候， 它的一头连接和源字节流相连，另外一头与目标设备相连（例如文件， 缓冲区， 蓝牙设备等）， 某些类型的Stream在与目标设备的链接之间可以设置缓冲区。 Flush（）函数的作用就是强制将当前的缓冲区的内容写入目标设备上面，为下一次的写入做准备。
**5: Length:表示流的长度**
**6: Position属性：（非常重要）**
虽然从字面中可以看出这个Position属性只是标示了流中的一个位置而已，可是我们在实际开发中会发现这个想法会非常的幼稚.很多asp.net项目中文件或图片上传中很多朋友会经历过这样一个痛苦：Stream对象被缓存了，导致了Position属性在流中无法.找到正确的位置，这点会让人抓狂，其实解决这个问题很简单，聪明的你肯定想到了，其实我们每次使用流前必须将Stream.Position.设置成0就行了，但是这还不能根本上解决问题，最好的方法就是用Using语句将流对象包裹起来，用完后关闭回收即可。
**7: abstract int Read(byte[] buffer, int offset, int count)**
这个方法包含了3个关键的参数：缓冲字节数组，位移偏量和读取字节个数，每次读取一个字节后会返回一个缓冲区中的总字节数
**第一个参数**：这个数组相当于一个空盒子，Read（）方法每次读取流中的一个字节将其放进这个空盒子中。（全部读完后便可使用buffer字节数组了）
**第二个参数**：表示位移偏量，告诉我们从流中哪个位置（偏移量）开始读取。
**最后一个参数**：就是读取多少字节数。**返回值**便是总共读取了多少字节数.
**8: abstract long Seek(long offset, SeekOrigin origin)**
其实Seek方法就是重新设定流中的一个位置，在说明offset参数作用之前大家先来了解下SeekOrigin这个枚举
- Begin 
- Current
- End
如果 offset 为负，则要求新位置位于 origin 指定的位置之前，其间隔相差 offset 指定的字节数。如果 offset 为零 (0)，则要求新位置位于由 origin 指定的位置处。

如果 offset 为正，则要求新位置位于 origin 指定的位置之后，其间隔相差 offset 指定的字节数.

Stream. Seek(-3,Origin.End);  表示在流末端往前数第3个位置
Stream. Seek(0,Origin.Begin); 表示在流的开头位置
Stream. Seek(3,Orig`in.Current); 表示在流的当前位置往后数第三个位置

查找之后会返回一个流中的一个新位置。其实说道这大家就能理解Seek方法的精妙之处了吧
**`9: abstract void Write(byte[] buffer,int offset,int count)`**
这个方法包含了3个关键的参数：缓冲字节数组，位移偏量和读取字节个数
和read方法不同的是 write方法中的第一个参数buffer已经有了许多byte类型
的数据，我们只需通过设置 offset和count来将buffer中的数据写入流中
**10: virtual void Close()**
关闭流并释放资源，在实际操作中，如果不用using的话，别忘了使用完流之后将其关闭
这个方法特别重要，使用完当前流千万别忘记关闭！

案例 ： https://www.cnblogs.com/JimmyZheng/archive/2012/03/17/2402814.html

### 异步操作

```c#
//异步读取
public virtual IAsyncResult BeginRead(byte[] buffer,int offset,int count,AsyncCallback callback,Object state)
//异步写
public virtual IAsyncResult BeginWrite( byte[] buffer, int offset, int count, AsyncCallback callback, Object state )
//结束异步读取
public virtual int EndRead( IAsyncResult asyncResult ) 
//结束异步写
public virtual void EndWrite( IAsyncResult asyncResult )  s
```

begin和end 必须对应出现


