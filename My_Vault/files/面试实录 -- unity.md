
**实现三消算法中生成必定可以全消的内容：**


如果是生成必定可以全消除还得保证趣味性这个就很麻烦了。一般我知道的三消都是策划去配置关卡，也就是说每一关啥样是固定的。但是这个配置的关卡到底能不能规定步骤内消除需要有自动化检测。

最关键是写出评分函数，贪心每一步的最优解，得到理论的最高分。比如权重设置参考，XY坐标移动分，目标分，目标xx元素收集分，留存xx元素分，还有一些未知道具参与的分。

然后再去根据分去进行移动，但是真人会考虑移动完后续的操作，可能当前步不是最优，但是后续会有大片操作空间。这时候还得考虑使用蒙特卡洛树搜索去博弈。

这确实不是一个简单的问题，他也不指望你能解出来，主要还是看你的思路广不广。



**我看到你那个说就是在这个生成地形的时候用了柏林噪声，可以，就是这个柏林噪声到生成地形中间可以再展开。**

讲一讲，就是我首先就是写了一个Mesh，写了个圆筒的那个Mesh，就是自己写个Mesh，然后包括这些顶点、三角形什么都有，然后我就把，然后对于里面每一个这些就是随取随机数，然后用这个噪声去起伏，把它放到那个 Mesh 里面的话，它就可以生成一个那种起伏上地形了，大概是这样子，就是说随机起伏那些顶点坐标，应该这么说。


**然后关于这个柏林噪声，然后它和纯随机是有什么区别呢？为什么？就是比如说你生成地形要使用柏林噪声，而不是说就是使用一个纯随机。**

柏林噪声生成的数值具有自然随机性，避免了简单随机数的不连贯性，也非常的平滑。这个在小车一开始就介绍了，有个模拟的曲线能看出来


**子弹穿透问题**

使用前后帧位置计算路径，来判断是否命中。

**网络问题 ： 客户端和服务器之间有时间差， 如何处理**

- 客户端通过列表存储释放的技能信息， 如果客户端释放时间到了，则判断列表中是否有该信息，有则释放，否则跳过
- 客户端接收到服务器的信息时，如果客户端时间已经过了直接释放，否则则存储在表中，等待客户端时间到了自己去表中拿。

**多个摄像头，让这多个相机同时处于激活状态，然后这时候会发生什么**

会叠加渲染，然后就是说参数的话应该就是相机会有一个渲染的，就是一个层级或者说一个先后，然后肯定是根据他的渲染的先后去，反正这就叠上去一层一层叠上去，

depth

depth only -- depth only就是表示当一帧新画面显示时，它会根据摄像机的深度信息来显示新画面与旧画面。理解这句话，或许不太明确，比如说有两个摄像机，一个摄像机照着大海，一个摄像机照着美女，大海的摄像机的深度是-1， 美女的摄像机的深度是0，根据深度来显示，就是先显示-1的内容，再显示0的内容。这样无论-1里的内容怎么变化，都是当作一个背景，0摄像机就可以设置为深度更新，这样就可以把美女与大海融合到一起了。


如果划定一个范围的话 可以使用 render  texture

https://blog.csdn.net/qq_37524903/article/details/131725727

关于 clear flag ： https://blog.csdn.net/iov3Rain/article/details/81367290

> shader : https://www.bilibili.com/video/BV1yi4y177RJ/?spm_id_from=333.337.search-card.all.click&vd_source=8beb74be6b19124f110600d2ce0f3957


## 图片压缩

ERC 和 ASTC 


## 事件中心

通过 `字典<type, delegate>` 记录。


## TimeSacle

总结一下要点：

1、timeScale是时间流逝速度的缩放比例。

2、timeScale为1.0时，时间是正常速度；为0.5时，时间流逝速度会降为正常速度的一半。

3、timeScale为0时，所有基于帧率的功能都将被暂停。

4、Time.realtimeSinceStartup这个值不受timeScale影响。

5、修改timeScale时，推荐同时以相同比例修改Time.fixedDeltaTime。

6、timeScale为0时，FixedUpdate函数不再执行。

1、timeScale是0到100之间的浮点数，超过此范围时，Unity会给出一条错误信息。这个在实验中没有体现，读者可以自己赋值试试。

2、timeScale会影响FixedUpdate的执行速度，但不会影响Update、LateUpdate（要测试的话把函数Update改为LateUpdate即可）的执行速度。timeScale为0时，FixedUpdate完全停止。

3、timeScale不会影响Coroutine本身的执行速度。当timeScale为0时，如果Coroutine中yield了某个WaitForSeconds或者WaitForFixedUpdate，那么该Coroutine会在此处停下。如果想要等待一个不受timeScale影响的时间，请用WaitForSecondsRealtime。在实验中将ChangeColor函数中的yield return 0;替换成其他的等待的表达式即可测试。

4、timeScale改变时，会对以下值产生影响：time、deltaTime、fixedTime以及fixedUnscaledDeltaTime。

5、timeScale改变时，不会对以下值产生影响：realtimeSinceStartup、unscaledTime、unscaledDeltaTime、fixedUnscaledTime、fixedDeltaTime。

6、当timeScale为0时，fixedUnscaledTime将停止，但是当timeScale由0变为非0值时，这个值将会有个跳跃，接近于unscaledTime和realtimeSinceStartup。

7、当timeScale改变时，fixedUnscaledDeltaTime会按反比进行改变；例外是当timeScale变为0时，fixedUnscaledDeltaTime的值不会发生改变。

## Assetbundle  unload
Q：AssetBundle的Unload方法，传入true和传入false之间的区别？

A：false引用的资源不会完全销毁掉，只断开索引和资源之间的连接，再次加载时候会引入新的资源，可能会导致资源冗余。True就是完全销毁掉，但是可能会导致引用丢失，一般是切换场景或者大的加载的时候会考虑true。


## LZ4 和 Lzma的区别

LZ4 按照块进行压缩。  压缩率不高，但是读取速度快
Lzma 是流式压缩，只能流式读取

