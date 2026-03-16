---
tags:
  - unity
---
**维持平衡：**  冻结部分轴，挂一个 box collider

如何控制 wheelCollider 的转动 --- `GetWorldPose(out v3 pos, out Quat quat)` 得到世界位置和旋转。

**判断转向：** 鼠标在屏幕的位置，来判断左转还是右转。 `Input.mousePosition.x > Screen.width * 0.5f`

**旋转 :**  `Quaternion.RotateTowards` 进行差值旋转。

https://blog.csdn.net/weixin_43147385/article/details/124266796  一些小车的控制。


## 柏林噪声 perlin

使用 Line 进行 简单的可视化 --- `LineRender`  通过 `SetPositoin` 控制位置

生成柏林噪声 `Mathf.PerlinNoise(x,y)` x,y 对应的采样点坐标  --- 默认没有随机。 可以手动添加随机。

**柏林噪声原理**:  TODO


## 地形创建

`WorldGenerator`  类。  `CreateCylinder`  函数创建地形


`Mesh`  网格  `MeshFilter` 持有mesh引用， `MeshRenderer` 渲染mesh



```c#



public vector2 dimensions;
public int scale;
public float perlinScale;
public float offset;
public int waveHeight;


public GameObject CreateCylinder()
{
	// 先创建一个主物体
	GameObject newCylinder = new GameObjcet();
	

	
	// 添加网络
	MeshFilter meshFilter = newCylinder.AddComponent<MeshFilter>();
	MeshFilter meshRender = newCylinder.AddComponent<MeshRender>();
	
	// 添加材质
	meshRender.material = meshMaterial;
	
	meshFilter.mesh = Generate();
	
	// 添加一个碰撞器
	newCylinder.AddComponent<MeshCollider>();
}

Mesh Generate(){
	Mesh mesh = new Mesh();
	mesh.name = "MESH";

	// 顶点 ， uv ， 三角形等

	Vector3[] vertices = null;
	Vector2[] uvs = null;
	int[] triangles = null;

	// 创建形状
	CreateShape(ref vectices, ref uvs, ref triangles);

	// 赋值
	mesh.vertices = vertices;
	mesh.uv = uvs;
	mesh.triangles = triangles;
	mesh.RecalculateNormals(); // 重新生成法向量

	return mesh;
	
}

void CreateShape(ref Vector3[]  vectices, ref Vector2[] uvs,int[] ref triangles){
	// 向z轴延申。  x轴位横截面， 
	int xCount = (int) dimensions.x;
	int zCount = (int) dimensions.y;

	vectices = new Vector3[(xCount+1) * (zCount + 1)];
	uvs = new Vector2[(xCount+1) * (zCount + 1)];

	// 半径
	float radius = xCount * scale * 0.5f;
	int index = 0;
	// 双循环设置顶点
	for(int x = 0 ; x <= xCount ; x++){
		for(int z = 0 ; z <= zCount; z++){
			// 获取圆柱体的角度
			float angle = x * Mathf.PI * 2f / xCount;
			vectices[index] = new Vector3(Mathf.Cos(angle) * radius, Mathf.Sin(angle) * radius, z * scale * Mathf.PI);
			uvs[index] = new Vector2(x*scale, z*scale);


			// 使用柏林噪声
			float pX = (vectices[index].x * perlienScale) + offset;
			float pZ = (vectices[index].z * perlienScale) + offset;
			// 需要一个中心点和当前定期那做减法
			Vector3 center = new Vector3(0,0, vertices[index].z);
			vertices[index] += (center - vertices[index]).normalized * Mathf.PerlinNoise(pX,pY) * waveHeight; 

			index++;
		}
	}

	//总数 ： x * z 1个矩形2个三角形， 1个性较小三个顶点， 一个矩形 5个顶点。。
	triangles = new int[xCount * zCount * 6];

	int[] boxBase = new int[6];


	int current = 0；
	for(int x = 0 ; x < xCount; x++){
		boxBase = new int[]{
			x * (zCount + 1),
			x * (zCount + 1) + 1,
			(x + 1) * (zCount + 1) + 1,
			x * (zCount + 1) + 1,
			(x + 1) * (zCount + 1) + 1,
			(x + 1) * (zCount + 1)
		};
		for( int  z = 0 ; z < zCount ; z++){
			
			for(int i = 0 ; i < 6 ; i++){
				boxBase[i] = boxBase[i] + 1;
			}
			for(int i = 0 ; i < 6 ; i++){
				boxBase[current + j] = boxBase[j] - 1;
			}
			current += 6;
		}
	}

}

```


