---
tags:
  - unity
---

## GetKey, GetKeyDown, GetKeyUp

- GetKey --- 按住
- GetKeyDown --- 按下的第一帧为true ，按住后 为 false
- GetKeyUp --- 同理

## new input system 

为了适配更多输入设备并将逻辑和操作进行分离。

- craete/input action
- 添加 Action Map ，设置Action type 和 control type ，添加 Actions 并绑定资源

实时控制：

```c#
private PlayerInputAction playerInputAction;

private void Awake()
{
	playerInputAction = new PlayerInputAction();
	playerInputAction.Player.Enable();
}



public Vector2 GetMovementVectorNormalized()
{
	Vector2 inputVector = playerInputAction.Player.Move.ReadValue<Vector2>();
	inputVector = inputVector.normalized;

	return inputVector;
}
```


按键监控：

利用 c# 事件 进行订阅

[[02 角色控制#use c event to make interact action]]

```c#
private void Awake()
{
	//初始化 input system
	playerInputAction = new PlayerInputAction();
	playerInputAction.Player.Enable();

	// 订阅 interaction 对应的按键 E
	playerInputAction.Player.Interact.performed += Interact_Performed;
}

private void Interact_Performed(UnityEngine.InputSystem.InputAction.CallbackContext obj)
{
	//自定义事件
	OnInteractAction?.Invoke(this, EventArgs.Empty);
}

```