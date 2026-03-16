---
tags:
  - unity
---
用于自动调整UI元素的大小，以适应其内容的大小变化。它可以根据内容的大小自动调整UI元素的宽度和高度，确保内容不会被截断或溢出。

ContentSizeFitter组件通过监听UI元素的子元素的大小变化，自动调整UI元素的大小。它可以根据子元素的大小自动调整UI元素的宽度和高度，以确保子元素的内容不会被截断或溢出。

- Horizontal Fit：水平适应方式，可选值为Unconstrained（不限制）、Preferred Size（首选大小）和 Min Size（最小大小）。
- Vertical Fit：垂直适应方式，可选值为Unconstrained（不限制）、Preferred Size（首选大小）和 Min Size（最小大小）。


## 使用

配合 layout group 使用可以，自动根据子元素的排列，控制当前组件的大小