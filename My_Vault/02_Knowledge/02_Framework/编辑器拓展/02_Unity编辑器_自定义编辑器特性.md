
两种自定义的方法，一种使用csharp的原生特性，还有一种是利用Unity来创建特性

## 1. Csharp 

```c#
public class HttpApiKey : Attribute
{
    public HttpApiKey(string _httpApi)
    {
        httpApi = _httpApi;
    }
    public string httpApi;
}

public class HttpId
{
    //示例，给id标记api
    [HttpApiKey("Register")]
    public const int registerId = 10001;
    [HttpApiKey("Login")]
    public const int loginId = 10002;


    public static void GetHttpApi()
    {
        //反射获取字段
        System.Reflection.FieldInfo[] fields = typeof(HttpId).GetFields();
        System.Type attType = typeof(HttpApiKey);
        for(int i = 0; i < fields.Length; i++)
        {
            if(fields[i].IsDefined(attType,false))
            {
                //获取id
                int httpId = (int)fields[i].GetValue(null);
                //获取api，读取字段的自定义Attribute
                object attribute = fields[i].GetCustomAttributes(typeof(HttpApiKey),false)[0];
                string httpApi = (attribute as HttpApiKey).httpApi;
            }
        }
    }
    
    private void Start()
    {
        if (this.GetType().IsDefined(typeof(CustomAttribute), false))
        {
            Debug.Log("已经产生关联");
        }
    }
}
```


## 2. Unity

```c#
public class ShowTimeAttribute ： PropertyAttribute
{
	public readonly bool ShowHour;
	public ShowTimeAttribute(bool isShowHour = false)
	{
		ShowHour = isShowHour;
	}
}


[CustomPropertyDrawer(typeof(ShowTimeAttribute))]
public class TimerDrawer: PropertyDrawer
{
	public override float GetPropertyHeight(SerializedProperty property, GUIContent label)
	{
		return EditorGUI.GetPropertyHeight(property) * 2;
	}
	
	public override void OnGUI(Rect position, SerializedProperty property, GUIContent lable)
	{
		if (property.propertyType == SerializedPropertyType.Integer){
			property.intValue = EditorGUI.IntField(new Rect(position.x, position.y, position.width, position.height /2), label, Mathf.max(0, property.intValue));
			
			EditorGUI.LabelField(new Rect(xxxxx));
		}else{
			EditorGUI.HelpBox(position, "To use Time Attribute, " + label.Tostring() + "must be int", MessageType.Error);
		}
	}
	
	private string TimerConvert(int value){
	}
}


public class Test : MonoBehaviour
{
	[ShowTime(true)]
	public int time = xxx;
}
```