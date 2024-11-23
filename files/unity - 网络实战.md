
## 1. 网络物体初始化

初始化： 在当前物体下创建一个子物体，并使用 skin 连接


```c#
public class BaseTank : MonoBehaviour
{
    public GameObject skin;


    public virtual void Init(string path){
        GameObject skinRes = ResManager.LoadPrefab(path);
        skin = (GameObject)Instantiate(skinRes);
        skin.transform.parent = this.transform;
        skin.transform.localPosition = Vector3.zero;
        skin.transform.localEulerAngles = Vector3.zero;
    }



// 外部调用：
void Start()
{
	GameObject tankObj = new GameObject("tank"); // 创建一个新物体
	BaseTank baseTank = tankObj.AddComponent<BaseTank>(); // 添加脚本
	baseTank.Init("tankPrefab"); // 初始化
	Debug.Log(baseTank.skin);
}


```


## camera follow 逻辑

```c#
public class CameraFollow : MonoBehaviour
{
    public Vector3 distance = new Vector3(0f, 8f, -18f); // 距离矢量

    public Camera camera;

    public Vector3 offset = new Vector3(0f, 5f, 0f); // 添加 offset

    public float speed = 3f;

    void Start()
    {
        camera = Camera.main;
        // 初始位置
        Vector3 pos = transform.position;
        Vector3 forward = transform.forward;
        Vector3 initPos = pos - 30*forward + Vector3.up*10;
        camera.transform.position = initPos;
    }

    void LateUpdate()
    {
        // 坦克位置
        Vector3 pos = transform.position;
        // 坦克方向
        Vector3 forward = transform.forward;

        // 相机更新后的位置
        Vector3 targetPos = pos;
        targetPos = pos + forward * distance.z;
        targetPos.y += distance.y;

        // 相机位置
        Vector3 cameraPos = camera.transform.position;
        cameraPos = Vector3.MoveTowards(cameraPos, targetPos, Time.deltaTime * speed);
        camera.transform.position = cameraPos;

        // 相机对准坦克
        camera.transform.LookAt(pos + offset);

    }
}


```