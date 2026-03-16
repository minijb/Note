---
tags:
  - Csharp
---
## 序列化

**数据类**

```c#
public class Lesson1Test
{
    [XmlElement("testPublic123123")]//---- 改名字
    public int testPublic;
    private int testPrivate;
    protected int testProtected;
    internal int testInternal;

    public string testPUblicStr;

    public int testPro { get; set; }

    public Lesson1Test2 testClass = new Lesson1Test2();

    public int[] arrayInt;
    [XmlArray("IntList")] //---- 改名字
    [XmlArrayItem("Int32")]
    public List<int> listInt;
    public List<Lesson1Test2> listItem;

    //不支持字典
    //public Dictionary<int, string> testDic = new Dictionary<int, string>() { { 1, "123" } };
}


public class Lesson1Test2
{
    [XmlAttribute("Test1")] // 变为属性
    public int test1 = 1;
    [XmlAttribute()]
    public float test2 = 1.1f;
    [XmlAttribute()]
    public bool test3 = true;
}
```


### 序列化一个类

```c#
//1.第一步准备一个数据结构类-------------------------------------------------
Lesson1Test lt = new Lesson1Test();
//2.进行序列化
//  关键知识点
//  XmlSerializer 用于序列化对象为xml的关键类
//  StreamWriter 用于存储文件  
//  using 用于方便流对象释放和销毁

//第一步：确定存储路径-------------------------------------------------
string path = Application.persistentDataPath + "/Lesson1Test.xml";
print(Application.persistentDataPath);
//第二步：结合 using知识点 和 StreamWriter这个流对象 来写入文件
// 括号内的代码：写入一个文件流 如果有该文件 直接打开并修改 如果没有该文件 直接新建一个文件
// using 的新用法 括号当中包裹的声明的对象 会在 大括号语句块结束后 自动释放掉 
// 当语句块结束 会自动帮助我们调用 对象的 Dispose这个方法 让其进行销毁
// using一般都是配合 内存占用比较大 或者 有读写操作时  进行使用的 
using ( StreamWriter stream = new StreamWriter(path) )
{
	//第三步：进行xml文件序列化-------------------------------------------------
	XmlSerializer s = new XmlSerializer(typeof(Lesson1Test));
	//这句代码的含义 就是通过序列化对象 对我们类对象进行翻译 将其翻译成我们的xml文件 写入到对应的文件中
	//第一个参数 ： 文件流对象
	//第二个参数: 想要备翻译 的对象
	//注意 ：翻译机器的类型 一定要和传入的对象是一致的 不然会报错
	s.Serialize(stream, lt);
}
```



序列化流程
1.有一个想要保存的类对象
2.使用XmlSerializer 序列化该对象
3.通过StreamWriter 配合 using将数据存储 写入文件
注意：
1.只能序列化公共成员
2.不支持字典序列化
3.可以通过特性修改节点信息 或者设置属性信息
4.Stream相关要配合using使用



## 反序列化

```c#
#region 知识点一 判断文件是否存在
string path = Application.persistentDataPath + "/Lesson1Test.xml";
if( File.Exists(path) )
{
	#region 知识点二 反序列化
	//关键知识
	// 1.using 和 StreamReader
	// 2.XmlSerializer 的 Deserialize反序列化方法

	//读取文件---------------------------------
	using (StreamReader reader = new StreamReader(path))
	{
		//产生了一个 序列化反序列化的翻译机器
		XmlSerializer s = new XmlSerializer(typeof(Lesson1Test));
		Lesson1Test lt = s.Deserialize(reader) as Lesson1Test;
	}
	#endregion
}
#endregion
```


1.判断文件是否存在 File.Exists
2.文件流获取 StreamReader reader = new StreamReader(path)
3.根据文件流 XmlSerializer通过Deserialize反序列化 出对象

注意：List对象 如果有默认值 反序列化时 不会清空 会往后面添加


## IXmlSerializable 接口

C# 的XmlSerializer 提供了可拓展内容 
可以让一些不能被序列化和反序列化的特殊类能被处理
让特殊类继承 IXmlSerializable 接口 实现其中的方法即可

