---
title: CUDA 硬件架构与编程
date: 2026-03-16
tags:
  - cuda
  - gpu
  - architecture
type: hardware
aliases:
  CUDA架构
description: CUDA硬件架构及编程基础
draft: false
---


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

