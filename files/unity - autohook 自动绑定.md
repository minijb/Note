---
tags:
  - unity
---





```c#
	[CustomPropertyDrawer(typeof(Autohoo kAttribute))]
public class AutohookPropertyDrawer : PropertyDrawer

{
#if UNITY_EDITOR 
    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        var component = FindAutohookTarget(property);
        if (component != null)
        {
            property.objectReferenceValue = component;
        }
        EditorGUI.PropertyField(position, property, label);
    }
#endif
    //todo 是否需要添加GameObject
    private Component FindAutohookTarget(SerializedProperty property)
    {
        var root = property.serializedObject;
        if (root.targetObject is Component)
        {
            var type = GetTypeFromProperty(property);
            var component = (Component)root.targetObject;
            var components = component.GetComponentsInChildren(type,true);
            foreach (var item in components)
            {
                //确保GameObject不要有重名的,todo 改规则
                if (item.gameObject.name == "#" + property.name)
                {
                    return item.gameObject.GetComponent(type);
                }
            }
        }
        else
        {
            Debug.LogError(property.name+"不是组件，不能被支持");
        }
        return null;
    }
    private static System.Type GetTypeFromProperty(SerializedProperty property)
    {
        var parentComponentType = property.serializedObject.targetObject.GetType();
        var fieldInfo = parentComponentType.GetField(property.propertyPath);
        return fieldInfo.FieldType;
    }
}
```