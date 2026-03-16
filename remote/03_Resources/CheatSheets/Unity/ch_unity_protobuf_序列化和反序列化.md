
```c#
// 序列化
MemoryStream ms = new MemoryStream();
res = new byte[len];
ms.SetLength(0);
msg.WriteTo(ms);
ms.Position = 0;
ms.Read(res, 0, len);

// 反序列化

{具体的类}.Parser.ParseFrom

```


将 enum 和 protobuf 序列化 


```c#
// 使用反射得到类并调用反序列化方法
public static bool TryDecodeMsg(byte[] input, out Type type, out object obj)
{
	int enum_num = (int)BitConverter.ToInt16(input.AsSpan(0, 2).ToArray());

	type = Type.GetType("Protomsg." + Enum.GetName(typeof(KCP_MessageNum), enum_num));
	if (type == null)
	{
		type = Type.GetType("Messages." + Enum.GetName(typeof(KCP_MessageNum), enum_num));
	}

	obj = null;
	if (type == null)
	{
		return false;
	}

	PropertyInfo propertyInfo = type.GetProperty("Parser");
	MessageParser messageParser = null;
	if (propertyInfo != null)
	{
		messageParser = (MessageParser)propertyInfo.GetValue(messageParser);
	}

	obj = messageParser.ParseFrom(input.AsSpan(2, input.Length - 2).ToArray());

	if (obj == null) return false;
	else if (obj.GetType() == type)
		return true;
	else
	{
		obj = null;
		type = null;
		Debug.LogError("[ PROTO ] 字节流解析失败");
		return false;
	}
}
```


**对应的 enum**

```c#
    public enum KCP_MessageNum
    {
        None = 0,
        HeartBeat = 3000, //  心跳消息
        ClientVerifyReq = 3033, //  连接验证消息                            ---------------------------------------
        ClientVerifySucceedRet = 3034, //  ClientVerifySucceedRet 验证成功返回消息 -----------------------------------
        ClientVerifyFailedRet = 3035, //  ClientVerifyFailedRet 验证失败返回消息 --------------------------------
        EntityRPCReq = 3030,
        AddMatchQueueReq = 4600, //  加入匹配队列请求
        AddMatchQueueRet = 4601, //  加入匹配队列返回
        CancelMatchQueueReq = 4602, //  取消匹配请求
        CancelMatchQueueRet = 4603, //  取消匹配返回
        MatchSuccessNtf = 4604, // 匹配成功游戏 推送客户端

// =============================================================================
        SndSelectReq = 4606, // 发送选择角色
        SndLoadReq = 4609,
        SndLoadRet = 4610, //  通知加载进度
        EnterGameReq = 4204, // 进入战斗
        EnterGameRet = 4205, // 返回战斗
        GameOverReq = 4206, // 对局结束
        GameOverRet = 4207, //

    }
```



## Protobuf 打包工具类


**处理message**



```c#
public static MemoryStream ms = new MemoryStream();

public static string getMsgTypeName(byte[] input)
{
	string res = Enum.GetName(typeof(KCP_MessageNum), BitConverter.ToInt32(input));
	if (res == null) Debug.LogError($"[PROTO] 解析失败， 没有对应类型的命令编号");
	return res;
}

public static bool TryDecodeMsg(byte[] input, out Type type, out object obj)
{
	int enum_num = (int)BitConverter.ToInt16(input.AsSpan(0, 2).ToArray());

	type = Type.GetType("Protomsg." + Enum.GetName(typeof(KCP_MessageNum), enum_num));
	if (type == null)
	{
		type = Type.GetType("Messages." + Enum.GetName(typeof(KCP_MessageNum), enum_num));
	}

	obj = null;
	if (type == null)
	{
		return false;
	}

	PropertyInfo propertyInfo = type.GetProperty("Parser");
	MessageParser messageParser = null;
	if (propertyInfo != null)
	{
		messageParser = (MessageParser)propertyInfo.GetValue(messageParser);
	}

	obj = messageParser.ParseFrom(input.AsSpan(2, input.Length - 2).ToArray());

	if (obj == null) return false;
	else if (obj.GetType() == type)
		return true;
	else
	{
		obj = null;
		type = null;
		Debug.LogError("[ PROTO ] 字节流解析失败");
		return false;
	}
}


public static bool TryEncodeMsg<T>(T msg, out byte[] res) where T : IMessage
{

	int len = msg.CalculateSize();
	res = new byte[len];

	try
	{
		ms.SetLength(0);
		msg.WriteTo(ms);
		ms.Position = 0;
		ms.Read(res, 0, len);
	}
	catch (Exception e)
	{
		Debug.LogError("[PROTO] 序列化失败" + typeof(T));
		res = null;
		return false;
	}

	return true;
}
public static byte[] EncoderMsg<T>(T msg) where T : IMessage
{
	int len = msg.CalculateSize();
	byte[] res = new byte[len];

	try
	{
		ms.SetLength(0);
		msg.WriteTo(ms);
		ms.Position = 0;
		ms.Read(res, 0, len);
	}
	catch (Exception e)
	{
		Debug.LogError("[PROTO] 序列化失败" + typeof(T));
		return null;
	}

	return res;
}
```


