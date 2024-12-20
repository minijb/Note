---
tags:
  - unity
---
Unity中的材质属性被序列化以后，就会一直存储在资源中，即使该属性删除后，它的序列化值以及引用关系也不会被丢掉，所以我们经常会发现，当我们使用一个和之前命名相同的属性时，原来的属性值或资源就会被自动赋值，这是因为材质中一直保持这种关系；但是，有些时候我们为了优化或者其它需求，想要去清理掉这些引用关系，如下，给出了清理某个文件夹下所有材质过期属性的一个工具；

因此 SerializedProperty 表示一种实例化的关系, 需要配合 editor 类使用

https://docs.unity.cn/cn/2019.4/Manual/editor-CustomEditors.html
https://docs.unity.cn/cn/2023.2/Manual/ExtendingTheEditor.html

