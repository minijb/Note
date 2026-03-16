
```c#
namespace System.Collections
{
    // 摘要:
    //     定义所有非泛型集合的大小、枚举器和同步方法。
    [ComVisible(true)]
    public interface ICollection : IEnumerable
    {
        // 摘要:
        //     获取 System.Collections.ICollection 中包含的元素数。
        //
        // 返回结果:
        //     System.Collections.ICollection 中包含的元素数。
        int Count { get; }
        //
        // 摘要:
        //     获取一个值，该值指示是否同步对 System.Collections.ICollection 的访问（线程安全）。
        //
        // 返回结果:
        //     如果对 System.Collections.ICollection 的访问是同步的（线程安全），则为 true；否则为 false。
        bool IsSynchronized { get; }
        //
        // 摘要:
        //     获取一个可用于同步对 System.Collections.ICollection 的访问的对象。
        //
        // 返回结果:
        //     可用于同步对 System.Collections.ICollection 的访问的对象。
        object SyncRoot { get; }
 
        // 摘要:
        //     从特定的 System.Array 索引处开始，将 System.Collections.ICollection 的元素复制到一个 System.Array
        //     中。
        //
        // 参数:
        //   array:
        //     作为从 System.Collections.ICollection 复制的元素的目标位置的一维 System.Array。System.Array
        //     必须具有从零开始的索引。
        //
        //   index:
        //     array 中从零开始的索引，将在此处开始复制。
        //
        // 异常:
        //   System.ArgumentNullException:
        //     array 为 null。
        //
        //   System.ArgumentOutOfRangeException:
        //     index 小于零。
        //
        //   System.ArgumentException:
        //     array 是多维的。- 或 -源 System.Collections.ICollection 中的元素数目大于从 index 到目标 array
        //     末尾之间的可用空间。
        //
        //   System.ArgumentException:
        //     源 System.Collections.ICollection 的类型无法自动转换为目标 array 的类型。
        void CopyTo(Array array, int index);
    }
}
```