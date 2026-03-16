---
tags:
  - unity
---

## 粘包

```c#
// 得到长度

byte[] length_Bytes = BitConverter.GetBytes((Int16)bodyBytes.Length);
byte[] toSendBytes = length_Bytes.Contcat(bodyBytes).toArray();

// send toSendBytes

```

**读取bytes 的前两个字节**

```c#
Int16 len = BitConverter.ToInt16(info.buffer, 0);
```


**简单思路**

```c#
int bufferCount; // 记录当前

// receive

bufferCount += count; // 当前的数据

// deal data
public void DealData(ClientInfo info){
	if(bufferCount <= 2) return; //还没收齐，不应该处理
	Int16 len = BitConverter.ToInt16(info.buffer, 0);
	if(buffercount < 2 + len) return; //也没有收齐
	// 处理消息
	.....
	//处理 buffer 区域
	int start = 2 + len; //
	int count = bufferCount - start;
	Array.Copy(info.buffer, start, info.buffer, 0, count);
	bufferCount -= start;
	DealData(info);
}

// 此时beginReceive 的时候

BeiginReceive(info.buffer, bufferCount, 1024-bufferCount, 0, receiverCallBack);


```


## 大小端问题

BitConverter的问题

**解决**

```c#
if(!BitConverter.IsLittleEndian){
	buferr.Reverse();
}

// 手动
if(!BitConverter.IsLittleEndian){
	byte[] n = new byte[2];
	n[0] = buffer[1];
	n[1] = buffer[0];
	len = BitConverter.Toint16(n, 0);
}

```


## 使用websocket库进行开发


客户端 ： https://github.com/endel/NativeWebSocket
安装 ： https://github.com/endel/NativeWebSocket.git#upm

后端 ： fleck
安装 : https://www.nuget.org/packages/Fleck

protobuf: 序列化和反序列化文件
Json : 也需要学习

