---
tags:
  - unity
---



**优点是可以更深层次地分析用户代码的性能热点，避免定位到大致模块后，无法继续往下分析，只能通过其他方式（如代码审查）继续优化的尴尬**

```c#
Profiler.BeginSample("curve");
Profiler.EndSample();
```

简单封装

```c#
using UnityEngine;
using System;
public class ProfilerSample {
    public static bool EnableProfilerSample = true;
    public static bool EnableFormatStringOutput = true;// 是否允许BeginSample的代码段名字使用格式化字符串（格式化字符串本身会带来内存开销）
    public static void BeginSample(string name) {
#if ENABLE_PROFILER
        if(EnableProfilerSample){
           Profiler.BeginSample(name);
        }
#endif
    }
    public static void BeginSample(string formatName, params object[] args) {
#if ENABLE_PROFILER
        if(EnableProfilerSample) {
           // 必要时很有用，但string.Format本身会产生GC Alloc，需要慎用
           if (EnableFormatStringOutput)
               Profiler.BeginSample(string.Format(formatName, args));
           else
               Profiler.BeginSample(formatName);
        }
#endif
    }
    public static void EndSample() {
#if ENABLE_PROFILER
        if(EnableProfilerSample) {
           Profiler.EndSample();
        }
#endif
    }
}
```
