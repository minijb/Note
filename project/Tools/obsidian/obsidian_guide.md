# Obsidian Guide

#obsidian 

## 嵌入

`![[]]` 

1. Markdown 文件：`md`;
2. 图像文件：`png`, `jpg`, `jpeg`, `gif`, `bmp`, `svg`;
3. 音频文件：`mp3`, `webm`, `wav`, `m4a`, `ogg`, `3gp`, `flac`;
4. 视频文件：`mp4`, `webm`, `ogv`;
5. PDF 文件：`pdf`.

嵌入网页(iframe) : `<iframe src="https://www.bilibili.com/"></iframe>`

可以添加属性 如

```html
<iframe border=0 frameborder=0 height=250 width=550 src="https://twitframe.com/show?url=https%3A%2F%2Ftwitter.com%2Fjack%2Fstatus%2F20"> </iframe>
```

### 调整大小

Markdown 风格的嵌入，使用 `![AltText|100x100](https://url/to/image.png)` 这样的语法。

一般的嵌入，使用 `![[image.png|100x100]]` 这样的语法。

## 笔记别名

在 metadata 中添加 

```markdown
aliases: [AI, Artificial Intelligence]
```