**处理 package**

```c#
public static bool TryGetPackageEnum(byte[] input, out KCP_MessageNum num)
{
	int index = BitConverter.ToInt16(input.AsSpan(4, 2).ToArray());
	num = KCP_MessageNum.None;
	try
	{
		num = (KCP_MessageNum)Enum.ToObject(typeof(KCP_MessageNum), index);
	}
	catch (Exception e)
	{
		return false;
	}

	return true;
}

public static bool TryDecodePackage<T>(byte[] input, out T t) where T : class
{
	t = null;
	if (TryDecodePackage(input, out Type type, out object obj))
	{
		if (type == typeof(T))
		{
			t = (T)obj;
			return true;
		}
	}
	return false;
}

public static byte[] CreatePackage<T>(T msg) where T : IMessage
{
	// 内部 协议 字节数组
	if (!TryEncodeMsg<T>(msg, out byte[] tempBody)) return null;

	int msgID = 0;

	foreach (var enumItem in Enum.GetValues(typeof(KCP_MessageNum)))
	{
		if (enumItem.ToString() == typeof(T).Name)
		{
			msgID = (int)enumItem;
		}
	}

	if (msgID == 0)
	{
		Debug.LogError("[PROTO] 没有对应协议的 enum");
		return null;
	}

	// 外层协议
	EntityRPCReq entityRPCReq = new EntityRPCReq()
	{
		EntityID = 0,
		SrvType = 10,
		PRCName = typeof(T).Name,
		MsgContent = ByteString.CopyFrom(tempBody),
		MsgID = (uint)msgID
	};
	// Debug.Log(typeof(T).Name); 
	// Debug.Log($"{BitConverter.ToString(tempBody)}");
	if (!TryEncodeMsg<EntityRPCReq>(entityRPCReq, out byte[] body)) return null;


	// 打包头部
	byte[] header = GetBodyLength(body.Length);
	KCP_MessageNum messageNum = (KCP_MessageNum)Enum.Parse(typeof(KCP_MessageNum), typeof(EntityRPCReq).Name);
	byte[] n = BitConverter.GetBytes((short)messageNum);
	byte[] res = Tool.ConcatBytes(header, n, body);

	// Debug.Log(BitConverter.ToString(res));

	return res;
}

public static byte[] CreateConnectVerifyPackage(ClientVerifyReq req)
{
	if (!TryEncodeMsg<ClientVerifyReq>(req, out byte[] body)) return null;
	byte[] header = GetBodyLength(body.Length);
	KCP_MessageNum messageNum = (KCP_MessageNum)Enum.Parse(typeof(KCP_MessageNum), typeof(ClientVerifyReq).Name);
	byte[] n = BitConverter.GetBytes((short)messageNum);
	byte[] res = Tool.ConcatBytes(header, n, body);
	return res;
}

public static byte[] GetBodyLength(int len)
{
	if (len < 0)
	{
		Debug.LogError("[PROTO] 非法包体长度");
		return null;
	}

	len += 2;
	byte[] res = BitConverter.GetBytes(len);
	return res;
}
```