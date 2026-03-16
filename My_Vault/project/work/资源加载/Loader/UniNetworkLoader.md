
使用接口 [[IUniAssetLoader]]

Priority，ForcePriority

**时间** ： RetryCount

**属性** ： 
缓存 ： CanCacheMem，CanCacheLocal
Http ：HttpStatusCode， Url ， ResponseRawData (byte)
m_ReqeustPath, m_Host, BuildId
本地 ： m_IsLocalFile, m_LocalSaveing， m_SaveLocalLockObject

**Dictionary**  : Ip2HostMap, Host2IpMap

## 方法

**GetCachePath** : 获得缓存path --- 主要为md5 + filename
**WriteBytesToLocal** ： 将文件内容通过二进制写入到本地

**网络Loader有两个Cache** ： 
1. 本地 localCache ： 写入到本地文件目录在 [[CachePath]]
2. RawData : 内存中的Cache。

**OnComplete** : ProcessLoaded 处理结束问题
