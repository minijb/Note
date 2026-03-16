# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 当前任务：笔记整合迁移

正在执行从 `Blog/`, `Note/`, `remote/` 三个旧版本向统一结构 `My_Vault/` 迁移的工作。

## 迁移目标结构
采用 **MOC + PARA + 数字前缀** 的混合结构：

```
My_Vault/                      # 新的统一知识库根目录
├── 00_Dashboard.md         # 主页/导航页
├── 00_Inbox/               # 收件箱：临时闪念、未分类内容
├── 01_Projects/            # 项目：正在进行的代码项目
├── 02_Knowledge/          # 知识库（核心）
│   ├── 01_Language/       # 编程语言
│   ├── 02_Framework/      # 框架与引擎
│   ├── 03_Tools/          # 工具使用
│   └── 04_CS_Basics/     # 计算机基础
├── 03_Resources/           # 资源库
│   ├── Code_Snippets/    # 代码片段
│   ├── PDF_Books/        # 电子书
│   └── Bookmarks/        # 网址收藏
├── 04_Career/             # 职业发展
├── 88_Templates/          # 模板
├── 99_Assets/             # 附件库
└── Archive/              # 归档
```

## 迁移步骤（按顺序执行）

### Step 1: 创建新目录结构
在 `My_Vault/` 下创建所有子文件夹

### Step 2: 处理 My_Vault 根目录散落文件
- `need to do.md`, `备忘录.md` → `00_Inbox/`
- `目标.md`, `面试实录.md` → `04_Career/`
- `template.md` → `88_Templates/`
- `Pasted image*.png` → `99_Assets/`

### Step 3: 吸收 Note 目录
- `Note/Language/` → `My_Vault/02_Knowledge/01_Language/`
- `Note/Tools/` → `My_Vault/02_Knowledge/03_Tools/`
- `Note/Unity/` → `My_Vault/02_Knowledge/02_Framework/`
- `Note/Project/` → `My_Vault/01_Projects/`
- `Note/Skill/` → `My_Vault/02_Knowledge/`（按内容分散）
- `Note/Resources/` → `My_Vault/03_Resources/`

### Step 4: 吸收 Blog 目录
- `Blog/1_Projects/` → `My_Vault/01_Projects/`
- `Blog/2_TechStack/` → `My_Vault/02_Knowledge/`（按内容分散）
- `Blog/5_KowledgeBase/` → `My_Vault/02_Knowledge/`
- `Blog/10_Archive/` → `My_Vault/Archive/`
- `Blog/Excalidraw/` → `My_Vault/99_Assets/`

## 常用操作命令
- **创建目录**：`mkdir -p My_Vault/00_Inbox My_Vault/01_Projects My_Vault/02_Knowledge/{01_Language,02_Framework,03_Tools,04_CS_Basics} My_Vault/03_Resources/{Code_Snippets,PDF_Books,Bookmarks} My_Vault/04_Career My_Vault/88_Templates My_Vault/99_Assets My_Vault/Archive`
- **移动文件**：`mv 源路径 目标路径`
- **搜索笔记**：`Grep` 工具搜索关键词
- **查找文件**：`Glob` 工具按模式匹配

## 笔记维护建议
- **标签优先于文件夹**：使用 `#tag` 而非深层次嵌套
- **状态标签**：`#todo`, `#draft`, `#review`
- **每目录放 MOC 索引页**：用 `[[wikilink]]` 串联相关内容