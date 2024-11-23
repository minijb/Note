
## container counter

我们创建 一个 `_BaseCounter` 作为所有 橱柜类的父类。 使用 prefeb variable --- 首先创建一个普通的预制体作为基类，使用这个基类可以创建很多子类的 prefeb 也就是子类。

使用使用这种方法创建一个 `ClearCounter`  的 prefeb variable 。同理创建 `ContainerCounter` 。我们将 clearCounter 的逻辑复制过去，但是并不能实现。因为我们之前所有的都直接使用 `ClearCounter` 作为互动的对象，当换到 ContainerCounter 的时候 很多逻辑就不能实现。

这里我们使用继承和多态，我们使用 `BaseCounter` 作为基类， clearcounter and containercounter 继承这个基类。 并更新 player 和 selectedCounter 的代码。

最后我们为 container 添加一个动画

```c#
// 发布
public event EventHandler OnPlayerGrabbedObject;

[SerializeField] private KitchenOjectSO kitchenOjectSo;

public override void Interact(Player player)
{

	if (!HasKitchenObject())
	{
		Transform KitchenObjectTransform = Instantiate(kitchenOjectSo.prefeb);
		KitchenObjectTransform.GetComponent<KitchenObject>().SetKictonObjectParent(player);
		OnPlayerGrabbedObject?.Invoke(this, EventArgs.Empty);
	}
}



//订阅  
public class ContainerCounterVisual : MonoBehaviour
{

    private const string OPEN_CLOSE = "OpenClose";

    [SerializeField] private ContainerCounter container;
    private Animator animator;


    private void Awake()
    {
        animator = GetComponent<Animator>();
    }

    private void Start()
    {
        container.OnPlayerGrabbedObject += Container_OnPlayerGrabbedObject;
    }

    private void Container_OnPlayerGrabbedObject(object sender, EventArgs e)
    {
        animator.SetTrigger(OPEN_CLOSE);
    }
}
```

## pick up and drop object


```c#
//containerCounter
public override void Interact(Player player)
{

	if (!HasKitchenObject())
	{
		if (!player.HasKitchenObject())
		{
			// plsyer get the kitchen objct
			Transform KitchenObjectTransform = Instantiate(kitchenOjectSo.prefeb);
			KitchenObjectTransform.GetComponent<KitchenObject>().SetKictonObjectParent(player);
			OnPlayerGrabbedObject?.Invoke(this, EventArgs.Empty);
		}

	}
}


//clearCounter
public override void Interact(Player player)
{
	if (!HasKitchenObject())
	{
		// dont't have kitchenObject
		if (player.HasKitchenObject()) // player carrying something
		{
			player.GetKitchenObject().SetKictonObjectParent(this);
		}
		else // player don't carrying something
		{
			
		}
	}
	else
	{
		// has kitchonobject
		if (player.HasKitchenObject())
		{
				
		}
		else
		{
			GetKitchenObject().SetKictonObjectParent(player);
		}
	}
}
```


我们会创建多个kitchonObject同时根据每种，创建一个 Container 方便之后创建多个 container

## 切菜

- 创建一个 cuttingCounter
- 创建对应 xxxslices 以及对应的 prefeb

逻辑实现

- 添加一个新的动作，并在 gameinput 中进行绑定 ， 创建一个新的事件
- 在 player 绑定这个事件
- 添加 cuttingCounter的逻辑

```c#

// player
private void GameInput_OnInteractAlternateAction(object sender, EventArgs e)
{
	if (selectCounter != null)
	{
		selectCounter.InteractAlterate(this);
	}
}

// cuttingcounter
public override void InteractAlterate(Player player)
{
	if (HasKitchenObject())
	{
		//删除
		GetKitchenObject().DestorySelf();

		//使用静态方法添加一个 kitchonobject 并使 counter 得到这个 object
		KitchenObject.SpwnKitchonObject(kitchenOjectSo, this);
	}
}

// kitchenObject
public static KitchenObject SpwnKitchonObject(KitchenOjectSO kitchenOjectSo, IKitchonObjectParent iKitchonObjectParent)
{
	Transform kitchenObjectTransform = Instantiate(kitchenOjectSo.prefeb);
	KitchenObject kitchenObject = kitchenObjectTransform.GetComponent<KitchenObject>();
	kitchenObject.SetKictonObjectParent(iKitchonObjectParent);
	return kitchenObject;
}
```

