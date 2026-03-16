---
tags:
  - bash
---
第一行  ： `#!/bin/bash` 告诉操作系统，本文将是一组命令，给的是路径下的解释器， **需要保证 路径是正确的**

`#` 注释

**变量** ： `xx=xx` 注意=周围不能有空格 , 变量可以使用命令的输出进行赋值, 使用 `$() 或者  back-ticks `

reference of var : `${xxx}` ，在字符串外部可以直接使用 `$`

**内部变量**   `$0` 为当前的命令  `$1-6`  为 第n个参数 `$#` 参数的个数 变量 `$@` 所有参数列表 -- 数组 `$*` 也是参数列表 字符串

**Array** : `()`  length : `${#arrayname[@]}` , all element `${arrayname[@/*]}` : `` reference : `${array[x]}`

注意键可以不是数字

```bash
declare -A site
site["google"]="www.google.com"
site["runoob"]="www.runoob.com"
site["taobao"]="www.taobao.com"

echo "数组的键为: ${!site[*]}"
echo "数组的键为: ${!site[@]}"
```


**string**  length : `${#xxx}` , 

**子串**  ： 

```bash
STRING="this is a string"
POS=1
LEN=3
echo ${STRING:$POS:$LEN}   # his


STRING="this is a string"
echo ${STRING:1}           # $STRING contents without leading character
echo ${STRING:12}          # ring
```


**简单的数据处理**

```bash
DATARECORD="last=Clifford,first=Johnny Boy,state=CA"
COMMA1=`expr index "$DATARECORD" ','`  # 14 position of first comma
CHOP1FIELD=${DATARECORD:$COMMA1}       #
COMMA2=`expr index "$CHOP1FIELD" ','`
LENGTH=`expr $COMMA2 - 6 - 1`
FIRSTNAME=${CHOP1FIELD:6:$LENGTH}      # Johnny Boy
echo $FIRSTNAME
```

**子串替换**

```bash
# replace one
STRING="to be or not to be"
echo ${STRING[@]/be/eat}        # to eat or not to be

# replace all
STRING="to be or not to be"
echo ${STRING[@]//be/eat}        # to eat or not to eat

# replace all not with empty string
STRING="to be or not to be"
echo ${STRING[@]// not/}        # to be or to be

# 匹配开头
STRING="to be or not to be"
echo ${STRING[@]/#to be/eat now}    # eat now or not to be

# 匹配结尾

STRING="to be or not to be"
echo ${STRING[@]/%be/eat}        # to be or not to eat

# 使用命令的结果作为替换结果

STRING="to be or not to be"
echo ${STRING[@]/%be/be on $(date +%Y-%m-%d)}    # to be or not to be on 2012-06-14

```


## 条件

```bash
NAME="George"
if [ "$NAME" = "John" ]; then
  echo "John Lennon"
elif [ "$NAME" = "George" ]; then
  echo "George Harrison"
else
  echo "This leaves us with Paul and Ringo"
fi
```


**数字条件判断**

```bash
comparison    Evaluated to true when
$a -lt $b    $a < $b
$a -gt $b    $a > $b
$a -le $b    $a <= $b
$a -ge $b    $a >= $b
$a -eq $b    $a is equal to $b
$a -ne $b    $a is not equal to $b
```

**字符串条件判断**

```bash
comparison    Evaluated to true when
"$a" = "$b"     $a is the same as $b
"$a" == "$b"    $a is the same as $b
"$a" != "$b"    $a is different from $b
-z "$a"         $a is empty
```


> 注意： = 周围需要空格

**逻辑混合 以及 switch**

```bash
if [[ $VAR_A[0] -eq 1 && ($VAR_B = "bee" || $VAR_T = "tee") ]] ; then
    command...
fi

case "$variable" in
    "$condition1" )
        command...
    ;;
    "$condition2" )
        command...
    ;;
esac


mycase=1
case $mycase in
    1) echo "You selected bash";;
    2) echo "You selected perl";;
    3) echo "You selected phyton";;
    4) echo "You selected c++";;
    5) exit
esac
```

## Loop

