
使用步骤

1. 初始化组件
	1. UDP端口
	2. IKcpCallback interface  实体化
	3. KCP 对象
2.  Out -> 使用 UDP 发送
3.  开一个线程，使用 UDP 接受信息，使用 `kcp_input` 存入信息
4. 使用  `TryRecive` 拿到接收的信息
5. 调用 `_update` 刷新 kcp 

[粘包问题](https://github.com/skywind3000/kcp/issues/238)
- 默认使用包模式， 不需要处理粘包
- 流模式需要

**一个简单的 kcp Session**

```c#
public class KCPSession
{

	private SimpleSegManager.Kcp kcp;
	private KCPHandle _kcpHandle;
	private UdpClient _udpClient;
	private IPEndPoint _targetEndPoint;
	private CancellationTokenSource _cts;
	private CancellationToken _ct;

	public Action<byte[]> OnReceivePack;


	public void InitSession()
	{
		_udpClient = new UdpClient(0);
		_kcpHandle = new KCPHandle();
		_cts = new CancellationTokenSource();
		_ct = _cts.Token;
	}


	public void ClientInit(IPEndPoint target, int userID)
	{
		this._targetEndPoint = target;

		_kcpHandle.Out = (Memory<byte> buffer) =>
		{
			byte[] toSend = buffer.ToArray();
			if (_udpClient != null)
			{
				_udpClient.Send(toSend, toSend.Length, _targetEndPoint);
			}
		};

		_kcpHandle.Recv = (byte[] buffer) =>
		{
			// Debug.Log(BitConverter.ToString(buffer));
			OnReceivePack(buffer);
		};
		kcp = new SimpleSegManager.Kcp((uint)userID, _kcpHandle);
		kcp.NoDelay(1, 10, 2, 1);
		kcp.WndSize(64, 64);
		kcp.SetMtu(512);

		Task.Run(_update, _ct);
		Task.Run(_Receive, _ct);
	}


	// kcp 内部更新
	private async void _update()
	{
		while (true)
		{
			DateTime now = DateTime.UtcNow;
			if (_ct.IsCancellationRequested)
			{
				break;
			}
			else
			{
				kcp.Update(now);
				int len;
				while ((len = kcp.PeekSize()) > 0)
				{
					var buffer = new byte[len];
					if (kcp.Recv(buffer) >= 0)
					{
						_kcpHandle.Receive(buffer);
					}
				}
				await Task.Delay(10);
			}
		}
	}

	private async void _Receive()
	{
		UdpReceiveResult receive;
		while (true)
		{
			if (_ct.IsCancellationRequested)
			{
				break;
			}

			receive = await _udpClient.ReceiveAsync();

			if (!_targetEndPoint.Equals(receive.RemoteEndPoint)) continue;

			kcp.Input(receive.Buffer.AsSpan());
		}
	}

	public void SendPack(byte[] input)
	{
		kcp.Send(input);
	}
}
```