## 移动地形


`transform.Translate(Vector3.forward * moveSpeed * time.deltaTime);`


## 地形的滚动

```c#
void Start(){
	for(int i = 0 ; i < 2 ; i++){
		GenmerateWorldPiece(i);
	}
}

public GameObject[] pieces = new GameObject[2]; //方便操作

void GenmerateWorldPiece(int i){
	pieces[i] = CreateCylinder();
	//根据索引，
	pieces[i].transform.Translate(v3.forward * (dimension.y * scale * Mathf.PI) * i);
	UpdateSiglePiece(pieces[i]);
}

// 标记尾部位置
void UpdateSiglePiece(GameObject picec){
	//添加地形移动
	BasicMovement move = newCylinder.addComponent<BasicMovement>();
	move.moveSpeed = -30f;


	// 创建结束点
	GameObject endPoint = new GameObject();
	endPoint.transform.postion = picec.transform.position + V3.forward * (dimensions.y * scale * Mathf.PI);
	endPoint.transform.parent = piece.transform;
	endPoint.name = "xxx";

	offset += randomness;
	
}


LateUpdate(){
	if(piece[1] && pieces[1].transform.z <=-15 ){
		startCoroutin(UpdateWorldPieces());
	}
}


IEnumerator UpdateWorldPieces(){
	Destory(pieces[0]);
	// 前移
	pieces[0] = pieces[1];
	pieces[1] = CreateCylinder();

	pieces[1].transform.position = pieces[0].transform.position + Vecotr3.forward * (dimensions.y * scale * Mathf.PI);
	pieces[1].transform.rotation = pieces[0].transform.rotation;
	UpdateSiglePiece(pieces[1]);
	yield return 0;
}
	


```



## 相机跟随


```c#

float height = 5f;
public float distance = 6f;

void LateUpdate(){
	if(camTarget == null){
		return ;
	}

	float wantedRotationAngle = camTarget.eulerAngles.y;
	float wantedHeight = camTarget.position.y + height;
	float currentRotationAngle = transform.eulerAngles.y;
	float currentHeight = transform.position.y;


	currentRotationAngle = Mathf.LerpAngle(currentRotationAngle , wantedRotationAngle, Time.deltaTime);
	currentHeight = Mathf.Lerp(currentHeight, wantedHeight, heightDamping * Time.deltaTime);

	Quaternion currentRotation = Quaternion.Euler(0, currentRotationAngle, z);

	transform.postion = camTarget.position;
	transform.postion -= currentRotation * V3.forward * distance;
	// 先后偏移
	transform.postion = new Vector3(transform.position.x, currentHeight, transform.postion.z);

	// 看向被观察者
	transform.LookAt(camTarget);
}
```


## 滚动问题

调整主体碰撞器，尽量和模型相近。


## 粒子效果和打滑效果


1. 选择材质
2. 设置大小和方向,角度，速度
3. 粒子的形状
4. 添加重力

印记： skid

skidMark --- prefab


