 
同时，host与device之间可以进行通信，这样它们之间可以进行数据拷贝。典型的CUDA程序的执行流程如下：

1. 分配host内存，并进行数据初始化；
2. 分配device内存，并从host将数据拷贝到device上；
3. **调用CUDA的核函数在device上完成指定的运算；**
4. 将device上的运算结果拷贝到host上；
5. 释放device和host上分配的内存。


**Kernal**  在 device 上调用， 使用 `__global__` 进行生命，在调用时需要用`<<<grid, block>>>`来指定kernel要执行的线程数量

在CUDA中，每一个线程都要执行核函数，并且每个线程会分配一个唯一的线程号thread ID，这个ID值可以通过核函数的内置变量`threadIdx`来获得。

**区分 host 和 device**

- `__global__`：在device上执行，从host中调用（一些特定的GPU也可以从device上调用），返回类型必须是`void`，不支持可变参数参数，不能成为类成员函数。注意用`__global__`定义的kernel是异步的，这意味着host不会等待kernel执行完就执行下一步。
- `__device__`：在device上执行，单仅可以从device中调用，不可以和`__global__`同时用。
- `__host__`：在host上执行，仅可以从host上调用，一般省略不写，不可以和`__global__`同时用，但可和`__device__`，此时函数会在device和host都编译。


kernel在device上执行时实际上是启动很多线程，一个kernel所启动的所有线程称为一个**网格**（grid），同一个网格上的线程共享相同的全局内存空间，grid是线程结构的第一层次，而网格又可以分为很多**线程块**（block），一个线程块里面包含很多线程，这是第二个层次。

![pic](https://pic3.zhimg.com/v2-aa6aa453ff39aa7078dde59b59b512d8_1440w.jpg)

这是一个gird和block均为2-dim的线程组织。grid和block都是定义为dim3类型的变量，dim3可以看成是包含三个无符号整数`（x，y，z）`成员的结构体变量，在定义时，缺省值初始化为1。因此grid和block可以灵活地定义为1-dim，2-dim以及3-dim结构，对于图中结构（主要水平方向为x轴），定义的grid和block如下所示，kernel在调用时也必须通过执行配置`<<<grid, block>>>`来指定kernel所使用的线程数及结构。


```c++
dim3 grid(3, 2); // grid 内部为 3 * 2 
dim3 block(5, 3); // block 内部有  5 * 3
kernel_fun<<< grid, block >>>(prams...);
```

^958572

所以，一个线程需要两个内置的坐标变量（blockIdx，threadIdx）来唯一标识，它们都是`dim3`类型变量，其中blockIdx指明线程所在grid中的位置，而threaIdx指明线程所在block中的位置，如图中的`Thread (1,1)`满足：

```c++
threadIdx.x = 1
threadIdx.y = 1
blockIdx.x = 1
blockIdx.y = 1
```
一个线程块上的线程是放在同一个流式多处理器（SM)上的，但是单个SM的资源有限，这导致线程块中的线程数是有限制的，现代GPUs的线程块可支持的线程数可达1024个。有时候，我们要知道一个线程在blcok中的全局ID，此时就必须还要知道block的组织结构，这是通过线程的内置变量blockDim来获得。它获取线程块各个维度的大小 $block(D_x,D_y,D_z)$  线程(x, y,z) ID ：$x+y \times D_+ z \times D_y \times D_z$   另外线程还有内置变量gridDim，用于获得网格块各个维度的大小。

如我们将利用上图2-dim结构实现两个矩阵的加法，每个线程负责处理每个位置的两个元素相加，代码如下所示。线程块大小为(16, 16)，然后将`N*N`大小的矩阵均分为不同的线程块来执行加法运算。

```c
// Kernel定义
__global__ void MatAdd(float A[N][N], float B[N][N], float C[N][N]) 
{ 
    int i = blockIdx.x * blockDim.x + threadIdx.x; 
    int j = blockIdx.y * blockDim.y + threadIdx.y; 
    if (i < N && j < N) 
        C[i][j] = A[i][j] + B[i][j]; 
}
int main() 
{ 
    ...
    // Kernel 线程配置
    dim3 threadsPerBlock(16, 16); 
    dim3 numBlocks(N / threadsPerBlock.x, N / threadsPerBlock.y);
    // kernel调用
    MatAdd<<<numBlocks, threadsPerBlock>>>(A, B, C); 
    ...
}
```


