# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 当前任务：笔记整合迁移

正在执行从 `Blog/`, `Note/`, `remote/` 三个旧版本向统一结构迁移。

## 迁移目标结构
采用 **MOC + PARA + 数字前缀** 的混合结构：

```
remote/                      # 以 remote 为基础目录（包含同步配置）
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
在 `remote/` 下创建所有子文件夹

### Step 2: 处理 remote 根目录散落文件
- `need to do.md`, `备忘录.md` → `00_Inbox/`
- `目标.md`, `面试实录.md` → `04_Career/`
- `template.md` → `88_Templates/`
- `Pasted image*.png` → `99_Assets/`

### Step 3: 吸收 Note 目录
- `Note/Language/` → `remote/02_Knowledge/01_Language/`
- `Note/Tools/` → `remote/02_Knowledge/03_Tools/`
- `Note/Unity/` → `remote/02_Knowledge/02_Framework/`
- `Note/Project/` → `remote/01_Projects/`
- `Note/Skill/` → `remote/02_Knowledge/`（按内容分散）
- `Note/Resources/` → `remote/03_Resources/`

### Step 4: 吸收 Blog 目录
- `Blog/1_Projects/` → `remote/01_Projects/`
- `Blog/2_TechStack/` → `remote/02_Knowledge/`（按内容分散）
- `Blog/5_KowledgeBase/` → `remote/02_Knowledge/`
- `Blog/10_Archive/` → `remote/Archive/`
- `Blog/Excalidraw/` → `remote/99_Assets/`

## 常用操作命令
- **创建目录**：`mkdir -p remote/00_Inbox remote/01_Projects remote/02_Knowledge/{01_Language,02_Framework,03_Tools,04_CS_Basics} remote/03_Resources/{Code_Snippets,PDF_Books,Bookmarks} remote/04_Career remote/88_Templates remote/99_Assets remote/Archive`
- **移动文件**：`mv 源路径 目标路径`
- **搜索笔记**：`Grep` 工具搜索关键词
- **查找文件**：`Glob` 工具按模式匹配

## 笔记维护建议
- **标签优先于文件夹**：使用 `#tag` 而非深层次嵌套
- **状态标签**：`#todo`, `#draft`, `#review`
- **每目录放 MOC 索引页**：用 `[[wikilink]]` 串联相关内容