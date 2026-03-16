---
tags:
  - unity
---
# Assert

package：
- netcode for gameobject
- https://github.com/VeriorPies/ParrelSync.git?path=/ParrelSync

model：
https://www.patreon.com/posts/low-poly-man-80680002

https://www.bilibili.com/video/BV12g4y1P7Vw/?spm_id_from=333.788&vd_source=8beb74be6b19124f110600d2ce0f3957

## 自制UI

三个组件:
- Canvas
- Canvas Scaler
- Grahic RayCaster

17:18

## 存档系统


## 问题 1  人物在落下之后，还会进行一点移动

原因： 在 进入 empty 的时候 设置  isJumping flag -- 有点问题

我们在 jumping end  状态进行设置


## 跳跃设计

进入跳跃  -> 跳跃升起 -> 到地面 则 jump end
**这里如果没到地面 默认** |-> 没到地面， jump idle ->到里面 jump end


## 人物攻击逻辑 

**输入攻击键**
1. NetWork --- 设置 左右手
2. CombatManager.PerformAction!!!  两个参数 **1. Inventory 中的 当前右手武器 ， 以及右手武器的 Action**

```c#
player.playerCombatManager.PerformWeaponBasedAction
(player.playerInventoryManager.currentRightHandWeapon.oh_rb_Action, 													player.playerInventoryManager.currentRightHandWeapon);

```


**PerformWeaponBasedAction**

只有在 Owner 的时候 ---
1. 设置当前武器 ID
2. 通知其他 client 进行动作！！

```c#
public void PerformWeaponBasedAction(WeaponItemAction weaponAction, WeaponItem weaponPerformingAction){
	
	if(player.IsOwner){
		weaponAction.AttemptToPerformAction(player, weaponPerformingAction); 
	//  通知所有client 进行动作
		player.playerNetworkManager.NotifyTheServerOfWeaponActionServerRpc(NetworkManager.Singleton.LocalClientId, weaponAction.actionID, weaponPerformingAction.itemID);
	}
}









//=============== AttemptToPerformAction =================
// 当前使用 武器的ID
public virtual void AttemptToPerformAction(PlayerManager playerPerformingAction, WeaponItem weaponPerformingAction){
	if(playerPerformingAction.IsOwner){
		playerPerformingAction.playerNetworkManager.currentWeaponBeingUsed.Value = weaponPerformingAction.itemID;
	}

	Debug.Log("Action is Fired");
}

// 检测是否能够进行动作
public override void AttemptToPerformAction(PlayerManager playerPerformingAction, WeaponItem weaponPerformingAction)
{
	base.AttemptToPerformAction(playerPerformingAction, weaponPerformingAction);

	if(!playerPerformingAction.IsOwner) return;

	//  检查是否需要停止

	if(playerPerformingAction.playerNetworkManager.currentStamina.Value <= 0){
		return;
	}

	if(!playerPerformingAction.isGrounded) return ; // 不在地面 不行

	PerformLightAttack(playerPerformingAction, weaponPerformingAction);

}

// 具体执行动作
private void PerformLightAttack(PlayerManager playerPerformingAction, WeaponItem weaponPerformingAction){
	


	if(playerPerformingAction.playerNetworkManager.isUsingRightHand.Value){
		playerPerformingAction.playerAnimatorManager.PlayerTargetAttackActionAnimation(AttackType.LightAttack01, light_Attack_01, true);
	}

	if(playerPerformingAction.playerNetworkManager.isUsingLeftHand.Value){
		// playerPerformingAction.playerAnimatorManager.PlayerTargetAttackActionAnimation();
	}
}
```


**Network**

```c#
// ITEM ACTIONS
[ServerRpc]
public void NotifyTheServerOfWeaponActionServerRpc(ulong clientID, int actionID, int weaponID){
	if(IsServer){
		NotifyTheServerOfWeaponActionClientRpc(clientID, actionID, weaponID);
	}
}


[ClientRpc]
private void NotifyTheServerOfWeaponActionClientRpc(ulong clientID, int actionID, int weaponID){
	//  注意， 这里自身不能播放动画， 使用来广播进行动画的
	if(clientID != NetworkManager.Singleton.LocalClientId){
		PerformWeaponBasedAction(actionID, weaponID);
	}
}

private void PerformWeaponBasedAction(int ActionID, int waeponID ){
	WeaponItemAction weaponItemAction = WorldActionManager.instance.GetWeaponItemAction(ActionID);

	if(weaponItemAction != null){
		weaponItemAction.AttemptToPerformAction(player, WorldItemDatabase.Instance.getWeaponByID(waeponID));
	}else{
		Debug.Log("Action is null");
	}
}
```


## 人物受击


1. 在动作的工程中开启 collider