### CUDA 内存模型

![img](https://pic2.zhimg.com/v2-6456af75530956da6bc5bab7418ff9e5_1440w.jpg)

每个线程有  local  memory ,   一个 block 内的线程共用一个 shared memory， **shared memory 的生命周期和线程块一只**，  Gloabl Menory --- > 所有线程都可以访问

还可以访问一些只读内存块：常量内存（Constant Memory）和纹理内存（Texture Memory）

> kernal  --> 启动的所有线程对应一个  -->  grid
> grid --> 分为很多 --> block
> block --> 包含很多 --> 线程


![[02_CUDA_硬件架构及编程基础#^958572]]


GPU硬件的一个核心组件是**SM**，前面已经说过，SM是英文名是 Streaming Multiprocessor，翻译过来就是流式多处理器。SM的核心组件包括CUDA核心，共享内存，寄存器等，SM可以并发地执行数百个线程，并发能力就取决于SM所拥有的资源数。


当一个kernal 被执行的时候，  grid 中的线程会被分配到 sm 上，  一个线程只能在一个 sm 中调度。  sm一般可以调度多个线程块。   此时  一个  kernal 会被分配到多个 sm。    grid 是数据层， sm 才是执行的物理层。

SM采用的是SIMT (Single-Instruction, Multiple-Thread，单指令多线程)架构，基本的执行单元是线程束（warps)，线程束包含32个线程，这些线程同时执行相同的指令，但是每个线程都包含自己的指令地址计数器和寄存器状态，也有自己独立的执行路径。所以尽管线程束中的线程同时从同一程序地址执行，但是可能具有不同的行为，比如遇到了分支结构，一些线程可能进入这个分支，但是另外一些有可能不执行，它们只能死等，因为GPU规定线程束中所有线程在同一周期执行相同的指令，线程束分化会导致性能下降。当线程块被划分到某个SM上时，它将进一步划分为多个线程束，因为这才是SM的基本执行单元，但是一个SM同时并发的线程束数是有限的


这是因为资源限制，SM要为每个线程块分配共享内存，而也要为每个线程束中的线程分配独立的寄存器。所以SM的配置会影响其所支持的线程块和线程束并发数量。总之，就是网格和线程块只是逻辑划分，一个kernel的所有线程其实在物理层是不一定同时并发的。所以kernel的grid和block的配置不同，性能会出现差异，这点是要特别注意的。还有，**由于SM的基本执行单元是包含32个线程的线程束，所以block大小一般要设置为32的倍数。**

![img](https://pic3.zhimg.com/v2-dcc0f678850d5bf1683753c34ca4b308_1440w.jpg)

  ```c
  int dev = 0;
    cudaDeviceProp devProp;
    CHECK(cudaGetDeviceProperties(&devProp, dev));
    std::cout << "使用GPU device " << dev << ": " << devProp.name << std::endl;
    std::cout << "SM的数量：" << devProp.multiProcessorCount << std::endl;
    std::cout << "每个线程块的共享内存大小：" << devProp.sharedMemPerBlock / 1024.0 << " KB" << std::endl;
    std::cout << "每个线程块的最大线程数：" << devProp.maxThreadsPerBlock << std::endl;
    std::cout << "每个EM的最大线程数：" << devProp.maxThreadsPerMultiProcessor << std::endl;
    std::cout << "每个SM的最大线程束数：" << devProp.maxThreadsPerMultiProcessor / 32 << std::endl;

    // 输出如下
    使用GPU device 0: GeForce GT 730
    SM的数量：2
    每个线程块的共享内存大小：48 KB
    每个线程块的最大线程数：1024
    每个EM的最大线程数：2048
    每个EM的最大线程束数：64
```



### 基本内存管理

```c
cudaError_t cudaMalloc(void** devPtr, size_t size);  // device 上 分配内存
cudaFree; // 释放内存

// host 和 device 之间通信的函数

cudaError_t cudaMemcpy(void* dst, const void* src, size_t count, cudaMemcpyKind kind); // dst 目标区域，  src  数据源， count  复制的字节数， 

// 其中kind控制复制的方向：cudaMemcpyHostToHost, cudaMemcpyHostToDevice, cudaMemcpyDeviceToHost及cudaMemcpyDeviceToDevice，如cudaMemcpyHostToDevice将host上数据拷贝到device上。
```

