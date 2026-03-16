
[Enum.GetName](https://learn.microsoft.com/zh-cn/dotnet/api/system.enum.getname?view=net-9.0)

```c#
// 从 enum 获取名称
string res = Enum.GetName(typeof(KCP_MessageNum), BitConverter.ToInt32(input));
// 将 string 转化为类型
Type type = Type.GetType("xxx") ; // full name


// Type 转化为 string
type.Name
type.FullName


// 获取 enum 对应的值
(int)enum.xxx

```


## Reflaction+enum

```c#
using System;
namespace HelloWorldApplication
{
	public enum EJobType
    {
        客服 = 1, 业务员 = 2, 财务 = 3, 经理 = 4
    }
   class HelloWorld
   {
      static void Main(string[] args)
      {
		  Type jobType = typeof(EJobType);
		  Array enumItems = Enum.GetValues(jobType);
            foreach (var enumItem in enumItems)
            {
                int value = (int)enumItem; // 得到 值
                string text = enumItem.ToString(); // 得到名称
				Console.WriteLine(value);
			}
         /* Write C# code in this online editor and run it. */
         
         Console.ReadKey();
      }
   }
}

FieldInfo[] fields = jobType.GetFields(BindingFlags.Static | BindingFlags.Public);//
foreach (var field in fields)
{
   string text =  field.Name;
   object value = field.GetRawConstantValue();
}
```