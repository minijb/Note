

Job System 是Unity 内多线程编程工具。 为 Dots 的重要组成部分

**优势**

- 内置的安全检查
	- 原生多线程必须手动 lock，mutex等
	- jobSystem : 强制使用线程安全的容器
	- 所有权：住现场将数据所有权授予 Job 后， 在主线陈的 `JobHandle.Complete()` 调用之前，住现场不能访问这些数据， 从而避免读写冲突。

**Burst 编译**
- 原生 使用 `.Net` 编译
- Burst 专门为数学计算密集任务进行优化
	- 一般没有GC分配 --- Job的优势

**负载均衡的线程池**
- 实现"工作窃取"算法
- 提前完成了可以从其他线程偷一些工作来做

**隐式的依赖管理和同步**
- 原生使用 Task.Wait  continueWith 等机制来显示的等待
- Job System
	- 调度Job的时候会返回 `JobHandle` 我们可以将句柄传递给一个job， 作为知心的先决条件 `job2.Schedule(job1Handle)`
	- 系统会自动处理这些依赖， 不需要复杂的同步代码
	- 自动构建依赖链，易于管理

**和Unity深度集成**

- 在Job中执行纯计算。将不涉及引擎核心对象的计算如位置，物理，网格等放在job中进行
- 在主线程中引用结果， 通过 `NativeContainer` 作为桥梁， 在job完成后与 主线陈的 `JobHandle.Completre()` 调用之后安全的将计算结果取回应用到Unity对象中


### Dots

JobSytem : 多线程系统
Burst ： Burst llvm 的后端编译器 --- 很多代码都可以编译，但是有限定
Entity Component System ： 实体组件系统


### ECS

Entity-Component-System 分离数据及行为，优化内存布局，提高缓存利用率

1. Entity ID: 不包含任何数据和逻辑 用来标记组件是否属于同一事物
2. Component ： 纯粹的数据，没有任何方法， 在unity中就是 实现 `IComponentData` 接口的 Struct
3. System ： 纯粹的逻辑， 不存储任何数据， 系统会持续遍历特定组件组合的所有 实体，并根据这些数据执行操作。
	1. MovementSystem ， 会遍历所有 PositionComponet 和 VelocityComponent 实体，并在每一帧根据速度跟新它们的位置

### JobSystem 

可以在 非 Dots 环境下使用