## 实现切菜功能

- 每一种可以切的 --- 得到对应的片
- 不可以切的不能放到 cutting 上
- 注意 片 不能继续切

因为这是一种对应关系的数据 --- 我们可以使用 script object

```c#
[CreateAssetMenu()] 
public class CuttingRecipeSo : ScriptableObject
{
    public KitchenOjectSO input;
    public KitchenOjectSO output;
}
```

同时 cuttingCounter 内需要记录每种对应关系 (其实也可以作为一种 scirpt object 防止每个counter 持有过多的引用)

```c#
[SerializeField] private CuttingRecipeSo[] cuttingRecipeSoArray;

// 实现两个函数， 判断是否可切+得到片的object

private KitchenOjectSO getOutputForInput(KitchenOjectSO inputKitchenOjectSo)
{
	foreach (CuttingRecipeSo cuttingRecipeSo in cuttingRecipeSoArray)
	{
		if (cuttingRecipeSo.input == inputKitchenOjectSo)
		{
			return cuttingRecipeSo.output;
		}
	}
	return null;
}

private bool hasRecipeWithInput(KitchenOjectSO inputkKitchenOjectSo)
{
	foreach (CuttingRecipeSo cuttingRecipeSo in cuttingRecipeSoArray)
	{
		if (cuttingRecipeSo.input == inputKitchenOjectSo)
		{
			return true;
		}
	}
	return false;
}
```

对之前的函数进行规范。

## cutting progress and world canvas

添加最大需要的动作次数

```c#
// cuttingSliceso
public KitchenOjectSO input;
public KitchenOjectSO output;
public int CuttingProgressMax;
```

### world canvas

我们在 cuttingCounter 中创建一个bar，并设置background。 注意 canvas 内的图层顺序就是 列表中的顺序

