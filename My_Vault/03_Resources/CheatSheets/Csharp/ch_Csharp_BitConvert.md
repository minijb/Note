
# BitConvert

主要分为两部分操作  字节->类型  类型->字节

**转换为字节**

`BitConvert.GetBytes(xxxx)`  
`BitConvert.xxToXXXBits()`

转化为具体类型

`BitConvert.ToBoolean()`


**大小端问题**

由 IsLittleEndian  决定

|               |             |
| ------------- | ----------- |
| Little-endian | D2-02-96-49 |
| Big-endian    | 49-96-02-D2 |
