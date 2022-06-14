# 变量

输出

```javascript
// 终端输出
console.log("hello");
// 警告
window.alert("hello");
```

**let 和 var的区别**

https://blog.csdn.net/weixin_43108539/article/details/108514200

也可以这样输出

```js
let x = 100;
let first = "Bro is"
let second = "three years old";
console.log(first,x,second)

document.getElementById("p1").innerHTML = first+x+second
```

### 输入

```js
let username = window.prompt("what is your name");
console.log(username);
```

```js
let username;
document.getElementById("myButton").onclick = function(){
    username = document.getElementById("myText").value;
    console.log(username);
    document.getElementById("mylabel").innerHTML = document.getElementById("mylabel").innerHTML + username;
}