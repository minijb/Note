
积累 ： [[UniNetworkLoader]]

四个徐方法 ： 

`SetHeader SetPostData SetMethod`

HTTPRequest : http 请求 

**SetHeader** : 通过 key : value 在 http 请求中添加必要的值.
**SetMethod** : 设置 一个 http 的 method type ： `GET POST HEAD`
**SetPostData** : 设置 BestHttpRequest 的 `RawData`  类型为 type
**Progress** -- BestHttp 有一个 event ： `OnUploadProgress, OnDownloadProgress` 绑定这个接口可以得到 进度。
**OnComplete** : 接入 HTTPRequest 的 callback event ， 参数 : `Request, Reponse` 处理 reponse 的返回值。 将 Response 的Rawdata 写入到 父类中的 RawData 中

**额外的流程**

**OnConfigRequest** ： 发送请求前的处理
**OnSendWebRequest** : 发送请求

**BeiginLoader** : 就是开始发送请求 ： 主要会预先配置必要的 header, method, .....
**OnComplete** :  如果失败会进行 retry 判断， 如果retry失效，同时接受报错，则发出错误信息。 **response 的值写入 RawData** ， 调用父类的 OnComplete -- 也就是  `processLoaded` 


## UniHttpLoader 另一个版本 基于 UnityRequest

流程类似

****

PS ： 感觉如果想要加入加密功能可以添加一个对象(策略模式)，在里面添加。
 
