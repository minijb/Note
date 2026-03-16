---
tags:
  - opencv
---

# 基本操作

### 读取

`img = cv2.imread({path})`

数据类型 : 

![[python常见图片格式-读取方法-相互转换#Opencv]]

### 展示

```python
cv2.imshow({window_name}, {img})
# 窗口销毁
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 写入

`cv2.imwrite({filename}, img)`


### 转换

[[python常见图片格式-读取方法-相互转换#转换]]
