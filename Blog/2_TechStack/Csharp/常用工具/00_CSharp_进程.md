
- Process 来启动一个进程
- ProcessStarInfo 来更好的为一个进程提供初始的值 --- 可以附加很多信息

```c#
var psi = new System.Diagnostics.ProcessStartInfo
{
	FileName = "powershell",
	Arguments = $"-NoProfile -NonInteractive -Command \"{psCommand}\"",
	UseShellExecute = false,
	RedirectStandardOutput = true,
	RedirectStandardError = true,
	CreateNoWi
	ndow = true
};
```

