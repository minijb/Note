
[[UniFileContext]] 外层壳子， 主要用来进行序列化和反序列化

HEAD ： 

```c#
//tag 4 byte
//version 8 byte
//flag 4 byte
//type 1 byte
//extend 2 byte
//datalength 4 byte
public const int HEAD_LENGTH = 4 + 8 + 4 + 1 + 2 + 4;
```

很多信息放在 meta 中， 比如压缩信息，是否公开，时间，类型等等等


json 解析过程 ： 

1. 添加 不同 Data 之间添加注释

**转化为 二进制 `toRawData` ：**

利用 MemoryStream 进行二进制处理。

1. seek到头后面
2. 序列化 meta 信息
3. 序列化具体信息
	1. 使用 `LZ4Codec.Encode` 进行压缩后添加到mem后面
4. 加入头信息

**二进制文件的比较和补丁**

使用 **Bsdiff** 库进行 (这个库原本是c++的同时有用C sharp 重写的)

Bsdiff 的好处就是可以很简单的进行增量更新

```c#
public static bool DiffContent(byte[] oriFullRawData, byte[] newFullRawData,out byte[] diffRawData)
{
	diffRawData = null;
	byte[] oriDBuffer = null;
	int oriHeadLen = 0;
	byte[] newDBuffer = null;
	int newHeadLen = 0;
	bool ok = Decompress(oriFullRawData, 0, oriFullRawData.Length, out oriDBuffer, out oriHeadLen);
	ok = ok && Decompress(newFullRawData, 0, newFullRawData.Length, out newDBuffer, out newHeadLen);
	if (ok)
	{
		System.IO.MemoryStream ms = new MemoryStream();
		BsDiff.BinaryPatchUtility.Create(oriDBuffer,oriHeadLen,oriDBuffer.Length - oriHeadLen,newDBuffer,newHeadLen,newDBuffer.Length-newHeadLen,ms);
		ms.Flush();
		diffRawData = ms.ToArray();
	}
	return ok;
}

public static bool MergeContent(byte[] oriFullRawData, byte[] patchFullRawData, out byte[] mergeRawData)
{
	mergeRawData = null;
	byte[] oriDBuffer = null;
	int oriHeadLen = 0;
	bool ok = Decompress(oriFullRawData, 0, oriFullRawData.Length, out oriDBuffer, out oriHeadLen);
	if (ok)
	{
		System.IO.MemoryStream ms = new MemoryStream(oriDBuffer, oriHeadLen, oriDBuffer.Length - oriHeadLen);
		System.IO.MemoryStream outStream = new MemoryStream();
		outStream.Write(oriDBuffer,0,oriHeadLen);
		BsDiff.BinaryPatchUtility.Apply(ms, () => { return new MemoryStream(patchFullRawData);},outStream);
		outStream.Flush();
		mergeRawData = outStream.ToArray();
	}
	return ok;
}
```


**解压缩同理**

**具体的序列化和反序列化**

```c#

        public static void Serialize(System.IO.Stream stream, UniNodeData data,ref UniFileContext context)
        {
            int beginPosition = (int)stream.Position;
            stream.Seek(4, System.IO.SeekOrigin.Current);
            if(data != null)
            {
                var ctx = new UniSerializationCtx();
                ProtoWriter writer = new ProtoWriter(stream, Uni.Data.UniTypeModel.ProtoModel, new SerializationContext(){Context = ctx});
                ctx.Writer = writer;
                writer.SetRootObject(data);
                UniNodeWriter.Serialize(writer, data,ref context);
                writer.Close();
                stream.Flush();
            }
            int currPos = (int)stream.Position;
            stream.Seek(beginPosition, System.IO.SeekOrigin.Begin);
            int len = currPos - beginPosition - 4;
            stream.WriteInt32LE(len);
            stream.Seek(currPos, System.IO.SeekOrigin.Begin);


        }
        public static UniNodeData Deserialize(System.IO.Stream stream,ref UniFileContext context)
        {
            var ctx = new UniSerializationCtx();
            var reader = new ProtoReader(stream, Uni.Data.UniTypeModel.ProtoModel, new SerializationContext(){Context = ctx});
            ctx.Reader = reader;
            ctx.Context = context;
            return UniNodeReader.Deserialize(reader, ref context);
        }
        public static UniNodeData DeserializeLegacy(System.IO.Stream stream, ref UniFileContext context)
        {
            var ctx = new UniSerializationCtx();
            ProtoBuf.ProtoReader reader = new ProtoBuf.ProtoReader(stream, Uni.Data.UniTypeModel.ProtoModel, new SerializationContext(){Context = ctx});
            ctx.Reader = reader;
            ctx.Context = context;
            var node = UniLegacyNodeReader.Deserialize(reader, ref context, context.Meta.Version);
            return node;
        }
```