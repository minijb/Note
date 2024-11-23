---
tags:
  - unity
  - socket
---
## 简单聊天室

### 服务端

变量

```c#
public static Socket socket; // 本地 socket
public static List<ClientInfo> clients = new List<ClientInfo>(); // 存储远程的socket

public class ClientInfo // 存储结构
{
	public Socket socket;
	public byte[] buffer = new byte[1024];
	public ClientInfo(Socket socket)
	{
		this.socket = socket;
	}
}
```


```c#
public static void Main(string[] argv)
{
	socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
	socket.Bind(new IPEndPoint(IPAddress.Any, 10010));
	socket.Listen(0);

	socket.BeginAccept(AcceptCallback, socket); // 异步的使用 accept 函数  --- 默认的accept 是阻塞的
	Console.ReadLine(); // 防止自动结束
}


```


两个回调函数

```c#
    public static void AcceptCallback(IAsyncResult result)
    {
        try
        {
            Socket socket = (Socket)result.AsyncState;// 得到目标socket
            Socket client = socket.EndAccept(result); // 停止接受
            ClientInfo clientInfo = new ClientInfo(client); //创建一个 client info 并存储
            clients.Add(clientInfo);
            client.BeginReceive(clientInfo.buffer, 0, 1024, 0, ReceiveCallback, clientInfo); //开始接受
            socket.BeginAccept(AcceptCallback, socket); // 继续执行 accept
        }
        catch (System.Exception e)
        {
            Console.WriteLine(e.ToString());
        }
    }

    public static void ReceiveCallback(IAsyncResult result)
    {
        try
        {
            ClientInfo info = (ClientInfo)result.AsyncState;
            int count = info.socket.EndReceive(result);

            // if(count == 0)

            Console.WriteLine("" + count);

            foreach (var c in clients)
            {
                c.socket.Send(info.buffer, 0, count, 0);
            }

            info.socket.BeginReceive(info.buffer, 0, 1024, 0, ReceiveCallback, info);
        }
        catch (System.Exception e)
        {
            Console.WriteLine(e.ToString());
        }
    }

```



### 客户端

```c#
public class NetWorkManager : MonoBehaviour
{
    public static Socket socket;
    public static byte[] buffer = new byte[1024];

    public static void Connect()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket.Connect(new IPEndPoint(IPAddress.Parse("116.198.200.12"), 10010));
        socket.BeginReceive(buffer, 0, 1024, 0, ReceiveCallBack, socket);
    }

    public static void Send(string message)
    {
        socket.Send(System.Text.Encoding.UTF8.GetBytes(message));
    }

    public static void ReceiveCallBack(IAsyncResult result)
    {
        Socket socket = (Socket)result.AsyncState;

        int count = socket.EndReceive(result);

        GameManager.instance.actions.Enqueue(() => // 使用action 队列实现 利用线程控制组件
        {
            UIManager.instance.contentText.text += "\n" + "Server:" + System.Text.Encoding.UTF8.GetString(buffer, 0, count);
        });
        socket.BeginReceive(buffer, 0, 1024, 0, ReceiveCallBack, socket);
    }
}
```


## 连接数据库

安装包

```sh
dotnet add package MySqlConnector --version 2.3.7
```


连接 mysql

