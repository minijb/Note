## UniModule 

1. Module 是 一个 monobehavior
2. 虚函数回调列表
   1. 初始化 + 释放
   2. 进入 + 推出
   3. 资源加载前
   4. 网络连接/断开连接
   5. 加载Play，game
   6. 开始游戏前
   7. 结束paly，game
   8. 注册服务器/client的时候
   9. 切换到 Edit/PlayScene
   10. OnTickPlayer/Character  OnTick

## UniModuleManager

**preInitializeAsync**
1. 注册所有模块，并根据时机进行调用对应的回调函数+update
2. Statistics 上传策略(按帧，按时间)
3. 质量控制  QualityManager
4. 初始化UI，并固定位置

