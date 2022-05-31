# Xpath

- 在xml文档中搜索内容的一门语言

## 1. 使用

```python
from lxml import etree
xml = '''
<book>
    <id>1</id>
    <name>ok</name>
    <author>
        <nick id="10086">zhouhao1</nick>
        <nick id="10089">zhouhao2</nick>
        <nick class="1">zhouhao3</nick>
        <nick class="1">zhouhao4</nick>
        
    </author>
</book>
'''
tree = etree.XML(xml)
result = tree.xpath("/book/author/nick/text()")
result#['zhouhao1', 'zhouhao2', 'zhouhao3', 'zhouhao4']
```

注：会返回同一目录下相同类型的列表如

```python
result = tree.xpath("/book/author//nick/text()")
#['zhouhao1', 'zhouhao2', 'zhouhao3', 'zhouhao4', 'rrrrrrr']
#//则会搜索当前目录内所有nick包括子目录中的


result = tree.xpath("/book/author/*/nick/text()")#['rrrrrrr']
#*代表任意目录，不包含当前目录
result
```

同理在html中

### 可以通过[]来选择特定的标签

```python
result = tree.xpath("/html/body/ul/li[0]/a/text()")
```

### 选择特定属性

```python
result = tree.xpath("/html/body/ul/li[0]/a[@href='dapao']/text()")
```

### 相对查找

```python
for li in ol_li_list:
    li.xpath("./a/text()")
```

### 获取属性

```python
li.xpath("./a/@href")
```

## 2. 实战

**注：xpath中的[]序号是从1开始的！！！！！**

```python
import requests
from bs4 import BeautifulSoup
import time

domain_url = 'https://www.umei.cc/katongdongman/katongrenwu/'
base_url = 'https://www.umei.cc'
content = requests.get(domain_url)
content.encoding='utf-8'

#找到pic所在的ul
bs_content = BeautifulSoup(content.text,'html.parser')
pic_ul = bs_content.find('ul',attrs={'class':"pic-list after"})

#找到a标签并获得链接
#链接地址为一个数据
href_list = []
pic_li = pic_ul.find_all('li')
for li in pic_li:
    pic_a = li.find('a')
    # print(base_url+pic_a.get('href'))#拿去href属性中的值
    href_list.append(base_url+pic_a.get('href'))
    

    
for index,href in enumerate(href_list):
    child_content = requests.get(href)
    child_content.encoding='utf-8'
    bs_child = BeautifulSoup(child_content.text,'html.parser')
    child_img_url = bs_child.find('div',attrs={'class':"content-box"}).find('img').get('src')
    # print(child_img_url)
    #下载文件
    img_resp = requests.get(child_img_url)
    with open('./learn/爬虫/img/'+str(index)+'.jpg','wb') as f:
        f.write(img_resp.content)#写入字节
    #防止被干掉
    print('over:'+str(index))
    child_content.close()
    time.sleep(1)
    
    
content.close()
```

