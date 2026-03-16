#TODO 

https://learn.microsoft.com/zh-cn/dotnet/csharp/linq/get-started/introduction-to-linq-queries


```c#
// The Three Parts of a LINQ Query:
// 1. Data source.
int[] numbers = [ 0, 1, 2, 3, 4, 5, 6 ];

// 2. Query creation.
// numQuery is an IEnumerable<int>
var numQuery = from num in numbers
               where (num % 2) == 0
               select num;

// 3. Query execution.
foreach (int num in numQuery)
{
    Console.Write("{0,1} ", num);
}
```


https://learn.microsoft.com/zh-cn/dotnet/csharp/linq/get-started/query-expression-basics


对于此源序列，查询可能会执行三种操作之一：

- 检索元素的子集以生成新序列，而不修改各个元素。 然后，查询可能以各种方式对返回的序列进行排序或分组，如下面的示例所示（假定 `scores` 是 `int[]`）：
    
    C#复制
    
    ```
    IEnumerable<int> highScoresQuery =
        from score in scores
        where score > 80
        orderby score descending
        select score;
    ```
    
- 如前面的示例所示检索元素的序列，但是将它们转换为新类型的对象。 例如，查询可能仅从数据源中的某些客户记录中检索出姓氏。 或者可以检索完整记录，然后用于构造其他内存中对象类型甚至是 XML 数据，再生成最终的结果序列。 下面的示例演示从 `int` 到 `string` 的投影。 请注意 `highScoresQuery` 的新类型。
    
    C#复制
    
    ```
    IEnumerable<string> highScoresQuery2 =
        from score in scores
        where score > 80
        orderby score descending
        select $"The score is {score}";
    ```
    
- 检索有关源数据的单独值，如：
    
    - 与特定条件匹配的元素数。
        
    - 具有最大或最小值的元素。
        
    - 与某个条件匹配的第一个元素，或指定元素集中特定值的总和。 例如，下面的查询从 `scores` 整数数组返回大于 80 的分数的数量：
        
        C#复制
        
        ```
        var highScoreCount = (
            from score in scores
            where score > 80
            select score
        ).Count();
        ```
        
        在前面的示例中，请注意在调用 [Enumerable.Count](https://learn.microsoft.com/zh-cn/dotnet/api/system.linq.enumerable.count) 方法之前，在查询表达式两边使用了括号。 也可以通过使用新变量存储具体结果。
        
        C#复制
        
        ```
        IEnumerable<int> highScoresQuery3 =
            from score in scores
            where score > 80
            select score;
        
        var scoreCount = highScoresQuery3.Count();
        ```
        

在上面的示例中，查询在 `Count` 调用中执行，因为 `Count` 必须循环访问结果才能确定 `highScoresQuery` 返回的元素数。



https://learn.microsoft.com/zh-cn/dotnet/csharp/linq/get-started/query-expression-basics

