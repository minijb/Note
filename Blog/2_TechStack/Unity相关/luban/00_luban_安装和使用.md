
## Unity

1. clone luban_example 并复制 demo
2. 使用 git 的方式安装 package  https://github.com/focus-creative-games/luban_unity.git


https://blog.csdn.net/SmillCool/article/details/113751711


Luban 加载

1. 使用 github 安装 luban 插件
2. 直接加载内容

```c#
Tables tables = new Tables(LoadTable);

private JArray LoadTable(string tableName)
{
	TextAsset textAsset = Resources.Load<TextAsset>($"ResExcel/JsonData/{tableName}");
	return JArray.Parse(textAsset.text);
}
```



需要注意的是  一次会加载多个 table ！！！

