---
tags:
  - algo
---
用于一定区间内的维护最大/最小值

### 单调队列

```cpp
class Myqueue{
private:
	deque<int> dq;
public:
	Myqueue(){}

	void Push(const int &num){
		while (!dq.empty() && dq.back() < num) dq.pop_back();
		dq.push_back(num);
	}

	void Pop(int num){
		if (!dq.empty()&&num == dq.front()) dq.pop_front();
	}

	int front(){
		return dq.front();
	}
};
```