```c#

public float skidMarkDelta;
public Transform[] skidMarkPivots; //轨迹的父物体
public Transform[] Effects;
public float skidMarkSize;
public RigidBody Rb;
public Transform back; // 添加力的位置
public float constantForce; // 力的大小

public GameObject skiMark;
public float grassEffectOffset; // 0.2f

public bool skidMarkRoutine; // 是否现实 Skid
public float minRotationDiff;
float lastRotation;

void start(){
	startcoroutine(SkidMark);
}

IEnumerator SkidMark(){
	while(true){
		yield return new WaitForSeconds(skidMarkDelta);
		if(skidMarkRoutine){
			for(int i = 0; i < skidMarkPivots.Length; i++){
				GameObject newSkidMark = Instance(skiMark, skidMarkPivots[i].position, skidMarkPivots[i].rotation);
				newSkidMark.transform.parent = World.GetWorldPiece(); // 获取世界地图中 piece[0] -- 当前脚下的地块
				newSkidMark.transform.localScale = new V3(1,1,4) * skidMarkSize;
			}
		}

	}
}



public FixedUpdate(){
	//更新粒子特效和痕迹
	UpdateEffectes();
}



void UpdateEffectes(){
	// 轮子在地面不需要加上轮胎的动力
	bool addForce = true;
	bool rotated = Mathf.abs(lastRotation - transform.localEulaerAngles.y) > minRotationDiff;
	for(int i = 0 ; i  < 2 ; i++){
		Transform whellMesh = wheelMesh[i+2];
		if(Physics.Raycast(whellMesh.position, V3.down), grassEffectOffset * 1.5f){
			//	粒子效果
			if(!grassEffects[i].gameObject.activateSelf){
				grassEffects[i].gameObject.setActivate(true);
			}
			float effectHeight = wheelMesh.Position.y - grassEffectOffset;
			V3 targetPosition = new V3(grassEffect[i].postion.x, effectHeight, wheelMesh.position.z);
			grassEffect[i].position = targetPosition; 
			skidMarkPivots[i].position = targetPosition;
			addForce =false;
		} else if(grassEffect[i].gameobject.activateSelf){
			grassEffects[i].gameObject.setActivate(false);
		}
	}

	if(addForce){ // 向下的力
		rb.AddForceAtPosition(back.position, V3.down * constantForce);
		skidMarkRoutine = false;
	}else{
		if(targetRotation != 0){ // 转弯
			if(rotated && !skidMarkRoutine){
				skidMarkRoutine = true;
			}else if(!rotated && skidMarkRoutine){
				skidMarkRoutine = false;
			}
		}else{
			skidMarkRoutine = true;
		}
	}

	lastRotation = transform.localEulaerAngles.y;
}
```


## 平滑连接


```c#
// 双循环设置顶点
for(int x = 0 ; x <= xCount ; x++){
	for(int z = 0 ; z <= zCount; z++){
		// 获取圆柱体的角度
		float angle = x * Mathf.PI * 2f / xCount;
		vectices[index] = new Vector3(Mathf.Cos(angle) * radius, Mathf.Sin(angle) * radius, z * scale * Mathf.PI);
		uvs[index] = new Vector2(x*scale, z*scale);


		// 使用柏林噪声
		float pX = (vectices[index].x * perlienScale) + offset;
		float pZ = (vectices[index].z * perlienScale) + offset;
		// 需要一个中心点和当前定期那做减法
		Vector3 center = new Vector3(0,0, vertices[index].z);
		vertices[index] += (center - vertices[index]).normalized * Mathf.PerlinNoise(pX,pY) * waveHeight; 

		
		if(z < startTransitionLength && beiginPoints[0] != V3.zero){ // 不是初始数组， 同时 需要更新
			float perlinpercentaget = z * (1f / startTransitionLength);	
			v3 beginPoint = new V3(beiginPoints[x].x, beiginPoints[x].y, beiginPoints[index].z);
			vectices[index] = (perlinpercentaget * vectices[index]) & (1-perlinpercentaget) * beiginPoint;
		}else if(z == zCount){
			beiginPoints[x] = vertices[index];
		}

		index++;
	}
}
```


## gamemanager

记录时间和分数 + gameOver + 控制所有Movement([[unity - 无尽赛车#BasicMovement]])


## BasicMovement

所有可移动物体的基类。


bool lamp --- 区分 灯光还是物体


CheckRotation