```c#
public class DBManager{

    public static MySqlConnection mysql = new MySqlConnection();
    public static bool Connect(string database, string server,int port, string username, string password){
        mysql.ConnectionString = string.Format("database={0};server={1};port={2};user={3};password={4}", database, server, port, username, password);
        try{
            mysql.Open();
            return true;
        }catch(Exception e){
            Console.WriteLine(e.Message);
            return false;
        }
    }

    public static bool Register(string user, string password){
        if(!IsSafeString(user) || !IsSafeString(password)) return false;
        if(IsAccountExist(user)) return false;
        try{
            string str = string.Format("insert into Account set Name = '{0}', Password = '{1}'", user, password);
            MySqlCommand cmd = new MySqlCommand(str, mysql);
            MySqlDataReader reader = cmd.ExecuteReader();
            reader.Close();
            return true;
        }catch(Exception e){
            Console.WriteLine(e.Message);
            return false;
        }
    }

    public static bool Login(string user, string password){
        if(!IsSafeString(user) || !IsSafeString(password)) return false;
        if(!IsAccountExist(user)) return false;
        try{
            string str = string.Format("select * from Account where Name = '{0}' and Password = '{1}'", user, password);
            MySqlCommand cmd = new MySqlCommand(str, mysql);
            MySqlDataReader reader = cmd.ExecuteReader();
            bool hasData = reader.HasRows;
            reader.Close();
            return hasData;
        }catch(Exception e){
            Console.WriteLine(e.Message);
            return false;
        }
    }

    public static bool IsAccountExist(string user){
        if(!IsSafeString(user)) return false;

        try{
            string str = string.Format("select * from Account where name = '{0}'", user);
            MySqlCommand cmd = new MySqlCommand(str, mysql);
            MySqlDataReader reader = cmd.ExecuteReader();
            bool hasData = reader.HasRows;
            reader.Close();
            return hasData;
        }catch(Exception e){
            Console.WriteLine(e.Message);
            return false;
        }


    } 

    public static bool IsSafeString(string str){
        if(string.IsNullOrEmpty(str)) return false;
        if(str.Length > 255) return false;

        return !Regex.IsMatch(str, @"[-|;|,|.|\/|\(|\)|\{|\}|%|@|\*|\'|]");
        
    }

    // public static void Main(){
    //     Connect("Socket", "127.0.0.1", 3306, "Alice", "123456");
    //     Console.WriteLine( Login("two", "100"));
    // }


}
```


之后需要改的

```c#
public static void ReceiveCallback(IAsyncResult result)
{
	try
	{
		ClientInfo info = (ClientInfo)result.AsyncState;
		int count = info.socket.EndReceive(result);

		if(count == 0){
			info.socket.Close();
			clients.Remove(info);
			Console.WriteLine("one client closed");
			return;
		}
		string message = System.Text.Encoding.UTF8.GetString(info.buffer, 0, count);
		Console.WriteLine(message);
		string[] argv = message.Split('|');

		if(argv[0] == "Register"){
			if(DBManager.Register(argv[1], argv[2])){
				info.socket.Send(System.Text.Encoding.UTF8.GetBytes("注册成功"));
			}else{
				info.socket.Send(System.Text.Encoding.UTF8.GetBytes("注册失败"));
			}
		}else if(argv[0] == "Login"){
			if(DBManager.Login(argv[1], argv[2])){
				info.socket.Send(System.Text.Encoding.UTF8.GetBytes("登录成功"));
			}else{
				info.socket.Send(System.Text.Encoding.UTF8.GetBytes("登录失败"));
			}
		}


		info.socket.BeginReceive(info.buffer, 0, 1024, 0, ReceiveCallback, info);
	}
	catch (System.Exception e)
	{
		Console.WriteLine(e.ToString());
	}

}
```


## 五子棋

自定义协议


```c#
[Serializable]
public class ProtoBase
{
    public string name;
}
[Serializable]
public class PlayProto:ProtoBase
{
    public int x;
    public int y;
    public int color;
}
[Serializable]
public class ReadyProto:ProtoBase
{

}
public class ColorProto:ProtoBase
{
    public int color;
}
public class MessageProto:ProtoBase
{
    public string message;
}
public class WinProto:ProtoBase
{
    public int color;
}
```


**有了协议我们需要有 encoder 和 decoder 来解析协议**

```c#
    private static ProtoBase Decode(string str) 
    {
        var args = str.Split('|');
        return args[0] switch
        {
            "color" => JsonUtility.FromJson<ColorProto>(args[1]),
            "play" => JsonUtility.FromJson<PlayProto>(args[1]),
            "message" => JsonUtility.FromJson<MessageProto>(args[1]),
            "ready" => JsonUtility.FromJson<ReadyProto>(args[1]),
            "win" => JsonUtility.FromJson<WinProto>(args[1]),
            _ => null,
        };
    }

    private static string Encode(object o)
    {
        return JsonUtility.ToJson(o);
    }


    public static void Send(string message)
    {
        socket.Send(System.Text.Encoding.UTF8.GetBytes(message));
    }
    public static void Send(ProtoBase proto)
    {
        socket.Send(System.Text.Encoding.UTF8.GetBytes(proto.name + "|" + Encode(proto)));
    }
```


