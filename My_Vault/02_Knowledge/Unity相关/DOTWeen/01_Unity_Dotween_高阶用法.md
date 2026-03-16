
## 1. to/from

```c#
Vector3 myvalue = new Vector3(0, 0, 0);
DOTween.To(() => myvalue, x => myvalue = x, new Vector3(10, 10, 10), 2);
                 要移动的初始值                目标值                时间
DOTween.To(getter, setter, endValue, duration);
	参数说明
		getter			一个函数，用于获取当前值。它应该返回一个 float、Vector3、Color 等类型的值，具体取决于你要动画化的属性。
		setter			一个函数，用于设置目标值。它接受一个参数（目标值），并将其应用于对象的属性。
		endValue		动画的结束值。即动画完成时，属性应该达到的值。
		duration		动画的持续时间，单位为秒。
```


From : 归位 --- ture 的时候为相对位置， 目标位置 = 目标位置+当前位置


transform.DOMove(new Vector3(2, 2, 0), 1).From();
1秒时间从世界坐标（2，2，0）处回到自身当前位置

transform.DOMove(new Vector3(2, 2, 0), 2).From(true);
从以自身为原点的坐标系（2，2，0）处回到自身当前位置


## 2. set方法

- SetDelay 设置延迟
- SetEase 设置运动类型 
- SetLoops 循环类型
- SetAutoKill 完成后自动销毁
- SetID 设置动画ID --- 便于查找和管理
- SetUpdate 独立的时间更新


## 3. 控制

- Pause 暂停
- Play 恢复
- Kill 结束动画
- Restart
- DoPlay 只播放一次，再次调用不可以播放
- DoPlayForward
- DoPlayBackwards
- DoResetart

## 4. 回调

- onStart
- onPlay
- OnUpdate
- OnComplete
- OnKill
- OnRewind
- OnPause

## 5. 动画对象

Tween： 通用对象对象，
Tweener ： 特定的动画类型 ： 通常用于数值类型的动画如浮点数，整数。语序在动画中设置开始和结束值。


## 6. ID的使用

在 DOTween 中，设置动画的ID是一个非常好用的功能，可以帮助你管理和查找特定的动画。通过 ID 可以方便地对某个特定的动画进行操作，比如暂停、恢复、停止或销毁。使用场景一般用于：

管理动画： 当你有多个动画时，可以通过 ID 来区分和管理它们。
批量操作： 可以通过 ID 批量暂停或停止具有相同 ID 的所有动画。
状态管理： 在游戏中，可以根据不同的状态来控制相应的动画。

```c#
//创建一个动画并设置 ID
Tween tween1 = transform.DOMove(target.position, duration)
	.SetId("moveTween")
	.OnComplete(() => Debug.Log("动画1完成"));

//创建另一个动画并设置相同的 ID
Tween tween2 = transform.DORotate(new Vector3(0, 180, 0), duration)
	.SetId("moveTween") // 设置相同的 ID
	.OnComplete(() => Debug.Log("动画2完成"));


//暂停所有 ID 为 "moveTween" 的动画
DOTween.Pause("moveTween");

//恢复所有 ID 为 "moveTween" 的动画
DOTween.Play("moveTween");

//杀死所有 ID 为 "moveTween" 的动画
DOTween.Kill("moveTween");
```

## 7. 序列动画

- **顺序执行：** 你可以将多个动画添加到序列中，确保它们按照你希望的顺序依次执行。
- **组合动画：** 可以将不同类型的动画（如移动、旋转、缩放等）组合在一起，形成一个复杂的动画效果。
- **控制时间：** 你可以设置每个动画的延迟、持续时间等参数，使得整个序列动画的表现更加丰富。

```c#
//创建一个序列动画
Sequence loopTween = DOTween.Sequence();

//添加第一个动画：移动到目标位置
loopTween.Append(transform.DOMove(target.position, 1f).SetEase(Ease.Linear));

//添加第二个动画：旋转
loopTween.Append(transform.DORotate(new Vector3(0, 180, 0), 1f).SetEase(Ease.OutBounce));

//添加第三个动画：缩放
loopTween.Append(transform.DOScale(new Vector3(2, 2, 2), 1f).SetEase(Ease.OutElastic));

//播放序列动画
loopTween.Play();

//暂停序列动画
loopTween.Pause();

//停止序列动画
loopTween.Kill();

//重播序列动画
loopTween.Restart();

// 添加一个回调，在序列完成时执行
loopTween.OnComplete(() => Debug.Log("序列动画完成"));
```


Sequence 的特化方法

```c#
Sequence loopTween = DOTween.Sequence();

//将一个新的动画添加到序列的末尾。
loopTween.Append(Tween tween);

//在序列中添加一个回调函数（序列执行到该位置时会被调用）。
loopTween.AppendCallback(TweenCallback callback);

//在序列中添加一个间隔（指定时间内不执行任何动画）。
loopTween.AppendInterval(float interval);

//将一个新的动画添加到序列的开头。Prepend和Append刚好相反，一个添加到尾部(Append)一个添加到头部(Prepend)
loopTween.Prepend(Tween tween);

//将一个回调函数添加到序列的开头。
loopTween.PrependCallback(TweenCallback callback);

//在序列前面添加一个间隔（指定时间内不执行任何动画）。
loopTween.PrependInterval(float interval);

//将一个新的动画添加到序列中，与当前动画同时播放。
loopTween.Join(Tween tween);

//在指定时间插入一个新的动画。
loopTween.Insert(float time, Tween tween);

//在特定时间点插入一个回调。
loopTween.InsertCallback(float atPosition, TweenCallback callback);
```