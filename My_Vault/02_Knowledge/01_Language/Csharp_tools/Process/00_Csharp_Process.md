---
title: C# Process 进程管理
date: 2026-03-16
tags:
  - csharp
  - process
  - system
type: language
aliases:
  Process进程
description: C# Process进程管理相关知识
draft: false
---

title: Csharp Process
date: 2026-03-16
tags:
  - knowledge
  - csharp
type: language
aliases:
  -
description: using (Process myProcess = new Process())
draft: false
---

# Csharp Process

## 两种启动进程的方式

### 1. 使用对象

```c#
try
{
    using (Process myProcess = new Process())
    {
        myProcess.StartInfo.UseShellExecute = false;
        // You can start any process, HelloWorld is a do-nothing example.
        myProcess.StartInfo.FileName = "C:\\HelloWorld.exe";
        myProcess.StartInfo.CreateNoWindow = true;
        myProcess.Start();
        // This code assumes the process you are starting will terminate itself.
        // Given that it is started without a window so you cannot terminate it
        // on the desktop, it must terminate itself or you can do it programmatically
        // from this application using the Kill method.
    }
}
catch (Exception e)
{
    Console.WriteLine(e.Message);
}
```

### 2. 使用Process本身

```c#
class MyProcess
{
    // Opens the Internet Explorer application.
    void OpenApplication(string myFavoritesPath)
    {
        // Start Internet Explorer. Defaults to the home page.
        Process.Start("IExplore.exe");

        // Display the contents of the favorites folder in the browser.
        Process.Start(myFavoritesPath);
    }

    // Opens urls and .html documents using Internet Explorer.
    void OpenWithArguments()
    {
        // url's are not considered documents. They can only be opened
        // by passing them as arguments.
        Process.Start("IExplore.exe", "www.northwindtraders.com");

        // Start a Web page using a browser associated with .html and .asp files.
        Process.Start("IExplore.exe", "C:\\myPath\\myFile.htm");
        Process.Start("IExplore.exe", "C:\\myPath\\myFile.asp");
    }

    // Uses the ProcessStartInfo class to start new processes,
    // both in a minimized mode.
    void OpenWithStartInfo()
    {
        ProcessStartInfo startInfo = new ProcessStartInfo("IExplore.exe");
        startInfo.WindowStyle = ProcessWindowStyle.Minimized;

        Process.Start(startInfo);

        startInfo.Arguments = "www.northwindtraders.com";

        Process.Start(startInfo);
    }

    static void Main()
    {
        // Get the path that stores favorite links.
        string myFavoritesPath =
            Environment.GetFolderPath(Environment.SpecialFolder.Favorites);

        MyProcess myProcess = new MyProcess();

        myProcess.OpenApplication(myFavoritesPath);
        myProcess.OpenWithArguments();
        myProcess.OpenWithStartInfo();
    }
}
```

## 注解

Process 此类信息包括线程集、加载的模块 (.dll 和 .exe 文件) ，以及性能信息，例如进程正在使用的内存量。

此类型实现 IDisposable 接口。 在使用完类型后，您应直接或间接释放类型。 若要直接释放类型，请在 try/finally 块中调用其 Dispose 方法。 若要间接释放类型，请使用 using（在 Csharp 中）或 Using（在 Visual Basic 中）等语言构造。 有关详细信息，请参阅接口文档中的“使用实现 IDisposable 的对象”部分 IDisposable 。

## ProcessStartInfo

指定进程启动时候的一组值

https://learn.microsoft.com/zh-cn/dotnet/api/system.diagnostics.processstartinfo?view=net-8.0

常用属性:

- Arguments
- CreateNoWindow  是都在新窗口中启动进程的值
- Environment
- FileName 启动的引用程序或者文档
- RedirectStandardError/Input/Output
- StandardError/Input/OutputEncoding
- UseShellExecute 获取活设置是否使用进程的值
- WorkingDirectory 工作目录

## 应用 ： Csharp 运行 pyhton 文件

```c#
public static void RunPythonDirectly(string filePath, string args)
{
	var processStartInfo = new ProcessStartInfo()
	{
		FileName = "python",
		Arguments = $"{filePath} {args}",
		UseShellExecute = true,
		WorkingDirectory = Path.Combine(Application.dataPath, "../../")
	};

	var process = new Process()
	{
		StartInfo = processStartInfo,
	};

	process.Start();
	process.WaitForExit();
}
```