
### 1. 多个 byte 数据拼接

```c#
public static byte[] ConcatBytes(params byte[][] sourceBytesArray)
{
	int allLength = sourceBytesArray.Sum(o => o.Length);
	byte[] res = new byte[allLength];
	for (int i = 0; i < sourceBytesArray.Length; i++)
	{
		int copyToIndex = GetCopyToIndex(sourceBytesArray, i);
		sourceBytesArray[i].CopyTo(res, copyToIndex);
	}

	return res;
}

public static int GetCopyToIndex(byte[][] sourceBytesArray, int index)
{
	if (index == 0)
	{
		return 0;
	}
	return sourceBytesArray[index - 1].Length + GetCopyToIndex(sourceBytesArray, index - 1);
}
```