```c#
protected override void OnTriggerEnter(Collider other)
{

	CharacterManager damageTarget = other.GetComponentInParent<CharacterManager>();



	if(damageTarget != null){

		if( damageTarget == characterCausingDamage) return; // 不打自己


		contactPoint  = other.gameObject.GetComponent<Collider>().ClosestPointOnBounds(transform.position);
		Debug.Log(other.gameObject.name);

		// check if we can damage this target base on friendly fire

		// check if target is blocking


		// check if is invulnerable

		//damage
		DamageTarget(damageTarget);
	}
}

protected override void DamageTarget(CharacterManager damageTarget)
{
	// dot damage the same taget more than once 
	if(characterDamaged.Contains(damageTarget)) return;

	characterDamaged.Add(damageTarget);

	TakeDamageEffect damageEffect = Instantiate(WorldCharacterEffectsManager.instance.takeDamageEffect);
	damageEffect.physicalDamage = physicalDamage;
	damageEffect.magicDamage = magicDamage;
	damageEffect.fireDamage = fireDamage;
	damageEffect.holyDamage = holyDamage;
	damageEffect.contactPoint = contactPoint;

	switch(characterCausingDamage.characterCombatManager.currentAttackType){
		case AttackType.LightAttack01:
			ApplyAttackDamageModifier(light_Attack_01_Modifier, damageEffect);
			break;
		default:
			break;
	}
	// damageTarget.characterEffectsManager.ProcessInstantEffect(damageEffect);

	if(characterCausingDamage.IsOwner){ // 不计算两次伤害 ！！！！
		damageTarget.characterNetworkManager.NotifyTheServerOfCharacterDamageServerRpc(damageTarget.NetworkObjectId, characterCausingDamage.NetworkObjectId,
		damageEffect.physicalDamage, damageEffect.magicDamage, damageEffect.fireDamage, damageEffect.holyDamage, damageEffect.poiseDamage,
		damageEffect.angleHitFrom, damageEffect.contactPoint.x,damageEffect.contactPoint.y,damageEffect.contactPoint.z
		);
	}
}


private void ApplyAttackDamageModifier(float modifier, TakeDamageEffect damage){
	damage.physicalDamage *= modifier;
	damage.magicDamage *= modifier;
	damage.fireDamage *= modifier;
	damage.holyDamage *= modifier;
	damage.poiseDamage *= modifier;

}

```

DamageTarget 这里 在主机的时候才会计算一次伤害！！！， 


**NetWork**

```c#
[ServerRpc(RequireOwnership = false)]
public void NotifyTheServerOfCharacterDamageServerRpc(ulong damageCharacterID,ulong characterCausingDamageID,
	float physicalDamage, float magicDamage, float fireDamage, float holyDamage, float poiseDamage,
	float angleHitFrom, float contactPointX, float contactPointY, float contactPointZ
){
	if(IsServer){
		NotifyTheServerOfCharacterDamageClientRpc(damageCharacterID, characterCausingDamageID, 
		physicalDamage, magicDamage, fireDamage, holyDamage, poiseDamage, 
		angleHitFrom, contactPointX, contactPointY , contactPointZ);        
	}
}

[ClientRpc]
public void NotifyTheServerOfCharacterDamageClientRpc(ulong damageCharacter,ulong characterCausingDamageID,
	float physicalDamage, float magicDamage, float fireDamage, float holyDamage, float poiseDamage,
	float angleHitFrom, float contactPointX, float contactPointY, float contactPointZ
){
	ProcessCharacterDamageFromServer(damageCharacter, characterCausingDamageID, 
		physicalDamage, magicDamage, fireDamage, holyDamage, poiseDamage, 
		angleHitFrom, contactPointX, contactPointY , contactPointZ);
}

public void ProcessCharacterDamageFromServer(ulong damageCharacterID,ulong characterCausingDamageID,
	float physicalDamage, float magicDamage, float fireDamage, float holyDamage, float poiseDamage,
	float angleHitFrom, float contactPointX, float contactPointY, float contactPointZ
){
	CharacterManager  damagedCharacter = NetworkManager.Singleton.SpawnManager.SpawnedObjects[damageCharacterID].gameObject.GetComponent<CharacterManager>();
	CharacterManager  characterCausingDamage =  NetworkManager.Singleton.SpawnManager.SpawnedObjects[characterCausingDamageID].gameObject.GetComponent<CharacterManager>();


	TakeDamageEffect damageEffect = Instantiate(WorldCharacterEffectsManager.instance.takeDamageEffect);
	
	damageEffect.physicalDamage = physicalDamage;
	damageEffect.magicDamage = magicDamage;
	damageEffect.fireDamage = fireDamage;
	damageEffect.holyDamage = holyDamage;
	damageEffect.poiseDamage = poiseDamage;
	damageEffect.angleHitFrom = angleHitFrom;
	damageEffect.contactPoint = new Vector3(contactPointX, contactPointY, contactPointZ);

	damageEffect.characterCausingDamage = characterCausingDamage;


	damagedCharacter.characterEffectsManager.ProcessInstantEffect(damageEffect);
}
```