此时我们的 receive 回调函数就是

```c#
public static void ReceiveCallback(IAsyncResult result)
{
	Socket socket = (Socket)result.AsyncState;
	int count = socket.EndReceive(result);

	string content = System.Text.Encoding.UTF8.GetString(buffer, 0, count);
	ProtoBase proto = Decode(content);
	Debug.Log("Receive");
	if (proto is MessageProto)
		GameManager.Instance.ReceiveMessage(proto as MessageProto);
	else if (proto is ColorProto)
		GameManager.Instance.ReceiveColor(proto as ColorProto);
	else if (proto is PlayProto)
		GameManager.Instance.ReceivePlay(proto as PlayProto);
	else if (proto is ReadyProto)
		GameManager.Instance.ReceiveReady(proto as ReadyProto);
	else if (proto is WinProto)
		GameManager.Instance.ReceiveWin(proto as WinProto);
	socket.BeginReceive(buffer, 0, 1024, 0, ReceiveCallback, socket);
}
```


游戏逻辑

```c#
    public void SendPlay(Cross cross)
    {
        PlayProto proto = new PlayProto() { name = "play", color = (color == GameStatus.Black ? 0 : 1), x = (int)cross.transform.position.x, y = (int)cross.transform.position.y };
        NetworkManager.Send(proto);
    }
    
    public void SendReady()
    {
        NetworkManager.Send(new ReadyProto() { name = "ready" });
    }
    
    public void ReceivePlay(PlayProto playProto)
    {
        Debug.Log("play proto");
        actions.Enqueue(() =>
        Instantiate(chessPrefab, new Vector3(playProto.x, playProto.y), Quaternion.identity, chessContainer).GetComponent<Chess>().chess.color = new Color(playProto.color, playProto.color, playProto.color));
        if (playProto.color == 0)
            status = GameStatus.White;
        else
            status = GameStatus.Black;
    }
    
    public void ReceiveMessage(MessageProto messageProto)
    {
        Debug.Log("message proto");
        actions.Enqueue(() => UIManager.Instance.contentText.text +=
        "\n" + messageProto.message);
    }
    
    public void ReceiveColor(ColorProto colorProto)
    {
        Debug.Log("color proto");
        actions.Enqueue(() =>
        {
            color = (colorProto.color == 1) ? GameStatus.Black : GameStatus.White;
        });
    }
    
    public void ReceiveReady(ReadyProto readyProto)
    {
        Debug.Log("ready proto");
        status = GameStatus.Black;
    }
    
    public void ReceiveWin(WinProto winProto)
    {
        status = GameStatus.End;
        actions.Enqueue(() => UIManager.Instance.contentText.text +="\n系统：游戏结束！"+
       ((winProto.color == 0) ? "黑棋" : "白棋") + "获胜！");
    }
    
    private void OnApplicationQuit()
    {
        NetworkManager.Close();
    }
```


### 后端协议

```c#
public class ProtoBase
{
    public string? name { get; set; }
}
public class PlayProto : ProtoBase
{
    public int x { get; set; }
    public int y { get; set; }
    public int color { get; set; }
}
public class ReadyProto : ProtoBase
{

}
public class ColorProto : ProtoBase
{
    public int color { get; set; }
}
public class MessageProto : ProtoBase
{
    public string? message { get; set; }
}
public class WinProto : ProtoBase
{
    public int color { get; set; }
}
```


**协议的解码**


