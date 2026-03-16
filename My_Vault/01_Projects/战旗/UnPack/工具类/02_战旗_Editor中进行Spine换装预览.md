
### 1. 简单换装预览

注意：Editor 模式下修改 Scene 中的物体会出现延迟！！！！


此时： 通过聚焦对应的物体来实现刷新的更新

```C#
Selection.activeGameObject = obj;
SceneView.lastActiveSceneView.FrameSelected();
```

### 2. 如果使用 renderTexture 进行拍摄

以上的方法还是存在延迟！！！   使用同步方法速度太快， 拍摄出的东西存在问题 --- 来不及更新显示原始图像。

解决方法： 使用 UniTask 进行更新

```c#
public async UniTask<Texture2D> GetTextureFromTempEnv(CharBust_Asset asset)
{
	if (asset.texture is not null) return asset.texture;

	if (temp_Env.tempRenderTexture is null)
	{
		Debug.LogError("tempEnv : renderTexture is null");
		return null;
	}
	// 进过测试 使用 0.5s 就可以
	await UniTask.Delay(500);
	RenderTexture pre = RenderTexture.active;
	RenderTexture.active = temp_Env.tempRenderTexture;

	Texture2D texture2D = new Texture2D(
		renderTexture.width,
		renderTexture.height,
		TextureFormat.RGBA32,
		false
	);
	// SelectTempEnvObject();
	temp_Env.tempCamera.Render();
	texture2D.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
	texture2D.Apply();
	asset.texture = texture2D;

	RenderTexture.active = pre;
	return texture2D;
}
```

### 3. Editor 中遇到的问题

1. 进行随机以及重置的时候 --- 应为当前聚焦于文本框  无法删除

```c#
// 删除聚焦
GUI.FocusControl(null);
RandomSelect();
Repaint();
Debug.Log("随机生成");
```


2. 文本框没有自动记忆功能

需要自己添加缓存 --- 推荐使用 一个 Dic 进行存储

### 4. 自适应

positon --- 为 EdtiorWindow 的当前大小

```c#
float WINDOW_W = Mathf.Max(PreviewPanelW, position.width - GridPanelW - ScrollBarW - LabelH);
float WINDOW_H = Mathf.Max(PreviewPanelW, position.height - LabelH * 3f);
EditorGUILayout.BeginVertical(EditorStyles.helpBox, GUILayout.Width(WINDOW_W));
{
	Rect previewRect = GUILayoutUtility.GetRect(WINDOW_W, WINDOW_H);
```

### 5. 如何生成网格状的 EditorWindow

1. thumbnailSize --- 网格大小

```c#
private void DrawImageList()
{
	EditorGUILayout.BeginVertical(EditorStyles.helpBox,  GUILayout.Width(windowW + ScrollBarW));
	{

		scrollPosition = EditorGUILayout.BeginScrollView(scrollPosition, GUILayout.Width(windowW + ScrollBarW));
		{
			GUILayout.BeginVertical();
			{
			// 首先每行多少个
				int columns = Mathf.FloorToInt(windowW / thumbnailSize);
				for (int i = 0; i < imageInfos.Count; i += columns)
				{
					GUILayout.BeginHorizontal();
					{
						for (int j = 0; j < columns; j++)
						{
							int index = i + j;
							if (index >= imageInfos.Count) break;
							DrawTextureButton(imageInfos[index]);
						}
					}
					GUILayout.EndHorizontal();
				}
			}
			GUILayout.EndVertical();
		}
		EditorGUILayout.EndScrollView();
	}
	EditorGUILayout.EndVertical();
}
```


```c#
private void DrawTextureButton(ImageInfo imageInfo)
{
	if (imageInfo.texture == null) return;
	// 确定内容
	GUIContent content = new GUIContent
	{
		image = imageInfo.texture,
		text = imageInfo.asset.ID.ToString()
	};
	// 确定样式
	GUIStyle btnStyle = new GUIStyle(GUI.skin.button)
	{
		alignment = TextAnchor.LowerCenter,
		imagePosition = ImagePosition.ImageAbove,
		fixedWidth = thumbnailSize,
		fixedHeight = thumbnailSize-50f
	};
	// 按钮功能
	if (GUILayout.Button(content, btnStyle))
	{
		selectedImageInfo = imageInfo;
	}
	if (selectedImageInfo_style == imageInfo)
	{
		Rect rect = GUILayoutUtility.GetLastRect();
		EditorGUI.DrawRect(rect, new Color(0, 0.15f, 0.62f, 0.3f));
	}
	// 实现按钮功能
	if (selectedImageInfo == imageInfo)
	{
		windowCallback?.Invoke(imageInfo.asset);
		father.previewWindow_1 = null;
		father.previewWindow_2 = null;
		Close();
	}
}
```