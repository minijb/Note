
https://www.cnblogs.com/Can-daydayup/p/18824060

LINQ语言集成查询是一系列直接将查询功能集成到 C# 语言的技术统称

**特性**

- 强类型：编译时验证查询逻辑，减少运行时错误。
- 延迟执行：LINQ查询通常是延迟执行的，即查询表达式本身不会立即执行，直到实际遍历结果时才触发查询。使用 `ToList()`、`ToArray()`、`ToDictionary()`、`FirstOrDefault()`等方法可立即执行。
- 支持多种数据源：LINQ可以用于查询多种数据源，如`LINQ to Objects、LINQ to XML、LINQ to SQL、LINQ to Entities（Entity Framework）`等。

### 基本查询方法

- **Where**：用于过滤集合中的元素，通过一个谓词（返回布尔值的条件）筛选集合中的元素，生成一个仅包含满足条件元素的新序列。
- **Select**：用于将集合中的每个元素投影（转换）为新序列。
- **SelectMany**：用于将多个集合（嵌套集合，如集合的集合）`展平`为一个集合。


```c#
var femaleStudents = students.Where(s => s.StudentName == "时光者");
var studentNames = students.Select(s => s.StudentName);

// 使用SelectMany展平所有学生的课程列表
var allCourses = students.SelectMany(student => student.Courses).ToList();

// 输出所有课程的名称
foreach (var course in allCourses)
{
	Console.WriteLine(course.CourseName);
}
```

### 转换方法

- **ToList**：将实现了`IEnumerable<T>`接口的集合转换为一个`List<T>`类型的对象，属于将集合转换为特定类型列表的方法。
- **ToArray**：将一个实现了`IEnumerable<T>`接口的集合转换为一个数组，属于将集合转换为数组类型的方法。
- **ToDictionary**：将一个`IEnumerable<T>`集合转换为一个`Dictionary<TKey,TValue>`键值对集合（字典）的方法，注意 ToDictionary 要求键唯一，否则抛出异常。
- **ToLookup**：将一个`IEnumerable<T>`集合转换为一个泛型`Lookup<TKey,TElement>`，`Lookup<TKey,TElement>`一个一对多字典，用于将键映射到值的集合。


### 元素操作方法

- **First**：返回集合中的第一个元素。
- **FirstOrDefault**：返回集合中的第一个元素，如果集合中未找到该元素，则返回默认值。
- **Single**：返回集合中的单个元素，如果集合中未找到该元素或包含多个元素则抛出异常。
- **SingleOrDefault**：返回集合中的单个元素，如果集合中未找到该元素，则返回默认值；如果该集合中包含多个元素，此方法将引发异常。
- **Last**：返回集合中的最后一个元素。
- **LastOrDefault**：返回集合中的最后一个元素，如果集合中未找到该元素，则返回默认值。
- **ElementAt**：返回集合中指定索引处的元素。
- **ElementAtOrDefault**：返回集合中指定索引处的元素，如果索引超出范围则返回默认值。
- **DefaultIfEmpty**：如果集合为空，则返回一个包含默认值的集合。

### 排序方法

- **OrderBy**：用于对集合进行升序排序。
- **OrderByDescending**：用于对集合进行降序排序。
- **ThenBy**：按升序对集合中的元素执行后续排序。
- **ThenByDescending**：按降序对集合中的元素执行后续排序。

### 聚合方法

- **Count**：返回集合中的元素数量。
- **Sum**：返回集合中数值类型元素的和。
- **Average**：返回集合中数值类型元素的平均值。
- **Min**：返回集合中的最小值。
- **Max**：返回集合中的最大值。
- **Aggregate**：对集合进行自定义聚合操作。

### 集合操作方法

- **Distinct**：返回集合中的唯一元素（去除重复项）。
- **Union**：返回两个集合的并集（合并后去重）。
- **Intersect**：返回两个集合的交集（共有的唯一元素）。
- **Except**：返回在第一个集合中存在但不在第二个集合中存在的元素（取集合的差集）。
- **Concat**：连接两个集合，返回一个新的序列（保留所有元素，包括重复项）。

### 分组与连接方法

- **GroupBy**：对集合中的元素进行分组。
- **Join**：基于匹配键对两个集合的元素进行关联。
- **GroupJoin**：基于键值等同性将两个集合的元素进行关联，并对结果进行分组。


### 跳过与获取指定数量的元素（常用作分页）

- **Skip**：用于跳过集合中指定数量的元素，并返回剩余的元素序列。
- **Take**：用于从集合的开头获取指定数量的元素，并返回一个新的序列。

### 条件判断方法

- **All**：判断集合中的所有元素是否都满足条件。
- **Any**：判断集合中是否包含元素或存在元素满足指定条件。
- **Contains**：用于判断集合中是否包含指定的元素。

## 查询语法

LINQ提供了类似于SQL的查询语法，允许开发者以几乎相同的方式对不同类型的数据源进行查询。查询语法使用from、where、select、orderby等关键字。

```c#
var querySyntaxResult = from student in students
						where student.ClassID == 101
						orderby student.StudentName ascending
						select student;

Console.WriteLine("查询语法结果:");
foreach (var student in querySyntaxResult)
{
	Console.WriteLine($"{student.StudentName}, ClassID: {student.ClassID}");
}
```


**查询关键字：**

- **from：** 指定数据源和范围变量（类似于迭代变量）。
- **where：** 基于由逻辑 AND 和 OR 运算符（&& 或 ||）分隔的一个或多个布尔表达式筛选源元素。
- **select：** 指定执行查询时，所返回序列中元素的类型和形状。
- **group：** 根据指定的密钥值对查询结果分组。
- **into：** 提供可作为对 join、group 或 select 子句结果引用的标识符（简单理解用于将配对的结果收集到一个临时序列）。
- **orderby：** 根据元素类型的默认比较器对查询结果进行升序或降序排序。
- **join：** 基于两个指定匹配条件间的相等比较而联接两个数据源（简单理解根据指定的键将两个序列中的元素配对）。
- **let：** 引入范围变量，在查询表达式中存储子表达式结果。
- **in：** join子句中的上下文关键字。
- **on：** join子句中的上下文关键字。
- **equals：** join子句中的上下文关键字。
- **by：** group 子句中的上下文关键字。
- **ascending：** orderby子句中的上下文关键字。
- **descending：** orderby子句中的上下文关键字。

## 方法语法

方法语法也称为扩展方法语法，使用点号“.”和一系列扩展方法来构建查询。

```c#
var methodSyntaxResult = students
						.Where(student => student.ClassID == 101)
						.OrderBy(student => student.StudentName)
						.ToList();


Console.WriteLine("方法语法结果:");
foreach (var student in methodSyntaxResult)
{
	Console.WriteLine($"{student.StudentName}, ClassID: {student.ClassID}");
}
```

## 混合查询和方法语法

```c#
var mixedResult = (from student in students
				   where student.ClassID == 101
				   where student.Courses.Any(course => course.CourseName == "数学")
				   orderby student.StudentName ascending
				   select student)
		   .Take(2)
		   .ToList();

// 输出结果
Console.WriteLine("混合查询结果:");
foreach (var student in mixedResult)
{
	Console.WriteLine($"{student.StudentName}, ClassID: {student.ClassID}");
}
```