---
tags:
  - socket
---
## server

TCP Server 函数调用顺序

- socket 创建套接字
- bind 分配套接字地址
- listen  等待请求链接
- accept 允许链接
- read/write 数据交换
- close 关闭

**listen**  进入等待连接请求状态

```c++
int listen(int sockfd, int backlog);
//成功时返回0，失败时返回-1
//sock: 希望进入等待连接请求状态的套接字文件描述符，传递的描述符套接字参数称为服务端套接字
//backlog: 连接请求等待队列的长度，若为5，则队列长度为5，表示最多使5个连接请求进入队列
```

**accept** 受理客户端连接请求

```c++
#include <sys/socket.h>
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
/*
成功时返回文件描述符，失败时返回-1
sock: 服务端套接字的文件描述符
addr: 受理的请求中，客户端地址信息会保存到该指针指向的地址
addrlen: 该指针指向的地址中保存第二个参数的结构体长度
*/
```

> 注意：accept 函数返回的套接字不等于服务端套接字，也需要通过 close 函数关闭。

注意 这里自动生成的套接字会和连接请求 建立连接。

## client

顺序

- socket
- connect
- read/write
- close

## 迭代回声

- 服务器同一时刻只与一个客户端连接
- 一次向五个客户端提供服务并推出
- 一直执行一直到 Q 为止

```c++
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUF_SIZE 1024
void error_handling(char *message);

int main(int argc, char *argv[])
{
    int sock;
    char message[BUF_SIZE];
    int str_len;
    struct sockaddr_in serv_adr;

    if (argc != 3)
    {
        printf("Usage : %s <IP> <port>\n", argv[0]);
        exit(1);
    }

    sock = socket(PF_INET, SOCK_STREAM, 0);
    if (sock == -1)
        error_handling("socket() error");

    memset(&serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family = AF_INET;
    serv_adr.sin_addr.s_addr = inet_addr(argv[1]);
    serv_adr.sin_port = htons(atoi(argv[2]));

    if (connect(sock, (struct sockaddr *)&serv_adr, sizeof(serv_adr)) == -1)
        error_handling("connect() error!");
    else
        puts("Connected...........");

    while (1)
    {
        fputs("Input message(Q to quit): ", stdout);
        fgets(message, BUF_SIZE, stdin);

        if (!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
            break;

        write(sock, message, strlen(message));
        str_len = read(sock, message, BUF_SIZE - 1);
        message[str_len] = 0;
        printf("Message from server: %s", message);
    }
    close(sock);
    return 0;
}

void error_handling(char *message)
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}
```


```c++
// serve
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUF_SIZE 1024
void error_handling(char *message);

int main(int argc, char *argv[])
{
    int serv_sock, clnt_sock;
    char message[BUF_SIZE];
    int str_len, i;

    struct sockaddr_in serv_adr, clnt_adr;
    socklen_t clnt_adr_sz;

    if (argc != 2)
    {
        printf("Usage : %s <port>\n", argv[0]);
        exit(1);
    }

    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if (serv_sock == -1)
        error_handling("socket() error");

    memset(&serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family = AF_INET;
    serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_adr.sin_port = htons(atoi(argv[1]));

    if (bind(serv_sock, (struct sockaddr *)&serv_adr, sizeof(serv_adr)) == -1)
        error_handling("bind() error");

    if (listen(serv_sock, 5) == -1)
        error_handling("listen() error");

    clnt_adr_sz = sizeof(clnt_adr);
    //调用 5 次 accept 函数，共为 5 个客户端提供服务
    for (i = 0; i < 5; i++)
    {
        clnt_sock = accept(serv_sock, (struct sockaddr *)&clnt_adr, &clnt_adr_sz);
        if (clnt_sock == -1)
            error_handling("accept() error");
        else
            printf("Connect client %d \n", i + 1);

        while ((str_len = read(clnt_sock, message, BUF_SIZE)) != 0)
            write(clnt_sock, message, str_len);

        close(clnt_sock);
    }
    close(serv_sock);
    return 0;
}

void error_handling(char *message)
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}
```

但是「第二章」中说过「TCP 不存在数据边界」，上述客户端是基于 TCP 的，因此多次调用 write 函数传递的字符串有可能一次性传递到服务端。此时客户端有可能从服务端收到多个字符串，这不是我们想要的结果。还需要考虑服务器的如下情况：

「字符串太长，需要分 2 个包发送！」

服务端希望通过调用 1 次 write 函数传输数据，但是如果数据太大，操作系统就有可能把数据分成多个数据包发送到客户端。另外，在此过程中，客户端可能在尚未收到全部数据包时就调用 read 函数。

> 简单来说就是  客户端不知道需要接受多少

这里因为是回声，我们可以简单设置一个循环，只要接受到足够长度的信息就可以了

```cpp
    while (1)
    {
        fputs("Input message(Q to quit): ", stdout);
        fgets(message, BUF_SIZE, stdin);

        if (!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
            break;
        str_len = write(sock, message, strlen(message));

        recv_len = 0;
	    //循环读直到达到一定的数量
        while (recv_len < str_len)
        {
            recv_cnt = read(sock, &message[recv_len], BUF_SIZE - 1);
            if (recv_cnt == -1)
                error_handling("read() error");
            recv_len += recv_cnt;
        }
        message[recv_len] = 0;
        printf("Message from server: %s", message);
    }

```

### 如果问题不在于回声客户端：定义应用层协议

这时需要的是**应用层协议**的定义

```c++
// client
fputs("Operand count: ", stdout);
scanf("%d", &opnd_cnt);
opmsg[0] = (char)opnd_cnt;

for (i = 0; i < opnd_cnt; i++)
{
	printf("Operand %d: ", i + 1);
	scanf("%d", (int *)&opmsg[i * OPSZ + 1]);
}
fgetc(stdin);
fputs("Operator: ", stdout);
scanf("%c", &opmsg[opnd_cnt * OPSZ + 1]);
write(sock, opmsg, opnd_cnt * OPSZ + 2);
read(sock, &result, RLT_SIZE);
```

```c++
//serve
opnd_cnt = 0;
clnt_sock = accept(serv_sock, (struct sockaddr *)&clnt_adr, &clnt_adr_sz);
read(clnt_sock, &opnd_cnt, 1);

recv_len = 0;
while ((opnd_cnt * OPSZ + 1) > recv_len)
{
	recv_cnt = read(clnt_sock, &opinfo[recv_len], BUF_SIZE - 1);
	recv_len += recv_cnt;
}
result = calculate(opnd_cnt, (int *)opinfo, opinfo[recv_len - 1]);
write(clnt_sock, (char *)&result, sizeof(result));
close(clnt_sock);
```


**连接确认**

SYN 收发前的同步信息
-> seq : 1000  |  ack:-                在传 1000， 请向我传递 1001
SYN + ACK
<- seq : 2000  |  ack: 1001      在传 2000，请传 2001 ，刚刚传输的1000收到， 请传递 1001
ACK
-> seq : 1001  |  ack: 2001       在传 1001， 受到 2000， 请传 2001


**交换数据**

-> SEQ 1200 + 100byte

<- ACK 1301 ok

-> SEQ 1301  100byte

超重发知道返回 1402

**断开**

-> FIN SEQ 5000 ACK -
<- ACK SEQ 7500 ACK 5001
<- FIN SEQ 7501 ACK 5001
-> ACK SEQ 5001 ACK 7502

