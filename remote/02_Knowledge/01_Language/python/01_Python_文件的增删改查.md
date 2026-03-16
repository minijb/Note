
主要包含两个库文件 `shutil, os`

- 复制 ： 
  - `shutil.copy(src, dest)` 复制文件
  - `shutil.copytree(src, dest)` 复制文件夹  
- 移动
  - `shutil.move(src, dest)`
- 删除
  - `os.unlink(dest)` 删除文件
  - `os.rmdir(dest)`
  - `os.rmtree(dest)`
- 创建文件夹
  - `os.makedirs(dest, exist_ok=True)` exist_ok : 是否递归的创建