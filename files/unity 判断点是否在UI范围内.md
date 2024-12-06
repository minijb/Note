---
tags:
  - unity
---
需要分情况

camera 模式 

```c#
if (Input.touchCount == 1)
{
	Touch touch = Input.touches[0];
	if (touch.phase == TouchPhase.Began && RectTransformUtility.ScreenPointToLocalPointInRectangle(rectTransform, touch.position, Camera.main,
			out Vector2 localPoint))
	{
		if (rectTransform.rect.Contains(localPoint))
		{
			Debug.Log("in area");   
		}
	}
}
```


overlay 需要通过坐标变换


**完美的解决方案**  转换为世界坐标

```c#
private Rect GetWorldRect(RectTransform rectTransform)  
{  
    Vector3[] corners = new Vector3[4];  
    rectTransform.GetWorldCorners(corners);  
    float width = Math.Abs(Vector2.Distance(corners[0], corners[3]));  
    float height = Math.Abs(Vector2.Distance(corners[0], corners[1]));  
    return new Rect(corners[0], new Vector2(width, height));  
}  
  
private bool IsClickInArea(Vector2 position)  
{  
    RectTransform rect = transform as RectTransform;  
    if(rect!=null)  
    {        Rect worldRect = GetWorldRect(rect);  
        // RectTransformUtility.ScreenPointToWorldPointInRectangle((RectTransform)canvas.transform, position, Camera.main, out Vector3 worldPosition);  
        if (position.x > worldRect.x &&  
            position.x < worldRect.x + worldRect.width &&  
            position.y > worldRect.y &&  
            position.y < worldRect.y + worldRect.height)  
        {            return true;  
        }        else  
        {  
            return false;  
        }           }  
    return false;  
}
```