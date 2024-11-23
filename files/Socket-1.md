---
tags:
  - socket
---
https://github.com/riba2534/TCP-IP-NetworkNote/tree/master/ch01

## 创建套接字

**server** 接电话

- 使用 `socket` 创建套接字
- `bind`  绑定ip 和 port
- `listen`  将套接字转为可接受链接状态
- `accept` 接受连接请求，如果没有链接，则会阻塞。

**client** 打电话

- `socket` 创建
- `connect` 打电话

> 常用文件描述符 : 0 , 1, 2 标准输入，标准输出，标准错误

### linux 文件

**打开**

`int open(const char *path, int flag);`

flag 打开模式

|   打开模式   |      含义       |
| :------: | :-----------: |
| O_CREAT  |    必要时创建文件    |
| O_TRUNC  |   删除全部现有数据    |
| O_APPEND | 维持现有数据，保存到其后面 |
| O_RDONLY |     只读打开      |
| O_WRONLY |     只写打开      |
|  O_RDWR  |     读写打开      |
**关闭**

`int close(int fd);`

**写入**

`ssize_t write(int fd, const void *buf, size_t nbytes);`

buf : 保存要传输数据的缓冲值地址
nbytes : 要传输数据的字节数

**读取**

```c++
ssize_t read(int fd, void *buf, size_t nbytes);
/*
成功时返回接收的字节数（但遇到文件结尾则返回 0），失败时返回 -1
fd : 显示数据接收对象的文件描述符
buf : 要保存接收的数据的缓冲地址值。
nbytes : 要接收数据的最大字节数
*/
```

## 套接字

`int socket(int domain, int type, int protocol);`

**第一个参数 ： protocol family** 协议簇

| 名称        | 协议族           |
| --------- | ------------- |
| PF_INET   | IPV4 互联网协议族   |
| PF_INET6  | IPV6 互联网协议族   |
| PF_LOCAL  | 本地通信 Unix 协议族 |
| PF_PACKET | 底层套接字的协议族     |
| PF_IPX    | IPX Novel 协议族 |


> 头文件 `sys/socket.h`

**第二个参数 ： 套接字类型**

SOCK_STREAM  --- 面向连接的套接字

传输方式特征整理如下：

- 传输过程中数据不会消失
- 按序传输数据
- 传输的数据不存在数据边界（Boundary）

SOCK_DGRAM   面向消息的套接字

- 强调快速传输而非传输有序
- 传输的数据可能丢失也可能损毁
- 传输的数据有边界
- 限制每次传输数据的大小

**不可靠的、不按序传递的、以数据的高速传输为目的套接字。**

**第三个参数 协议的最终选择** -- TCP/UDP

IPPROTO_TCP， IPPROTO_UDP

**TCP client 修改** --- 修改 read 方式

```c++
while (read_len = read(sock, &message[idx++], 1))
{
	if (read_len == -1)
		error_handling("read() error!");
	str_len += read_len;
}
```

有了 sock 就可以多次进行读

### 表示地址信息

```c++
struct sockaddr_in
{
    sa_family_t sin_family;  //地址族（Address Family）
    uint16_t sin_port;       //16 位 TCP/UDP 端口号
    struct in_addr sin_addr; //32位 IP 地址
    char sin_zero[8];        //不使用
};

struct in_addr
{
    in_addr_t s_addr; //32位IPV4地址
}

// client
serv_addr.sin_family = AF_INET;
serv_addr.sin_addr.s_addr = inet_addr(argv[1]);
serv_addr.sin_port = htons(atoi(argv[2]));

//server

serv_addr.sin_family = AF_INET;
serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
serv_addr.sin_port = htons(atoi(argv[1]));
```


| 地址族（Address Family） | 含义                   |
| ------------------- | -------------------- |
| AF_INET             | IPV4用的地址族            |
| AF_INET6            | IPV6用的地址族            |
| AF_LOCAL            | 本地通信中采用的 Unix 协议的地址族 |

- 成员 sin_port
    
    该成员保存 16 位端口号，重点在于，它以网络字节序保存。
    
- 成员 sin_addr
    
    该成员保存 32 位 IP 地址信息，且也以网络字节序保存
    
- 成员 sin_zero
    
    无特殊含义。只是为结构体 sockaddr_in 结构体变量地址值将以如下方式传递给 bind 函数。



```C++

//

if (bind(serv_sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
    error_handling("bind() error");

struct sockaddr
{
    sa_family_t sin_family; //地址族
    char sa_data[14];       //地址信息
}
```

> atoi --- 字符串转int

### 字节序列转换

unsigned short htons(unsigned short);
unsigned short ntohs(unsigned short);
unsigned long htonl(unsigned long);
unsigned long ntohl(unsigned long);

- htons 的 h 代表主机（host）字节序。
- htons 的 n 代表网络（network）字节序。
- s 代表两个字节的 short 类型，因此以 s 为后缀的函数用于端口转换
- l 代表四个字节的 long 类型，所以以 l 为后缀的函数用于 IP 地址转换

将字符串信息转换为网络字节序的整数型

`in_addr_t inet_addr(const char *string); //成功时返回 32 位大端序整数型值，失败时返回 INADDR_NONE`


```c++
#include <arpa/inet.h>
int inet_aton(const char *string, struct in_addr *addr);
/*
成功时返回 1 ，失败时返回 0
string: 含有需要转换的IP地址信息的字符串地址值
addr: 保存转换结果的 in_addr 结构体变量的地址值
*/
```

inet_aton 函数与 inet_addr 函数在功能上完全相同，也是将字符串形式的IP地址转换成整数型的IP地址。只不过该函数用了 in_addr 结构体，且使用频率更高。

```c++
char *inet_ntoa(struct in_addr adr);
//成功时返回保存转换结果的字符串地址值，失败时返回 NULL 空指针
```

还有一个函数，与 inet_aton() 正好相反，它可以把网络字节序整数型IP地址转换成我们熟悉的字符串形式，函数原型如下：

**网络地址初始化**

```c++
struct sockaddr_in addr;
char *serv_ip = "211.217,168.13";          //声明IP地址族
char *serv_port = "9190";                  //声明端口号字符串
memset(&addr, 0, sizeof(addr));            //结构体变量 addr 的所有成员初始化为0
addr.sin_family = AF_INET;                 //制定地址族
addr.sin_addr.s_addr = inet_addr(serv_ip); //基于字符串的IP地址初始化
addr.sin_port = htons(atoi(serv_port));    //基于字符串的IP地址端口号初始
```


**INADDR_ANY** 0.0.0.0
