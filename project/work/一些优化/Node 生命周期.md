
所有的Node 都含有一个个生命周期 如 初始化， OnDescripted， 

```c#
public override void OnUniStart(Uni.Component.IUniComponent component,Uni.UniNode node){((UniAnimationBasicComponent)component).OnUniStart(node);}
public override void OnUniRenderReady(Uni.Component.IUniComponent component,Uni.UniNode node){((UniAnimationBasicComponent)component).OnUniRenderReady(node);}
public override void OnUniLogicReady(Uni.Component.IUniComponent component,Uni.UniNode node){((UniAnimationBasicComponent)component).OnUniLogicReady(node);}
public override void OnUniDestroy(Uni.Component.IUniComponent component){((UniAnimationBasicComponent)component).OnUniDestroy();}
public override void OnUniStartAuthority(Uni.Component.IUniComponent component,Uni.UniNode node){((UniAnimationBasicComponent)component).OnUniStartAuthority(node);}
public override void OnUniStopAuthority(Uni.Component.IUniComponent component,Uni.UniNode node){((UniAnimationBasicComponent)component).OnUniStopAuthority(node);}
public override void OnUniScenePlaying(Uni.Component.IUniComponent component){((UniAnimationBasicComponent)component).OnUniScenePlaying();}
public override void OnUniSceneStop(Uni.Component.IUniComponent component){((UniAnimationBasicComponent)component).OnUniSceneStop();}
```