```c#
public class TestLesson3 : IXmlSerializable
{
    public int test1;
    public string test2;

    //返回结构----------------------------------
    public XmlSchema GetSchema()
    {
        return null;
    }

    //反序列化时 会自动调用的方法----------------------------------
    public void ReadXml(XmlReader reader)
    {
        //在里面可以自定义反序列化 的规则
        //1.读属性
        //this.test1 = int.Parse(reader["test1"]);
        //this.test2 = reader["test2"];

        //2.读节点
        //方式一
        //reader.Read();//这时是读到的test1节点
        //reader.Read();//这时是读到的test1节点包裹的内容
        //this.test1 = int.Parse(reader.Value);//得到当前内容的值
        //reader.Read();//这时读到的是尾部包裹节点
        //reader.Read();//这时是读到的test2节点
        //reader.Read();//这时是读到的test2节点包裹的内容
        //this.test2 = reader.Value;
        //方式二
        //while(reader.Read())
        //{
        //    if( reader.NodeType == XmlNodeType.Element )
        //    {
        //        switch (reader.Name)
        //        {
        //            case "test1":
        //                reader.Read();
        //                this.test1 = int.Parse(reader.Value);
        //                break;
        //            case "test2":
        //                reader.Read();
        //                this.test2 = reader.Value;
        //                break;
        //        }
        //    }
        //}

        //3.读包裹元素节点
        XmlSerializer s = new XmlSerializer(typeof(int));
        XmlSerializer s2 = new XmlSerializer(typeof(string));
        //跳过根节点
        reader.Read();
        reader.ReadStartElement("test1");
        test1 = (int)s.Deserialize(reader);
        reader.ReadEndElement();

        reader.ReadStartElement("test2");
        test2 = s2.Deserialize(reader).ToString();
        reader.ReadEndElement();
    }

    //序列化时 会自动调用的方法----------------------------------
    public void WriteXml(XmlWriter writer)
    {
        //在里面可以自定义序列化 的规则

        //如果要自定义 序列化的规则 一定会用到 XmlWriter中的一些方法 来进行序列化
        //1.写属性
        //writer.WriteAttributeString("test1", this.test1.ToString());
        //writer.WriteAttributeString("test2", this.test2);

        //2.写节点
        //writer.WriteElementString("test1", this.test1.ToString());
        //writer.WriteElementString("test2", this.test2);

        //3.写包裹节点
        XmlSerializer s = new XmlSerializer(typeof(int));
        writer.WriteStartElement("test1");
        s.Serialize(writer, test1);
        writer.WriteEndElement();

        XmlSerializer s2 = new XmlSerializer(typeof(string));
        writer.WriteStartElement("test2");
        s2.Serialize(writer, test2);
        writer.WriteEndElement();
    }
}
```

```c#
TestLesson3 t = new TestLesson3();
t.test2 = "123";
string path = Application.persistentDataPath + "/TestLesson3.xml";
//序列化
using (StreamWriter writer = new StreamWriter(path))
{
	//序列化"翻译机器"
	XmlSerializer s = new XmlSerializer(typeof(TestLesson3));
	//在序列化时  如果对象中的引用成员 为空 那么xml里面是看不到该字段的
	s.Serialize(writer, t);
}
//反序列化
using (StreamReader reader = new StreamReader(path))
{
	//序列化"翻译机器"
	XmlSerializer s = new XmlSerializer(typeof(TestLesson3));
	TestLesson3 t2 = s.Deserialize(reader) as TestLesson3;
}
```


## dic 支持 序列化

```c#
public class SerizlizerDictionary<TKey, TValue> : Dictionary<TKey, TValue>, IXmlSerializable
{
    public XmlSchema GetSchema()
    {
        return null;
    }

    //自定义字典的 反序列化 规则
    public void ReadXml(XmlReader reader)
    {
        XmlSerializer keySer = new XmlSerializer(typeof(TKey));
        XmlSerializer valueSer = new XmlSerializer(typeof(TValue));

        //要跳过根节点
        reader.Read();
        //判断 当前不是元素节点 结束 就进行 反序列化
        while (reader.NodeType != XmlNodeType.EndElement)
        {
            //反序列化键
            TKey key = (TKey)keySer.Deserialize(reader);
            //反序列化值
            TValue value = (TValue)valueSer.Deserialize(reader);
            //存储到字典中
            this.Add(key, value);
        }
    }

    //自定义 字典的 序列化 规则
    public void WriteXml(XmlWriter writer)
    {
        XmlSerializer keySer = new XmlSerializer(typeof(TKey));
        XmlSerializer valueSer = new XmlSerializer(typeof(TValue));

        foreach (KeyValuePair<TKey, TValue> kv in this)
        {
            //键值对 的序列化
            keySer.Serialize(writer, kv.Key);
            valueSer.Serialize(writer, kv.Value);
        }
    }
}


```


```c#
public class TestLesson4
{
    public int test1;

    public SerizlizerDictionary<int, string> dic;
}
```


```c#
TestLesson4 tl4 = new TestLesson4();
//tl4.dic = new SerizlizerDictionary<int, string>();
//tl4.dic.Add(1, "123");
//tl4.dic.Add(2, "234");
//tl4.dic.Add(3, "345");
string path = Application.persistentDataPath + "/TestLesson4.xml";
//using(StreamWriter writer = new StreamWriter(path))
//{
//    XmlSerializer s = new XmlSerializer(typeof(TestLesson4));
//    s.Serialize(writer, tl4);
//}

using (StreamReader reader = new StreamReader(path))
{
	XmlSerializer s = new XmlSerializer(typeof(TestLesson4));
	tl4 = s.Deserialize(reader) as TestLesson4;
}


```