```c#
    private static ProtoBase Decode(string str)
    {
        var args = str.Split('|');
        ProtoBase proto = null;
        switch (args[0])
        {
            case "ready":
                proto = JsonSerializer.Deserialize<ReadyProto>(args[1]);
                break;
            case "play":
                proto = JsonSerializer.Deserialize<PlayProto>(args[1]);
                break;
            case "message":
                proto = JsonSerializer.Deserialize<MessageProto>(args[1]);
                break;
            default:
                Console.WriteLine("Decode Wrong Arguments");
                break;
        }
        return proto;
    }
    private static byte[] Encode(ProtoBase proto)
    {
        string res = proto.name;
        //res = res + "|" + JsonSerializer.Serialize(proto);
        switch (res)
        {
            case "color":
                res = res + "|" + JsonSerializer.Serialize<ColorProto>(proto as ColorProto);
                break;
            case "play":
                res = res + "|" + JsonSerializer.Serialize<PlayProto>(proto as PlayProto);
                break;
            case "message":
                res = res + "|" + JsonSerializer.Serialize<MessageProto>(proto as MessageProto);
                break;
            case "ready":
                res = res + "|" + JsonSerializer.Serialize<ReadyProto>(proto as ReadyProto);
                break;
            case "win":
                res = res + "|" + JsonSerializer.Serialize<WinProto>(proto as WinProto);
                break;
            default:
                Console.WriteLine("Encode Wrong Arguments");
                break;
        }
        Console.WriteLine("Encode: " + res);
        return System.Text.Encoding.UTF8.GetBytes(res);
    }
```

**回调函数**

```c#
    public static async void ReceiveCallback(IAsyncResult result)
    {
        try
        {
            ClinetInfo info = (ClinetInfo)result.AsyncState;
            int count = info.socket.EndReceive(result);
            if (count == 0)
            {
                colorTaken[info.index] = false;
                info.socket.Close();
                clients.Remove(info);
                Console.WriteLine("one client left");
                return;
            }
            string jsonString = System.Text.Encoding.UTF8.GetString(info.buffer, 0, count);
            Console.WriteLine(jsonString);
            ProtoBase proto = Decode(jsonString);

            if (proto is MessageProto)
                ReceiveMessage(proto as MessageProto);
            else if (proto is PlayProto)
                ReceivePlay(proto as PlayProto);
            else if (proto is ReadyProto)
                ReceiveReady(info, proto as ReadyProto);
            info.socket.BeginReceive(info.buffer, 0, 1024, 0, ReceiveCallback, info);
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }
    }
```


**接受逻辑**

```c#
    private static void ReceivePlay(PlayProto playProto)
    {
        foreach (var c in clients)
            c.socket.Send(Encode(playProto));
        map[playProto.x, playProto.y] = playProto.color;
        CheckWin(playProto);
        if (checkWinFlag)
        {
            foreach (var c in clients)
                c.socket.Send(Encode(new WinProto() { name = "win", color = playProto.color }));
        }
    }
    private static async void ReceiveReady(ClinetInfo info, ReadyProto readyProto)
    {
        Random r = new Random();
        int v = r.Next(0, 2);
        if (!colorTaken[v])
        {
            colorTaken[v] = true;
            info.socket.Send(Encode(new ColorProto() { name = "color", color = v }));

            info.socket.Send(Encode(new MessageProto() { name = "message", message = "系统: 你已经就绪，请等待另一位玩家。" }));

            info.index = v;
        }
        else if (!colorTaken[1 - v])
        {
            colorTaken[1 - v] = true;
            info.socket.Send(Encode(new ColorProto() { name = "color", color = 1 - v }));

            info.socket.Send(Encode(new MessageProto() { name = "message", message = "系统: 你已经就绪，请等待另一位玩家。" }));

            info.index = 1 - v;
        }
        else
        {
            Console.WriteLine("Ready Wrong Arguments");
        }
        await Task.Delay(200);
        if (colorTaken[0] && colorTaken[1])
        {
            foreach (var c in clients)
            {
                c.socket.Send(Encode(readyProto));
                await Task.Delay(200);
                c.socket.Send(Encode(new MessageProto() { name = "message", message = "系统: 所有玩家已就位，对局开始。" }));
            }
        }
    }
    private static void ReceiveMessage(MessageProto messageProto)
    {
        foreach (var c in clients)
            c.socket.Send(Encode(messageProto));
    }
    private static void CheckWin(PlayProto proto)
    {
        checkWinFlag = false;
        DFS(0, proto.color, proto.x, proto.y, proto.x, proto.y, 1);
        DFS(1, proto.color, proto.x, proto.y, proto.x, proto.y, 1);
        DFS(2, proto.color, proto.x, proto.y, proto.x, proto.y, 1);
        DFS(3, proto.color, proto.x, proto.y, proto.x, proto.y, 1);
    }
```