> sort in sorting layer/ sorting order [video](https://www.youtube.com/watch?v=5_BwFB-1dAo&feature=youtu.be)
> UI element [video](https://www.youtube.com/watch?v=Zwgj3mwOVlg)


使用 event 将 切菜动作绑定显示。

## camera lookat

问题：如果cuttingcounter 反向，那么进度条也是反向的，因此我们需要让摄像头看向用户

```c#
public class LookAtCamera : MonoBehaviour
{

    private enum Mode
    {
        LookAt,
        LookAtInverted,
        CameraForward,
        CameraForwardInverted,
    }

    [SerializeField] private Mode mode = Mode.LookAtInverted;

    // run after update
    private void LateUpdate()
    {
        switch (mode)
        {
            case Mode.LookAt:
                transform.LookAt(Camera.main.transform);
                break;
            case Mode.LookAtInverted:   
                Vector3 dirDormCamera = transform.position - Camera.main.transform.position;
                transform.LookAt(transform.position + dirDormCamera);
                break;
            case Mode.CameraForward:
                transform.forward = Camera.main.transform.forward; 
                break;
            case Mode.CameraForwardInverted:
                transform.forward = -Camera.main.transform.forward;
                break;

        }

        // 如果又很多相机， 则不建议使用 main camera， 每一次 update 都会遍历一次 array
    }
}
```

## trashcounter

删除 kitchonObject

## frying counter

- 创建 fryingh script object
- 创建 counter

实现燃烧的事件

 - 直接使用一个 float 变量
 - 使用协程 Coroutines --- 不需要


coroutines 示范

```c#
private void Start()
{
	StartCoroutine(HandleFryTimer());
}

private IEnumerable HandleFryTimer()
{
	yield return new WaitForSeconds(1f);
}
```


使用 一个变量并使用 Update

```c#
private float fryingTimer;
private FryingRecipeSo fryingRecipeSo;

private void Update()
{
	if (HasKitchenObject())
	{
		fryingTimer += Time.deltaTime;
		if (fryingTimer > fryingRecipeSo.FryingTimeMax)
		{
			fryingTimer = 0f;
			Debug.Log("Fired");
			GetKitchenObject().DestorySelf();
			KitchenObject.SpwnKitchonObject(fryingRecipeSo.output, this);
		}
	}
}
```

问题：会一直燃烧。

创建一个状态管理。

```c#
public enum State
{
	Idle,
	Frying,
	Fried,
	Burned
}

private float fryingTimer;
private float burningTimer;
private FryingRecipeSo fryingRecipeSo;
private BurningRecipeSo burningRecipeSo;
private State state;


public event EventHandler<OnStateChangedEventArgs> OnsStateChanged;

public class OnStateChangedEventArgs : EventArgs
{
	public State state;
}



private void Start()
{
	state = State.Idle;
}

private void Update()
{

	if (HasKitchenObject())
	{
		switch (state)
		{
			case State.Idle:
				break;
			case State.Frying:
				fryingTimer += Time.deltaTime;
				if (fryingTimer > fryingRecipeSo.FryingTimeMax)
				{
					GetKitchenObject().DestorySelf();
					KitchenObject.SpwnKitchonObject(fryingRecipeSo.output, this);
					burningRecipeSo = GetBurningRecipeSoWithInput(GetKitchenObject().GetKictionObjectSO());
					state = State.Fried;
					burningTimer = 0f;

					OnsStateChanged?.Invoke(this, new OnStateChangedEventArgs
					{
						state =  this.state
					});
				}
				break;
			case State.Fried:
				burningTimer += Time.deltaTime;
				if (burningTimer > burningRecipeSo.BurningTimeMax)
				{
					GetKitchenObject().DestorySelf();
					KitchenObject.SpwnKitchonObject(burningRecipeSo.output, this);
					state = State.Burned;
					OnsStateChanged?.Invoke(this, new OnStateChangedEventArgs
					{
						state = this.state
					});
				}
				break;
			case State.Burned:
				break;
		}
	}
}
```

### 重用进度条


可选用方法: 

- 复制代码 -- 并更改橱柜类
- 使用接口 

第一种适合表现不同的进度条， 第二种适合表现相似的进度条

首先创建一个接口

表示 需要接口做的事

```c#
public interface IHasProgress 
{
    public event EventHandler<OnProgressChangedEventArgs> OnProgressChanged;
    public class OnProgressChangedEventArgs : EventArgs
    {
        public float progressNormalized;
    }
}

```

stove counter 继承这个接口

对于 progressUI

```c#
[SerializeField] private Image barImage;
[SerializeField] private GameObject hasProgreeObject;

private IHasProgress hasProgress;


hasProgress = hasProgreeObject.GetComponent<IHasProgress>();
if (hasProgress == null)
{
	Debug.LogError("dont have progess object");
}
```

由于unity 不能直接识别接口类，因此我们需要进行转换。

## platesCounter

由于 plate 是可以堆叠的 因此我们无法直接使用 baseCounter 中建立物体的方法，我们需要 在 PlateCounterVisual 中建立一个列表保存自动生成的盘子并使用事件进行连接

```c#

// plate counter
public class PlatesCounter : BaseCounter
{
    private float spawnPlateTimmer;
    private float spawnPlateTimmerMax = 4f;
    private int platesSpawnAmount;
    private int platesSpawnAmountMax = 4;

    [SerializeField] private KitchenOjectSO plaKitchenOjectSo;

    public event EventHandler OnPlateSpawned;
    public event EventHandler OnPlateRemoved;

    private void Update()
    {
        spawnPlateTimmer += Time.deltaTime;
        if (spawnPlateTimmer > spawnPlateTimmerMax)
        {
            spawnPlateTimmer = 0f;

            if (platesSpawnAmount < platesSpawnAmountMax)
            {
                platesSpawnAmount++;
                OnPlateSpawned?.Invoke(this, EventArgs.Empty);
            }
        }
    }

    public override void Interact(Player player)
    {
        if (!player.HasKitchenObject()) // player empty hand
        {
            if (platesSpawnAmount > 0) 
            {
                // give plate to player
                platesSpawnAmount--;

                KitchenObject.SpwnKitchonObject(plaKitchenOjectSo, player);
                OnPlateRemoved?.Invoke(this, EventArgs.Empty);
            }
        }
        else
        {

        }
    }
}



public class PlatesCounterVisual : MonoBehaviour
{
    [SerializeField] private Transform counterTopPoint;
    [SerializeField] private Transform plateVisualPrfeb;
    [SerializeField] private PlatesCounter platesCounter;

    private List<GameObject> plateVisualGameObjectsList;

    private void Start()
    {
        platesCounter.OnPlateSpawned += PlatesCounter_OnPlateSpawned;
        platesCounter.OnPlateRemoved += PlatesCounter_OnPlateRemoved;
        plateVisualGameObjectsList = new List<GameObject>();
    }

    private void PlatesCounter_OnPlateRemoved(object sender, System.EventArgs e)
    {
        GameObject plate = plateVisualGameObjectsList[plateVisualGameObjectsList.Count - 1];
        plateVisualGameObjectsList.Remove(plate);
        Destroy(plate);
    }

    private void PlatesCounter_OnPlateSpawned(object sender, System.EventArgs e)
    {
        Transform plateVisualTransform = Instantiate(plateVisualPrfeb, counterTopPoint);


        float plateOffSetY = .1f;
        plateVisualTransform.localPosition = new Vector3(0, plateOffSetY* plateVisualGameObjectsList.Count, 0);
        plateVisualGameObjectsList.Add(plateVisualTransform.gameObject);

    }
}

```

## 让盘子和事物进行互动

由于盘子有额外的逻辑 -- 同时他也符合 kictionObject 的逻辑, 因此我们可以将plate 作为 kictionObject 的子类

```c#
public class PlateKitchenObject : KitchenObject
{

    private List<KitchenOjectSO> kitchenObjectSOList;

    [SerializeField] private List<KitchenOjectSO> valiedKictionObjectSOList;



    private void Awake()
    {
        kitchenObjectSOList = new List<KitchenOjectSO>();
    }
    public bool TryAddIngredient(KitchenOjectSO kictKitchenOjectSo)
    {

        if (valiedKictionObjectSOList.Contains(kictKitchenOjectSo))
        {
            if (kitchenObjectSOList.Contains(kictKitchenOjectSo))
            {
                return false;
            }
            else
            {
                kitchenObjectSOList.Add(kictKitchenOjectSo);
                return true;
            }
        }
        else // is not valied in 
        {
            return false;
        }
    }
}
```


此时 盘子的互动可以

```c#
if (player.HasKitchenObject())
{
	if (player.GetKitchenObject().TryGetPlate(out PlateKitchenObject plateKitchenObject)) // hold a plate
	{
		if (plateKitchenObject.TryAddIngredient(GetKitchenObject().GetKictionObjectSO()))
		{
			GetKitchenObject().DestorySelf();
		}
	}
	else
	{
		// player is carry something else
		if (GetKitchenObject().TryGetPlate(out plateKitchenObject))
		{
			if (plateKitchenObject.TryAddIngredient(player.GetKitchenObject().GetKictionObjectSO()))
			{
				player.GetKitchenObject().DestorySelf();
			}
		}
	}
}
```

简化代码接口 --- kitchenObject 得到子类

```c#
public bool TryGetPlate(out PlateKitchenObject plateKitchenObject)
{
	if (this is PlateKitchenObject)
	{
		plateKitchenObject = this as PlateKitchenObject;
		return true;
	}
	else
	{
		plateKitchenObject = null;
		return false;
	}
}
```

## plate visiual

简单来说就是根据一个关系对照表  根据 player 手中的 物品 显示 预先设置好的 prefeb 中的 visiual 物体

```c#
public class PlateCompleteVisiual : MonoBehaviour
{
    [Serializable] public struct KictionObjectSO_GameObject
    {
        public KitchenOjectSO KitchenOjectSo;
        public GameObject gameObject;
    }


    [SerializeField] private PlateKitchenObject plateKitchenObject;
    [SerializeField] public List<KictionObjectSO_GameObject> KictionObjectSO_GameObjectlist;

    private void Start()
    { 
        plateKitchenObject.OnIngredientAdded += PlateKitchenObject_OnIngredientAdded;
        foreach (KictionObjectSO_GameObject kictionObjectSoGameObject in KictionObjectSO_GameObjectlist)
        {
            kictionObjectSoGameObject.gameObject.SetActive(false);
        }
    }

    private void PlateKitchenObject_OnIngredientAdded(object sender, PlateKitchenObject.OnIngredientAddedEventArgs e)
    {
        foreach (KictionObjectSO_GameObject kictionObjectSoGameObject in KictionObjectSO_GameObjectlist)
        {
            if (kictionObjectSoGameObject.KitchenOjectSo == e.KitchenOjectSo)
            {
                kictionObjectSoGameObject.gameObject.SetActive(true);
            }
        }
    }
}


// plate kiction object

public bool TryAddIngredient(KitchenOjectSO kictKitchenOjectSo)
{

	if (valiedKictionObjectSOList.Contains(kictKitchenOjectSo))
	{
		if (kitchenObjectSOList.Contains(kictKitchenOjectSo))
		{
			return false;
		}
		else
		{
			kitchenObjectSOList.Add(kictKitchenOjectSo);
			OnIngredientAdded?.Invoke(this, new OnIngredientAddedEventArgs
			{
				KitchenOjectSo = kictKitchenOjectSo
			});
			return true;
		}
	}
	else // is not valied in 
	{
		return false;
	}

}
```


## plate counter 的世界icon

在 plate 的 prefeb 中建立 canves 和 并使用 image 图片， 安装 package : 2D spirte。
使用 grid layout group 实现网格功能，更好的规划子图片 

> UI 大小 --- $0.9 \times 0.9$
> cell size --- $0.3 \times 0.3$
> 同理 这种 leyout 还有 vertical horizontal


简单来说就是监听这个事件并根据 父obj 中的 scriptobjectlist 添加一个 icon。于此同时创建的时候可以根据 kitchonObjectSO 中的 sprite 添加精灵

```c#
public class PlateIconUI : MonoBehaviour
{
    [SerializeField] private PlateKitchenObject plateKitchenObject;
    [SerializeField] private Transform iconTemplate;

    private void Start()
    {
        plateKitchenObject.OnIngredientAdded += PlateKitchenObject_OnIngredientAdded;
    }

    private void Awake()
    {
        // iconTemplate.gameObject.SetActive(false);
    }

    //监听这个事件
    private void PlateKitchenObject_OnIngredientAdded(object sender, PlateKitchenObject.OnIngredientAddedEventArgs e)
    {
        UpdateVisiual();
    }

    private void UpdateVisiual()
    {

        foreach (Transform child in transform)
        {
            if (child == iconTemplate) continue;
            Destroy(child.gameObject);
        }

        foreach (KitchenOjectSO kitchenOjectSo in plateKitchenObject.GetKitchenOjectSoList())
        {
            Transform iconTransform = Instantiate(iconTemplate, transform);
            iconTransform.gameObject.SetActive(true);
            iconTransform.GetComponent<PlateIconSingleUI>().SetkictchenObject(kitchenOjectSo);
        }
    }
}

// icon 
public class PlateIconSingleUI : MonoBehaviour
{
    [SerializeField] private Image image;
    public void SetkictchenObject(KitchenOjectSO obj)
    {
        image.sprite = obj.sprite;
    }
}

```

## delivery counter

- 创建一个 counter
- 使用 shader 
	- 创建shader
	- 根据 shader 创建 material

## delivery manager

首先 manager 应该是一个单例。

```c#
public class DeliveryManager : MonoBehaviour
{
    public static DeliveryManager Instance { get; private set; }

	//创建 RecipeSO 并 使用一个 RecipeListSO 包含所有的菜单
    private List<RecipeSO> waitingrecipeList;
    [SerializeField] private RecipeListSO recipeListSo;

    private float spawnRecipeTimer;
    private float spawnRecipeTimerMax = 4f;
    private int waitingRecipeMax = 4;


    private void Awake()
    {

        Instance = this;
        waitingrecipeList = new List<RecipeSO>();
    }

    private void Update()
    {
        spawnRecipeTimer -= Time.deltaTime;

        if (spawnRecipeTimer <= 0f)
        {
            spawnRecipeTimer = spawnRecipeTimerMax;

            if (waitingrecipeList.Count < waitingRecipeMax)
            {
                RecipeSO waitingRecipeSo = recipeListSo.RecipeSoList[Random.Range(0, recipeListSo.RecipeSoList.Count)];
                Debug.Log(waitingRecipeSo.RecipeName);
                waitingrecipeList.Add(waitingRecipeSo);
            }

        }
    }


    public void DeliverRecipe(PlateKitchenObject plateKitchenObject)
    {
        for (int i = 0; i < waitingrecipeList.Count; i++)
        {
            RecipeSO waitingRecipeSo = waitingrecipeList[i];

            // number 相同
            if (waitingRecipeSo.KitchenOjectSoList.Count == plateKitchenObject.GetKitchenOjectSoList().Count)
            {
                bool plateMatch = true;

                foreach (KitchenOjectSO recepie_kitchenOjectSo in waitingRecipeSo.KitchenOjectSoList)
                {
                    bool ingredientFound = false;

                    foreach (KitchenOjectSO plate_kitchenOjectSo in plateKitchenObject.GetKitchenOjectSoList())
                    {
                        if (plate_kitchenOjectSo == recepie_kitchenOjectSo)
                        {
                            ingredientFound = true;
                            break;
                        }
                    }

                    if(!ingredientFound) // something in the recipe can't found
                    {
                        plateMatch = false;
                    }
                }


                if (plateMatch)
                {
                    Debug.Log("player delivery a correct recipe");
                    waitingrecipeList.RemoveAt(i);
                    return;
                }
            }
        }
        // no match found

        Debug.Log("player do not delivery a correct recipe");
    }


}
```


## the world UI of waiting list

> UI -- anchor and pivot
> 
> https://vionixstudio.com/2022/08/25/unity-ui-anchors-and-pivots-guide/#:~:text=UI%20Anchors%20UI%20Anchors%20position%20is%20based%20on,change%20based%20on%20the%20Anchor%20presents%20you%20select
> 
> https://zhuanlan.zhihu.com/p/685783301


- 创建 canvas
- 创建 text
- 创建 recipe template and recipe container
- 创建 icon conatiner and ingredientImage

Delivery manager UI UI的总体逻辑

```c#
public class DeliveryManagerUI : MonoBehaviour
{
    [SerializeField] private Transform container;
    [SerializeField] private Transform recipeTemplate;

    private void Awake()
    {
        recipeTemplate.gameObject.SetActive(false);
    }

	// 订阅 DeliveryManager 的事件
    private void Start()
    {
        DeliveryManager.Instance.OnRecipeCompleted += DeliveryManager_OnRecipeCompleted;
        DeliveryManager.Instance.OnRecipeSpawned += DeliveryManager_OnRecipeSpawned;
        UpdateVisual();
    }

    private void DeliveryManager_OnRecipeSpawned(object sender, System.EventArgs e)
    {
        UpdateVisual();
    }

    private void DeliveryManager_OnRecipeCompleted(object sender, System.EventArgs e)
    {
        UpdateVisual();
    }

    private void UpdateVisual()
    {
        foreach (Transform child in container)
        {
            if (child == recipeTemplate) continue;
            Destroy(child.gameObject);    
        }

        foreach (RecipeSO recipeSo in DeliveryManager.Instance.GetWaitingRecipeSOList())
        {
            Transform recepieTransform = Instantiate(recipeTemplate, container);
            recepieTransform.gameObject.SetActive(true);
            recepieTransform.GetComponent<DeliveryManagerSingleUI>().SetRecipeSO(recipeSo);
        }
    }
}
```


Delivery manager Single UI 处理单个的recipe

```c#
public class DeliveryManagerSingleUI : MonoBehaviour
{

    // is not text --- TextMeshProUGUI -- Text is the 3D object
    [SerializeField] private TextMeshProUGUI recipeNameText;
    [SerializeField] private Transform iconContainer;
    [SerializeField] private Transform iconTemplate;


    private void Awake()
    {
        iconTemplate.gameObject.SetActive(false);
    }

    public void SetRecipeSO(RecipeSO recipeSO)
    {
        recipeNameText.text = recipeSO.RecipeName;

        foreach (Transform child in iconContainer)
        {
            if(child == iconTemplate) continue;
            Destroy(child.gameObject);
        }

        foreach (KitchenOjectSO kitchenOjectSo in recipeSO.KitchenOjectSoList)
        {
            Transform iconTransform = Instantiate(iconTemplate, iconContainer);
            iconTransform.gameObject.SetActive(true);
            iconTransform.GetComponent<Image>().sprite = kitchenOjectSo.sprite;
        }
    }

    
}
```