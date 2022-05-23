# Socket

## 1. TCP

`socket(family,type[,protocal])` 使用给定的地址族、套接字类型、协议编号（默认为0）来创建套接字。

| socket类型            | 描述                                                         |
| --------------------- | ------------------------------------------------------------ |
| socket.AF_UNIX        | 只能够用于单一的Unix系统进程间通信                           |
| socket.AF_INET        | 服务器之间网络通信                                           |
| socket.AF_INET6       | IPv6                                                         |
| socket.SOCK_STREAM    | 流式socket , for TCP                                         |
| socket.SOCK_DGRAM     | 数据报式socket , for UDP                                     |
| socket.SOCK_RAW       | 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。 |
| socket.SOCK_SEQPACKET | 可靠的连续数据包服务                                         |
| 创建TCP Socket：      | s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)           |
| 创建UDP Socket：      | s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)            |

### 函数

| socket函数                           | 描述                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| 服务端socket函数                     |                                                              |
| s.bind(address)                      | 将套接字绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址. |
| s.listen(backlog)                    | 开始监听TCP传入连接。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。 |
| s.accept()                           | 接受TCP连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。 |
| 客户端socket函数                     |                                                              |
| s.connect(address)                   | 连接到address处的套接字。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。 |
| s.connect_ex(adddress)               | 功能与connect(address)相同，但是成功返回0，失败返回errno的值。 |
| 公共socket函数                       |                                                              |
| s.recv(bufsize[,flag])               | 接受TCP套接字的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。 |
| s.send(string[,flag])                | 发送TCP数据。将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。 |
| s.sendall(string[,flag])             | 完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。 |
| s.recvfrom(bufsize[.flag])           | 接受UDP套接字的数据。与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。 |
| s.sendto(string[,flag],address)      | 发送UDP数据。将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。 |
| s.close()                            | 关闭套接字。                                                 |
| s.getpeername()                      | 返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。  |
| s.getsockname()                      | 返回套接字自己的地址。通常是一个元组(ipaddr,port)            |
| s.setsockopt(level,optname,value)    | 设置给定套接字选项的值。                                     |
| s.getsockopt(level,optname[.buflen]) | 返回套接字选项的值。                                         |
| s.settimeout(timeout)                | 设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如connect()） |
| s.gettimeout()                       | 返回当前超时期的值，单位是秒，如果没有设置超时期，则返回None。 |
| s.fileno()                           | 返回套接字的文件描述符。                                     |
| s.setblocking(flag)                  | 如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。 |
| s.makefile()                         | 创建一个与该套接字相关连的文件                               |

客户端

```python
import socket

phone = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

phone.connect(('127.0.0.1',8848))
data = 'new'

phone.send(data.encode('utf-8'))
data = phone.recv(1024)
print(f"from server {data}")
phone.close()
```

服务端

```python
import socket

phone = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
phone.bind(('127.0.0.1',8848))
#开始监听
phone.listen(5)
print(111)

#此步会阻塞 直到有链接接入
conn, addr = phone.accept()

print(conn,addr)

data = conn.recv(1024)
print(f"from client {data}")

conn.send(data.upper())
conn.close()
phone.close()
```

phone,conn既是对象也是一个管道可以用来接收信息

### 循环输入

```python
#serve
import socket
import time
phone = socket.socket()
phone.bind(('127.0.0.1',8848))


#开始监听
phone.listen()


conn ,addr = phone.accept()
print(addr)

while 1:
    try:
        data = conn.recv(12)
        print(f"from client : {data}")
        if data.upper() == b'Q':
            break
        recv_data = input('>>>').strip().encode('utf-8')
        conn.send(recv_data)
    except Exception as e:
        print('结束')
        break
conn.close()
phone.close()



#client
import socket
import time

phone = socket.socket()

phone.connect(('127.0.0.1',8848))
while 1:
    
    data = input('>>>').strip().encode('utf-8')
    phone.send(data)
    if data.upper()==b'Q':
        break
    recv_data = phone.recv(1024)
    
    print(f"from server {recv_data}")

phone.close()

```

### 服务算同时连接多个客户端

```python
import socket
import time
phone = socket.socket()
phone.bind(('127.0.0.1',8848))


#开始监听,做多同时监听5个
phone.listen(5)

while 1:
    conn ,addr = phone.accept()
    print(addr)

    while 1:
        try:
            data = conn.recv(12)
            print(f"from client : {data}")
            if data.upper() == b'Q':
                break
            recv_data = input('>>>').strip().encode('utf-8')
            conn.send(recv_data)
        except Exception as e:
            print('结束')
            break
    conn.close()
phone.close()
```

