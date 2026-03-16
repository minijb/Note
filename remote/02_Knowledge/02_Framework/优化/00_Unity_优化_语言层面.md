
1. 使用集合的时候需要提前设置大小
比如 List，Dictionary

2. 引用连续!=内存连续

```c#
class A
{
	public int a;
	public float b;
	public bool c;
}

A[] arrayA = xxxx;

class C
{
	private static C _instance;
	public static C instance
	{
		get xxx
	}
	
	public int[] a = xxx;
	public float[] b = xxx;
	public bool[] c= xxx;
}

C c = C.instance;
```

arrayA 只是引用连续
C存储的地方，内存是连续的可以更好的利用缓存