```bash
# basic construct
for arg in [list]
do
 command(s)...
done



# loop on array member
NAMES=(Joe Jenny Sara Tony)
for N in ${NAMES[@]} ; do
  echo "My name is $N"
done

# loop on command output results
for f in $( ls prog.sh /etc/localtime ) ; do
  echo "File is: $f"
done


# basic construct
while [ condition ]
do
 command(s)...
done

COUNT=4
while [ $COUNT -gt 0 ]; do
  echo "Value of count is: $COUNT"
  COUNT=$(($COUNT - 1))
done

# basic construct
until [ condition ]
do
 command(s)...
done

COUNT=1
until [ $COUNT -gt 5 ]; do
  echo "Value of count is: $COUNT"
  COUNT=$(($COUNT + 1))
done

```



**break and continue**


```bash
# Prints out 0,1,2,3,4

COUNT=0
while [ $COUNT -ge 0 ]; do
  echo "Value of COUNT is: $COUNT"
  COUNT=$((COUNT+1))
  if [ $COUNT -ge 5 ] ; then
    break
  fi
done

# Prints out only odd numbers - 1,3,5,7,9
COUNT=0
while [ $COUNT -lt 10 ]; do
  COUNT=$((COUNT+1))
  # Check if COUNT is even
  if [ $(($COUNT % 2)) = 0 ] ; then
    continue
  fi
  echo $COUNT
done
```


## Function

```bash
function function_B {
  echo "Function B."
}
function function_A {
  echo "$1"
}
function adder {
  echo "$(($1 + $2))"
}

# FUNCTION CALLS
# Pass parameter to function A
function_A "Function A."     # Function A.
function_B                   # Function B.
# Pass two parameters to function adder
adder 12 56                  # 68
```


## special variables

- `$0` - The filename of the current script.|
- `$n` - The Nth argument passed to script was invoked or function was called.|
- `$#` - The number of argument passed to script or function.|
- `$@` - All arguments passed to script or function.|
- `$*` - All arguments passed to script or function.|
- `$?` - The exit status of the last command executed.|
- `$$` - The process ID of the current shell. For shell scripts, this is the process ID under which they are executing.|
- `$!` - The process number of the last background command.|

https://www.learnshell.org/en/Bash_trap_command


## trap 命令

捕获信号

```bash
#!/bin/bash
# traptest.sh
# notice you cannot make Ctrl-C work in this shell, 
# try with your local one, also remeber to chmod +x 
# your local .sh file so you can execute it!

trap "echo Booh!" SIGINT SIGTERM
echo "it's going to run until you hit Ctrl+Z"
echo "hit Ctrl+C to be blown away!"

while true        
do
    sleep 60       
done


trap booh SIGINT SIGTERM

#one of the common usage of trap is to do cleanup temporary files:
trap "rm -f folder; exit" 2
```


- `SIGINT`: user sends an interrupt signal (Ctrl + C)
- `SIGQUIT`: user sends a quit signal (Ctrl + D)
- `SIGFPE`: attempted an illegal mathematical operation

## `-<command>`

**use "-e" to test if file exist**

```bash
#!/bin/bash
filename="sample.md"
if [ -e "$filename" ]; then
    echo "$filename exists as a file"
fi
```

**use "-d" to test if directory exists**

```bash
#!/bin/bash
directory_name="test_directory"
if [ -d "$directory_name" ]; then
    echo "$directory_name exists as a directory"
fi
```

**use "-r" to test if file has read permission for the user running the script/test**

```bash
#!/bin/bash
filename="sample.md"
if [ ! -f "$filename" ]; then
    touch "$filename"
fi
if [ -r "$filename" ]; then
    echo "you are allowed to read $filename"
else
    echo "you are not allowed to read $filename"
fi
```

## pipeline

connect output from one command to the ibput of the next

`A | B`

## Process substitution

`> / <`

先 sort file， 然后 diff

```bash
sort file1 > sorted_file1
sort file2 > sorted_file2
diff sorted_file1 sorted_file2

diff <(sort file1) <(sort file2)
```


Imagine you want to store logs of an application into a file and at the same time print it on the console. A very handy command for that is `tee`.

```bash
echo "Hello, world!" | tee /tmp/hello.txt


echo "Hello, world!" | tee >(tr '[:upper:]' '[:lower:]' > /tmp/hello.txt)

```


- [ ] 正则
- [ ] Special Commands sed,awk,grep,sort