- 可以同时监听但是，只有再一个链接失效了，才可以和其他链接通话

### subprocess模块

subprocess 模块允许我们启动一个新进程，并连接到它们的输入/输出/错误管道，从而获取返回值

```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None)
```

- args：表示要执行的命令。必须是一个字符串，字符串参数列表。
- stdin、stdout 和 stderr：子进程的标准输入、输出和错误。其值可以是 subprocess.PIPE、subprocess.DEVNULL、一个已经存在的文件描述符、已经打开的文件对象或者 None。subprocess.PIPE 表示为子进程创建新的管道。subprocess.DEVNULL 表示使用 os.devnull。默认使用的是 None，表示什么都不做。另外，stderr 可以合并到 stdout 里一起输出。
- timeout：设置命令超时时间。如果命令执行时间超时，子进程将被杀死，并弹出 TimeoutExpired 异常。
- check：如果该参数设置为 True，并且进程退出状态码不是 0，则弹 出 CalledProcessError 异常。
- encoding: 如果指定了该参数，则 stdin、stdout 和 stderr 可以接收字符串数据，并以该编码方式编码。否则只接收 bytes 类型的数据。
- shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令。

```py
import subprocess

obj = subprocess.Popen(
    'ls -l',
    shell= True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
#相当于调用一个终端进程执行命令
msg = obj.stdout.read()
if msg !=None:
    print(msg.decode('utf-8'))
```

### 缓冲区和粘包

如果缓冲区没有清空  那么recv只会读取缓冲区的内容，那么服务器和客户端的交流可能出现断层，这既是粘包现象(尤其是将一个数据分割很小的包连续输出)

缓冲区分为输入缓冲区和输出缓冲区

- read,recv
- write,send



- 一般缓冲区大小为8*1024



粘包

- 接收方没有及时接收缓冲包，造成多宝接收
- 发送端需要等待缓冲区满才发送，造成粘包（时间间隔短，每次数据少）

#### 解决方法

接收数据时循环接收

##### 方案一

在发具体数据前，发送总长度，之后发送总数居

```python
#方案1

#server
import socket
import subprocess

ipadr = '127.0.0.1'
port = 8848

phone = socket.socket()
phone.bind((ipadr,port))
phone.listen(2)

while 1:
    conn , addr  = phone.accept()

    while 1 :
        try:
            from_client = conn.recv(1024)
            from_origin = from_client.decode('utf-8')
            if from_origin.upper() == "Q":
                print('退出链接')
                break

            terminal_text = subprocess.Popen(
                from_origin,
                shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )

            result = terminal_text.stdout.read()+terminal_text.stderr.read()
            result_num = len(result)
            print(result_num)

            conn.send(str(result_num).encode('utf-8'))
            conn.send(result)
        except Exception as e :
            print(e)
            break
    conn.close()
phone.close()

```

- 问题：直接发送的话两次send会发生粘包！！！！！！  那么就不知道发送的是数据还是数量
- 解决方法：将不固定长度的int转化为固定长度的byte，并且可以转换，使用struct模块

```python
import struct

ret = struct.pack('i',12345)
print(ret , type(ret),len(ret))#len=4

'''
i  int
I unsigned int
l long
L uns long
q long long
'''

n = struct.unpack('i', ret)[0]
print(n)
```

```python
#server
import socket
import struct
import subprocess

ipadr = '127.0.0.1'
port = 8848

phone = socket.socket()
phone.bind((ipadr,port))
phone.listen(2)

while 1:
    conn , addr  = phone.accept()

    while 1 :
        try:
            from_client = conn.recv(1024)
            from_origin = from_client.decode('utf-8')
            if from_origin.upper() == "Q":
                print('退出链接')
                break

            terminal_text = subprocess.Popen(
                from_origin,
                shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )

            result = terminal_text.stdout.read()+terminal_text.stderr.read()
            result_num = len(result)
            print(result_num,end=' => ')

            result_num_struct = struct.pack('i',result_num)
            print(f"{result_num_struct}  len:{len(result_num_struct)}")
            conn.send(result_num_struct)
            conn.send(result)
        except Exception as e :
            print(e)
            break
    conn.close()
phone.close()


#  client
import socket
import struct

phone = socket.socket()
phone.connect(('127.0.0.1',8848))

phone.send('ls -l'.encode('utf-8'))
length =  struct.unpack('i',phone.recv(4))[0]
print(length)
data = b""
while len(data) < length :
    data += phone.recv(200)

print(data.decode('utf-8'))

```

