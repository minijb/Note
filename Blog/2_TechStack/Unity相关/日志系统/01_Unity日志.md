
三种基础打印方式

```c#
Debug.Log("This is a log message.");
Debug.LogWarning("This is a warning message!");
Debug.LogError("This is an error message!");
```

点击定位对应 gameobject

> 注意 可以指向 prefab ！！！ 

```c#
GameObject go = new GameObject("go");
Debug.Log("Test", go);
```


**彩色打印**

`<color=#rbg颜色值>xxx</color>`

```c#
Debug.LogFormat("This is <color=#ff0000>{0}</color>", "red");
Debug.LogFormat("This is <color=#00ff00>{0}</color>", "green");
Debug.LogFormat("This is <color=#0000ff>{0}</color>", "blue");
Debug.LogFormat("This is <color=yellow>{0}</color>", "yellow");
```

**日志存储和上传**

```c#
using System.IO;
using System.Text;
using UnityEngine;

public class Main: MonoBehaviour
{
	// 使用StringBuilder来优化字符串的重复构造
    StringBuilder m_logStr = new StringBuilder();
    // 日志文件存储位置
    string m_logFileSavePath;

    void Awake()
    {
    	// 当前时间
        var t = System.DateTime.Now.ToString("yyyyMMddhhmmss");
        m_logFileSavePath = string.Format("{0}/output_{1}.log", Application.persistentDataPath, t);
        Debug.Log(m_logFileSavePath);
        Application.logMessageReceived += OnLogCallBack;
        Debug.Log("日志存储测试");
    }

    /// <summary>
    /// 打印日志回调
    /// </summary>
    /// <param name="condition">日志文本</param>
    /// <param name="stackTrace">调用堆栈</param>
    /// <param name="type">日志类型</param>
    private void OnLogCallBack(string condition, string stackTrace, LogType type)
    {
        m_logStr.Append(condition);
        m_logStr.Append("\n");
        m_logStr.Append(stackTrace);
        m_logStr.Append("\n");

        if (m_logStr.Length <= 0) return;
        if (!File.Exists(m_logFileSavePath))
        {
            var fs = File.Create(m_logFileSavePath);
            fs.Close();
        }
        using (var sw = File.AppendText(m_logFileSavePath))
        {
            sw.WriteLine(m_logStr.ToString());
        }
        m_logStr.Remove(0, m_logStr.Length);
    }
}

```

**日志上传**

使用 WWWFORM 或者  UnityWebRequest.Post

```c++
// 读取日志文件的字节流
byte[] ReadLogFile()
{
	byte[] data = null;
	
	using(FileStream fs = File.OpenRead("你的日志文件路径")) 
	{
		int index = 0;
		long len = fs.Length;
		data = new byte[len];
		// 根据你的需求进行限流读取
		int offset = data.Length > 1024 ? 1024 : data.Length;
		while (index < len) 
		{
			int readByteCnt = fs.Read(data, index, offset);
			index += readByteCnt;
			long leftByteCnt = len - index;
			offset = leftByteCnt > offset ? offset : (int)leftByteCnt;
		}
		Debug.Log ("读取完毕");
	}
	return data;
}

// 将日志字节流上传到web服务器
IEnumerator HttpPost(string url, byte[] data)
{
	WWWForm form = new WWWForm();
	// 塞入描述字段，字段名与服务端约定好
	form.AddField("desc", "test upload log file");
	// 塞入日志字节流字段，字段名与服务端约定好
	form.AddBinaryData("logfile", data, "test_log.txt", "application/x-gzip");
	// 使用UnityWebRequest
	UnityWebRequest request = UnityWebRequest.Post(url, form);
	var result = request.SendWebRequest();
    while (!result.isDone)
    {
        yield return null;
        //Debug.Log ("上传进度: " + request.uploadProgress);
    }
    if (!string.IsNullOrEmpty(request.error))
    {
        GameLogger.LogError(request.error);
    }
    else
    {
        GameLogger.Log("日志上传完毕, 服务器返回信息: " + request.downloadHandler.text);
    }
    request.Dispose();
}

```

https://blog.csdn.net/linxinfa/article/details/119280053