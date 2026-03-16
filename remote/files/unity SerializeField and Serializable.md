
- `[SerializeField]` 表示将原本不会被序列化的私有变量和保护变量变成可以被序列化的，那么它们在下次读取的值就是你上次赋值的值。
- `[Serializable]` 指示可序列化的类或结构
	- 具有 `Serializable` 属性的自定义结构
	- 如果想要自定义的类显示在inspector中我们就需要 先对类进行 Serializable， 随后对属性进行 SerializeField