---
tags:
  - unity
---
## 饿汉

```C#
public static WorldSoundFXManager instance;

private void Awake()
{
	if (instance == null){
		instance = this;   
	}else{
		Destroy(gameObject);
	}
}


```

## 懒汉

```c#
public static WorldSoundFXManager instance;

public static ABManager getIntance(){
	if(Instance == null){
		Instance = new ABManager();
		return Instance;
	}else{
		return Instance;
	}
}


```