---
tags:
  - unity
---

使用 sproto 协议，做的简单 客户端。

RpcClient ： 网络管理
UniNetworkSession : 自定义 本地 Session  --- 继承 UniBinaryStream
**UniNetworkTransport** : 使用 TcpClient 进行连接

## UniNetworkSession

简单来说就是将 package 中的内容写入到 writebuffer 中 然后发送

WriteProtoPackage 调用者

```c#
public void WriteMessagePackage(IUniProtoMessagePackage package,bool signPackage)  
{  
    BeginWrite();  
    var data = package.Encode(); // 编码 
    WriteData(data,0,data.Length);    // 根据编码写入到 writebuffer 
    if (signPackage)  
    {        
	    var sign = UniSprotoHelper.SignData(data, 3);  
        WriteData(sign,0,sign.Length);  
    }  
    int pos = WriteEnd;  
    WriteInt32(0);  
    var session = package.Session;  
    UniSprotoHelper.PackLuaInt(WriteBuffer,  pos, (uint)session, false, 4, session < 0);  
    EndWrite();  
}

// 防止沾包
public virtual void BeginWrite()  
{  
    WriteEnd = WritePosition = SendEnd;  
    CheckWrite(2);  
    WriteEnd += 2;  
}

public void WriteData(byte[] data, int offset, int size)  
{  
    CheckWrite(size);  
    System.Array.Copy(data, offset, WriteBuffer, WriteEnd, size);  
    WriteEnd += size;  
}
```


WriteEnd ， WritePosition ， SendEnd 这些参数进行数据传递

```c#
//使用新线程进行循环
private void ThreadTickLoop(object obj)
{
	while (fdClient != null && this.State == TransportState.Message && tickInThread)
	{
		TickMessageState();
		Thread.Sleep(10);
	}
}
//TickMessageState
//在Update 中进行读取
private void TickMessageState()
{
	try
	{
		if (fdClient.Client.Poll(0, SelectMode.SelectRead))
		{
			OnRead?.Invoke();
		}
		if (fdClient.Client.Poll(0, SelectMode.SelectWrite))
		{
			OnWrite?.Invoke();
			
		}
		
	}

//Update

case TransportState.Message:  
{  
	if (!tickInThread) TickMessageState();  
	break;  
}
```


