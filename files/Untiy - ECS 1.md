---
tags:
  - unity
  - ECS
---
## ECS

优势：


1. 优化数据的存储和处理
2. 数据分离！！！！！
3. 数据存储是连续的！！！ --- 最大化cpu hit
4. 可以添加或者移除 components and function

DotS : Data Oriented Technology Stack
- Entities ECS
- Job System
- Burst Compiler
- Math

## ECS

**Entities**

- 仅仅是一组Index。
- 将数据进行分组并分配给一个东西
- 每一个 ， 多个组件的组合 就是一个原型

**Components**

- 实际数据 -- 绑定在 Entity 上
- 静态或者动态数据
- 存储在块(chunk)中 --- 16KB
- 相同原型的数据会被存储在一个 chunk中

**System**

- 数据操作
- 在多组 Entities 中运行
- 通过 Entity Queries 得到 Entites Groups
- SystemUpdate order --- system 更新规则

**Player Loop**

每帧有以下部分
- 初始化 Group
- 同化 Group --- 主要部分
- Presentation Group