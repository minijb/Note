---
tags:
  - python
  - pylint
---
# pylint guide

## installation

`pip install pylint`

result

```txt
************* Module 1
1.py:5:9: C0303: Trailing whitespace (trailing-whitespace)
1.py:15:34: C0303: Trailing whitespace (trailing-whitespace)
1.py:19:0: C0303: Trailing whitespace (trailing-whitespace)
1.py:1:0: C0114: Missing module docstring (missing-module-docstring)
1.py:1:0: C0103: Module name "1" doesn't conform to snake_case naming style (invalid-name)
1.py:7:0: C0115: Missing class docstring (missing-class-docstring)
1.py:14:4: C0116: Missing function or method docstring (missing-function-docstring)
1.py:17:4: C0116: Missing function or method docstring (missing-function-docstring)
1.py:3:0: W0611: Unused import string (unused-import)

-----------------------------------
Your code has been rated at 2.50/10
```

## about

built-in checkers [pylint documentaion](http://pylint-messages.wikidot.com/all-codes)

## basic using and introduciton

`pylint xxx.py`

three kind of checkers in pylint

- AST(Abstract Syntax tree) checkers -- *most used*
- filestreams checkers
- tokens checkers

### AST

将源码转化为语法树

use `visit_<node_type>` and `leave_<node_type>` 来处理节点

the list of all node: [here](https://pylint.pycqa.org/projects/astroid/en/latest/api/astroid.nodes.html)
**message category**:

```txt
+----------+------------+---------------------------------------------------------------------------+
| category |    name    |                                description                                | 
+----------+------------+---------------------------------------------------------------------------+
| C        | Convention | It is displayed when the program is not following the standard rules.     |
| R        | Refactor   | It is displayed for bad code smell                                        |
| W        | Warning    | It is displayed for python specific problems                              |
| E        | Error      | It is displayed when that particular line execution results in some error |
| F        | Fatal      | It is displayed when pylint has no access to further process that line.   |
+----------+------------+---------------------------------------------------------------------------+
```


#TODO 