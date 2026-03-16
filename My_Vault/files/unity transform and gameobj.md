---
tags:
  - unity
---

- 两者都可以直接创建 gameobj
- 两者之间不能相互转换
- 两者可以通过属性得到对方 `transform.gameobj` `gameobj.transform`
- Insatance 实例化的时候，两者返回对应的属性
- **如果经常改变transformer , 就用transformer， 如果常用 setActivate 这些方法则使用 gameobj 进行实例化**




- **transform** 不能 new ， **gameobj** 可以 new
- transform 不能 Destory , gameobj 可以
