

[[C Sharp IList  IReadOnlyList]]


List 默认扩容为2的整数倍


**报错**

Contract.Ensures

```c#
int IArray.Add(Object value)
{
    // Returns the index in which an item was inserted.
    Contract.Ensures(Contract.Result<int>() >= -1);
    Contract.Ensures(Contract.Result<int>() < ((IArray)this).Count);
    return default(int);
}
```


List 删除 --- Array.Copy

Insert 也是同理 --- Array.Copy

ToArray : 复制一个新数组，有大量内存分配

