---
tags:
  - Csharp
---
## XML

树形结构

属性语法 ： `<a name="xxx" age='a'>hello</a>`

- 元素节点 ： a
- 属性 ：name, age
- 节点信息 ： hello


## C#读取xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Root>
	<name>唐老狮</name>
	<age>18</age>
	<Item id="1" num="10"/>
	<Friend>
		<name>小明</name>
		<age>8</age>
	</Friend>
	<Friend>
		<name>小红</name>
		<age>10</age>
	</Friend>
</Root>
```


1.读取xml --- 得到字符串/使用文件名


```c#
XmlDocument xml = new XmlDocument();
//通过XmlDocument读取xml文件 有两个API
//1.直接根据xml字符串内容 来加载xml文件
//存放在Resorces文件夹下的xml文件加载处理
TextAsset asset = Resources.Load<TextAsset>("TestXml");
print(asset.text);
//通过这个方法 就能够翻译字符串为xml对象
xml.LoadXml(asset.text);

//2.是通过xml文件的路径去进行加载
xml.Load(Application.streamingAssetsPath + "/TestXml.xml");
```


2. 读取内容




```c#
//节点信息类
//XmlNode 单个节点信息类
//节点列表信息
//XmlNodeList 多个节点信息类

// -------------------------获得节点------------------------------------
//获取xml当中的根节点
XmlNode root = xml.SelectSingleNode("Root");
//再通过根节点 去获取下面的子节点
XmlNode nodeName = root.SelectSingleNode("name");

// -------------------------获得包裹信息------------------------------------
//如果想要获取节点包裹的元素信息 直接 .InnerText
print(nodeName.InnerText);

XmlNode nodeAge = root.SelectSingleNode("age");
print(nodeAge.InnerText);

XmlNode nodeItem = root.SelectSingleNode("Item");


// -------------------------获得属性信息------------------------------------
//第一种方式 直接 中括号获取属性信息
print(nodeItem.Attributes["id"].Value);
print(nodeItem.Attributes["num"].Value);
//第二种方式 
print(nodeItem.Attributes.GetNamedItem("id").Value);
print(nodeItem.Attributes.GetNamedItem("num").Value);


// -------------------------得到重名节点------------------------
//这里是获取 一个节点下的同名节点的方法
XmlNodeList friendList = root.SelectNodes("Friend");

//遍历方式一：迭代器遍历
foreach (XmlNode item in friendList)
{
    print(item.SelectSingleNode("name").InnerText);
    print(item.SelectSingleNode("age").InnerText);
}
//遍历方式二：通过for循环遍历
//通过XmlNodeList中的 成员变量 Count可以得到 节点数量
for (int i = 0; i < friendList.Count; i++)
{
	print(friendList[i].SelectSingleNode("name").InnerText);
	print(friendList[i].SelectSingleNode("age").InnerText);
}
```


**总结**

```c#
	//1.读取XML文件
	//XmlDocument xml = new XmlDocument();
	//读取文本方式1-xml.LoadXml(传入xml文本字符串)
	//读取文本方式2-xml.Load(传入路径)

	//2.读取元素和属性
	//获取单个节点 : XmlNode node = xml.SelectSingleNode(节点名)
	//获取多个节点 : XmlNodeList nodeList = xml.SelectNodes(节点名)

	//获取节点元素内容：node.InnerText
	//获取节点元素属性：
	//1.item.Attributes["属性名"].Value
	//2.item.Attributes.GetNamedItem("属性名").Value

	//通过迭代器遍历或者循环遍历XmlNodeList对象 可以获取到各单个元素节点
```


## 存储xml


1.Resources 可读 不可写 打包后找不到  ×
2.Application.streamingAssetsPath 可读 PC端可写 找得到  ×
3.Application.dataPath 打包后找不到  ×
4.Application.persistentDataPath 可读可写找得到   √


```c#
//关键类 XmlDocument 用于创建节点 存储文件
//关键类 XmlDeclaration 用于添加版本信息
//关键类 XmlElement 节点类

//存储有5步
//1.创建文本对象-----------------------------------------
XmlDocument xml = new XmlDocument();

//2.添加固定版本信息-----------------------------------------
//这一句代码 相当于就是创建<?xml version="1.0" encoding="UTF-8"?>这句内容
XmlDeclaration xmlDec = xml.CreateXmlDeclaration("1.0", "UTF-8", "");
//创建完成过后 要添加进入 文本对象中
xml.AppendChild(xmlDec);

//3.添加根节点-----------------------------------------
XmlElement root = xml.CreateElement("Root");
xml.AppendChild(root);

//4.为根节点添加子节点-----------------------------------------
//加了一个 name子节点
XmlElement name = xml.CreateElement("name");
name.InnerText = "唐老狮";
root.AppendChild(name);

XmlElement atk = xml.CreateElement("atk");
atk.InnerText = "10";
root.AppendChild(atk);

XmlElement listInt = xml.CreateElement("listInt");
for (int i = 1; i <= 3; i++)
{
	XmlElement childNode = xml.CreateElement("int");
	childNode.InnerText = i.ToString();
	listInt.AppendChild(childNode);
}
root.AppendChild(listInt);

XmlElement itemList = xml.CreateElement("itemList");
for (int i = 1; i <= 3; i++)
{
	XmlElement childNode = xml.CreateElement("Item");
	//添加属性-----------------------------------------
	childNode.SetAttribute("id", i.ToString());
	childNode.SetAttribute("num", (i * 10).ToString());
	itemList.AppendChild(childNode);
}
root.AppendChild(itemList);

//5.保存-----------------------------------------
xml.Save(path);
#endregion
```


## 修改xml

```c#
#region 知识点三 修改xml文件
//1.先判断是否存在文件----------------------
if( File.Exists(path) )
{
	//2.加载后 直接添加节点 移除节点即可-----------------------------------------
	XmlDocument newXml = new XmlDocument();
	newXml.Load(path);

	//修改就是在原有文件基础上 去移除 或者添加
	//移除----------------------
	XmlNode node;// = newXml.SelectSingleNode("Root").SelectSingleNode("atk");
	//这种是一种简便写法 通过/来区分父子关系
	node = newXml.SelectSingleNode("Root/atk");
	//得到自己的父节点
	XmlNode root2 = newXml.SelectSingleNode("Root");
	//移除子节点方法
	root2.RemoveChild(node);

	//添加节点
	XmlElement speed = newXml.CreateElement("moveSpeed");
	speed.InnerText = "20";
	root2.AppendChild(speed);

	//改了记得存
	newXml.Save(path);
}
```