##### 方案二

自制报头！！！！自制协议

`dic={'filename':xx , 'md5':xxxx,'total_size':xxxxx}`

可以解决文件过大的问题

```python
import socket
import struct
import subprocess
import json

ipadr = '127.0.0.1'
port = 8848

phone = socket.socket()
phone.bind((ipadr,port))
phone.listen(2)

conn , addr  = phone.accept()

try:
    from_client = conn.recv(1024)
    from_origin = from_client.decode('utf-8')
    if from_origin.upper() == "Q":
        print('退出链接')

    terminal_text = subprocess.Popen(
        from_origin,
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    result = terminal_text.stdout.read()+terminal_text.stderr.read()
    result_num = len(result)
    print(result_num,end=' => ')

    head_dic = {
        'file_name' : 'test1',
        'md5':6512398172398,
        'total_size': total_size,
    }
    head_dic_json_b = json.dumps(head_dic).encode('utf-8')

    conn.send(head_dic_json_b)#报头不固定
    conn.send(result)
except Exception as e :
    print(e)

conn.close()
phone.close()
```

- 这样的话 包头不固定！！！！

接下来的问题是如何制作固定的报头

那就再添加一个报头的长度！！！！

`====报头长度====报头====内容====`

报头长度是固定的，

> 感觉可以模拟http协议每一段的报头每一段的长度是固定的，包头内的长度为报文总长度

- 如何解决文件过大：1024*1024.。。。转化为字典的一项，并说明将字典的长度作为报头的长度

```python
#server
import socket
import struct
import subprocess
import json

ipadr = '127.0.0.1'
port = 8848

phone = socket.socket()
phone.bind((ipadr,port))
phone.listen(2)

conn , addr  = phone.accept()

try:
    from_client = conn.recv(1024)
    from_origin = from_client.decode('utf-8')
    if from_origin.upper() == "Q":
        print('退出链接')

    terminal_text = subprocess.Popen(
        from_origin,
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    result = terminal_text.stdout.read()+terminal_text.stderr.read()
    result_num = len(result)

    head_dic = {
        'file_name' : 'test1',
        'md5':6512398172398,
        'total_size': result_num,
    }
    head_dic_json_b = json.dumps(head_dic).encode('utf-8')

    head_len_b = struct.pack('i',len(head_dic_json_b))
    conn.send(head_len_b)
    conn.send(head_dic_json_b)#报头不固定
    conn.send(result)
except Exception as e :
    print(e)

conn.close()
phone.close()


#client
import socket
import struct
import json

phone = socket.socket()
phone.connect(('127.0.0.1',8848))

phone.send('cat server.py'.encode('utf-8'))
length =  struct.unpack('i',phone.recv(4))[0]
print(length)

#head
head_b = phone.recv(length).decode('utf-8')
print(head_b)
head = json.loads(head_b)

head_filename =  head['file_name']
head_size = head['total_size']


data = b""
while len(data) < head_size :
    data += phone.recv(200)

print(f"file_size : {head_size}")
print("="*6,"data","="*6,sep=' ')
print(data.decode('utf-8'))

```

## 2. UDP

- `socket.recvform()`

Receive data from the socket. The return value is a pair `(bytes, address)` where *bytes* is a bytes object representing the data received and *address* is the address of the socket sending the data

- socket.sendto(bytes, flags, address)---flag可选

Send data to the socket. The socket should not be connected to a remote socket, since the destination socket is specified by *address*. The optional *flags* argument has the same meaning as for [`recv()`](https://devdocs.io/python~3.9/library/socket#socket.socket.recv) above. Return the number of bytes sent. (The format of *address* depends on the address family — see above.)

```python
import socket

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server.bind(('127.0.0.1',9000))

while 1:
    data = server.recvfrom(1024)[0]
    print(data.decode('utf-8'))
    # to_client = input('>>>>')


    
#client
import socket

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#client.connect(('127.0.0.1',9000))
#UDP无需建立链接/管道，客户端和服务端没有开启的先后顺序
while 1:
    data = input(">>>>")
    client.send(data.encode('utf-8'))

```

有过想要原理返回的话 那么就需要使用recvfrom来得到源ip和端口

只要有ip和端口就可以发送消息！！
