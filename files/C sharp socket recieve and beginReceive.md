---
tags:
  - Csharp
  - socket
---
## 同步调用

同步接收是最简单直接的方式，它使用Socket类的Receive方法来接收数据。这种方法在接收数据时会阻塞调用线程，直到数据接收完成或超时。

```c#
Socket socket = ... // 假设已经创建并连接了Socket
byte[] buffer = new byte[1024]; // 接收缓冲区
int received = socket.Receive(buffer); // 阻塞调用，直到接收到数据
```

## 异步调用

为了解决同步接收中的线程阻塞问题，可以使用异步接收。Socket类提供了BeginReceive和EndReceive方法来实现基于APM（Asynchronous Programming Model）模式的异步接收。


```c#
Socket socket = ... // 假设已经创建并连接了Socket
byte[] buffer = new byte[1024]; // 接收缓冲区
IAsyncResult asyncResult = socket.BeginReceive(buffer, 0, buffer.Length, 0, out SocketError errorCode, new AsyncCallback(ReceiveCallback), socket);
 
// 异步回调方法
private static void ReceiveCallback(IAsyncResult ar)
{
    Socket socket = (Socket)ar.AsyncState;
    int received = socket.EndReceive(ar, out SocketError errorCode);
    // 处理接收到的数据...
    // 可以继续调用BeginReceive进行下一次异步接收
}
```

使用BeginReceive开始异步接收后，当数据到达时，会调用提供的回调函数（在这个例子中是ReceiveCallback）。在回调函数中，可以使用EndReceive来获取接收到的数据，并进行处理。这种方式允许单个线程处理多个Socket连接，提高了应用程序的伸缩性。

## 基于事件的异步接收（使用SocketAsyncEventArgs）

```c#
Socket socket = ... // 假设已经创建并连接了Socket
SocketAsyncEventArgs args = new SocketAsyncEventArgs();
args.SetBuffer(new byte[1024], 0, 1024); // 设置接收缓冲区
args.Completed += new EventHandler<SocketAsyncEventArgs>(OnReceiveCompleted); // 注册完成事件处理程序
 
// 开始异步接收操作，如果返回true，则表示操作是异步的，将在完成后触发Completed事件；如果返回false，则表示操作已经同步完成。
if (!socket.ReceiveAsync(args))
{
    ProcessReceive(args); // 如果同步完成，直接处理接收结果（这在实际应用中很少见）
}
 
// 异步接收完成事件处理程序
private void OnReceiveCompleted(object sender, SocketAsyncEventArgs e)
{
    if (e.SocketError == SocketError.Success)
    {
        // 处理接收到的数据...
        // 可以继续调用ReceiveAsync进行下一次异步接收
        if (!e.AcceptSocket.ReceiveAsync(e))
        {
            ProcessReceive(e); // 如果同步完成，直接处理（同样很少见）
        }
    }
    else
    {
        // 处理错误情况...
    }
}
 
private void ProcessReceive(SocketAsyncEventArgs e)
{
    // 实际处理接收数据的逻辑...
}
```

在这种模式下，当数据到达时，会触发Completed事件，并在事件处理程序中处理接收到的数据。与BeginReceive/EndReceive相比，这种方式避免了显式地管理IAsyncResult对象，并且通常具有更好的性能。它是构建高性能、高伸缩性网络应用程序的推荐方式。