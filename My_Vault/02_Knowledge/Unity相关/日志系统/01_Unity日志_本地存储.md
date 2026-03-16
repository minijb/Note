

https://www.yxtown.com/my/course/70

```c#
public class LogData
{
    public string log;
    public string trace;
    public LogType type;
}
public class LogHelper : MonoBehaviour
{
    /// <summary>
    /// 文件写入
    /// </summary>
    private StreamWriter mStreamWriter;
    /// <summary>
    /// 日志数据队列
    /// </summary>  
    ConcurrentQueue<LogData> mConCurrentQueue = new ConcurrentQueue<LogData>();

    /// <summary>
    /// 工作信号事件
    /// </summary>
    readonly ManualResetEvent mManualResetEvent = new ManualResetEvent(false); // false 初始化

    private string mNowTime { get { return DateTime.Now.ToString("yyyy:MM:dd HH:mm:ss"); } }

    private bool mThreadRunning = false;


    public void InitLogFileModule(string savePath, string logFileName)
    {
        string logFilePath = Path.Combine(savePath, logFileName);
        //子线程使用
        // 主线程使用
        Debug.Log("logFilePath :" + logFilePath);
        mStreamWriter = new StreamWriter(logFilePath);
        Application.logMessageReceivedThreaded += OnLogMessageReceivedThreaded;
        mThreadRunning = true;
        Thread fileThread = new Thread(FileLogThread);

        fileThread.Start();
    }


    // 推出的时候调用
    public void OnApplicationQuit()
    {
        Application.logMessageReceivedThreaded -= OnLogMessageReceivedThreaded;
        mThreadRunning = false;
        mManualResetEvent.Reset();
        mStreamWriter.Close();
        mStreamWriter = null;
    }

    private void OnLogMessageReceivedThreaded(string condition, string stackTrace, LogType type)
    {

        mConCurrentQueue.Enqueue(new LogData()
        {
            log = mNowTime + " " + condition,
            trace = stackTrace,
            type = type
        });
        mManualResetEvent.Set();
        // mManualResetEvent.Set();  // 设置信号，表示线程需要工作 //表示有信号了，通知WaitOne不再阻塞
        // mManualResetEvent.Reset(); // 充值信号， 表示线程是需要工作
        // mManualResetEvent.WaitOne(); // 线程进入等待， 并进行阻塞
    }

    private void FileLogThread()
    {
        while (mThreadRunning)
        {
            mManualResetEvent.WaitOne();
            if (mStreamWriter == null) break;


            LogData data = null;

            while (!mConCurrentQueue.IsEmpty && mConCurrentQueue.TryDequeue(out data))
            {
                if (data.type == LogType.Log)
                {
                    mStreamWriter.Write("Log >>> ");
                    mStreamWriter.Write(data.log);
                    mStreamWriter.Write("\n");
                    mStreamWriter.Write(data.trace);
                }
                else if (data.type == LogType.Warning)
                {
                    mStreamWriter.Write("Warning >>> ");
                    mStreamWriter.Write(data.log);
                    mStreamWriter.Write("\n");
                    mStreamWriter.Write(data.trace);
                }
                else if (data.type == LogType.Error)
                {

                    mStreamWriter.Write("Error >>> ");
                    mStreamWriter.Write(data.log);
                    mStreamWriter.Write("\n");
                    mStreamWriter.Write(data.trace);

                }
                mStreamWriter.Write("\r\n");
            }

            mStreamWriter.Flush();// 保存使stream 生效
            mManualResetEvent.Reset();
            Thread.Sleep(1);
        }
    }
}

```


编译提出

**使用宏编译**

```c#
    [Conditional("OPEN_LOG")]
    public static void InitLog(LogConfig _cfg = null)
    {
        if (cfg == null) cfg = new LogConfig();
        else cfg = _cfg;

        if (cfg.flag_SaveLog)
        {
            GameObject logObj = new GameObject("LogHelper");
            GameObject.DontDestroyOnLoad(logObj);
            LogHelper helper = logObj.AddComponent<LogHelper>();
            helper.InitLogFileModule(cfg.LogFileSavePath, cfg.LogFileName);
        }
    }

	[Conditional("OPEN_LOG")]
    public static void LogGreen(object obj)
    {
        ColorLog(obj, LogColor.Green);
    }
    [Conditional("OPEN_LOG")]
    public static void LogBlue(object obj)
    {
        ColorLog(obj, LogColor.Blue);
    }
    [Conditional("OPEN_LOG")]
    public static void LogRed(object obj)
    {
        ColorLog(obj, LogColor.Red);
    }
    [Conditional("OPEN_LOG")]
    public static void LogDarkBlue(object obj)
    {
        ColorLog(obj, LogColor.DarkBlue);
    }
    
public class LogSystem : MonoBehaviour
{
    void Start()
    {
#if OPEN_LOG
        Debugger.InitLog(new LogConfig());
        Debugger.Log("log");
        Debugger.LogWarning("LogWarning");
        Debugger.LogError("LogError");
        Debugger.ColorLog("ColorLog", LogColor.Purple);
        Debugger.LogRed("LogRed");
        Debugger.LogGreen("LogGreen");
#else
        Debug.unityLogger.logEnabled = false;
#endif
    }


```


此时  只有加入对应的宏才会打包对应的方法。（排除对应的方法和调用）

