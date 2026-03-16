
[unity doc](https://docs.unity.cn/cn/2023.2/ScriptReference/Networking.UnityWebRequest.html)

**简单流程**

1. 使用静态函数如 `Get, Post, Put` 等创建一个经配置可通过 HTTP POST 向服务器发送表单数据的 UnityWebRequest。
2. 使用 **异步** 进行消息发送 `SendWebRequest` 开始通信
3.  异步的 等待  `isDone` 完成
4. 通过 变量 `downloadHandler` 获取下载数据

**常用属性**

- `result`  enum : 结果
- `error`  string  错误结果
- `timeout`  超时时间
- `reponseCode`  HTTP 响应码
- `downloadHandler/uploadHandler`  Send 之后只读， 可以提前设置回调函数
- `GetResponseHeader`   获取返回头
- `SendWebRequest`  开始通信
- `SetRequestHeader` 设置http头
## ch_unity_DownloadHandler

拥有对 [DownloadHandler](https://docs.unity.cn/cn/2023.2/ScriptReference/Networking.DownloadHandler.html) 对象的引用，该对象可管理此 [UnityWebRequest](https://docs.unity.cn/cn/2023.2/ScriptReference/Networking.UnityWebRequest.html) 从远程服务器接收的主体数据。

将此属性设置为 `null` 表示此 [UnityWebRequest](https://docs.unity.cn/cn/2023.2/ScriptReference/Networking.UnityWebRequest.html) 不考虑响应的主体数据；接收的所有主体数据将被忽略和丢弃。请参阅 [DownloadHandler](https://docs.unity.cn/cn/2023.2/ScriptReference/Networking.DownloadHandler.html) 对象的参考信息，以了解有关创建和使用 DownloadHandler 的更多信息。  
  
调用 [Send](https://docs.unity.cn/cn/2023.2/ScriptReference/Networking.UnityWebRequest.Send.html) 后将无法更改此属性。

**常用属性**

- GetProgress()  获取进度
- GetData() 获取信息
- GetText() 获取文本
- ReceiveData() 拿到服务器数据后的回调函数