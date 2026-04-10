自己的 wiki ：

- 原始资料
- wiki ： 一个由 LLM 生成的 markdown 文件目录。摘要、实体页、概念页、比较、概述、综合。LLM 完全拥有这一层。它创建页面，当新资料来源到来时更新，维护交叉引用，并保持一切一致性。你读了;LLM 写的。a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.
- scheme ： 总纲 一份文档（例如 Claude Code 的 CLAUDE.md 或 Codex 的 AGENTS.md Wiki 的文档），告诉 LLMwiki 的结构、惯例以及在导入源代码、回答问题或维护维基时应遵循的工作流程。这是关键的配置文件——正是它让 LLM 成为一个有纪律的维基维护者，而不是普通的聊天机器人。你和 LLM 会随着时间推移共同进化，找出适合你领域的方法。

**吞下。** 你把一个新源放进原始集合，然后让 LLM 处理它。一个示例流程：LLM 会阅读源代码，与你讨论关键要点，在维基中写摘要页，更新索引，更新维基中相关的实体和概念页面，并在日志中添加条目。一个来源可能覆盖 10 到 15 个维基页面。我个人更喜欢一次只吸收一个资料，保持参与——我会阅读摘要，查看更新，指导大语言模型强调什么。但你也可以在更少监督的情况下一次性批量吸收多个来源。你需要自己制定适合自己风格的工作流程，并在模式中记录下来，以便以后使用。

**查询。** 你会对着维基提问。LLM 会搜索相关页面，阅读它们，并综合答案并引用。答案根据问题的不同形式可能不同——标记页、比较表、幻灯片（Marp）、图表（matplotlib）、画布。重要的见解是： **好的答案可以作为新页面重新归档到维基。** 你要求的比较、分析、你发现的联系——这些都很有价值，不应该被消失在聊天记录里。这样你的探索就能像吸收的资源一样积累知识库。

**绒毛。** 定期让 LLM 对维基进行健康检查。注意：页面间矛盾、陈旧的说法认为新来源已被取代、无入站链接的孤立页面、提及重要概念但缺乏独立页面、缺失交叉引用、可用网络搜索填补的数据空白。LLM 擅长提出新的问题和新的资源。这样能让维基在成长过程中保持健康。

如何保持文档在不断扩展中健壮性和实时性？

- index.md 以内容为导向。它是 wiki 中所有内容的目录——每页都附有链接、一句摘要，以及可选的元数据，如日期或来源数量。按类别（实体、概念、来源等）组织。LLM 会在每次导入时更新它。在回答查询时，LLM 首先读取索引以找到相关页面，然后深入挖掘。这在中等规模（~100 个源码，~数百页）下效果出奇地好，避免了嵌入式 RAG 基础设施的需求。
- log.md 是按时间顺序排列的。它只是一个只附录的时间和记录发生了什么——摄入、查询、棉絮传递。一个有用的建议：如果每个条目都以一致的前缀开头（例如 `## [2026-04-02] ingest | Article Title` ），日志就会变得可以用简单的 Unix 工具解析—— `grep "^## \[" log.md | tail -5` 给出最近 5 条条目。日志为你提供了维基演变的时间线，帮助大型语言模型理解最近的工作进展。

一个搜索引擎(本地) ： https://github.com/tobi/qmd 提供 Markdown 文件的混合功能，结合 BM25/矢量搜索和 LLM 重新排序，全部在设备上运行。它既有 CLI（这样 LLM 可以向它分配），也有 MCP 服务器（LLM 可以作为原生工具使用）。你也可以自己做更简单的——LLM 可以帮你根据需要对一个天真搜索脚本进行氛围编码。


**技巧**

- **Obsidian Web Clipper** 是一款将网页文章转换为 markdown 的浏览器扩展。非常方便快速将资料导入你的原始收藏。
- **Download images locally.** 在 Obsidian 设置→文件和链接中，将“附件文件夹路径”设置为固定目录（例如 `raw/assets/`）。然后在设置→快捷键中搜索“下载”，找到“下载当前文件附件”，并将其绑定到快捷键（例如 Ctrl+Shift+D）。剪辑完一篇文章后，按下快捷键，所有图片就会被下载到本地磁盘。这是可选但有用的——它让 LLM 直接查看和引用图片，而不必依赖可能损坏的 URL。注意，LLM 不能一次性读取内联图片的 markdown——解决方法是让 LLM 先读取文本，然后单独查看部分或全部引用图片以获得更多上下文。虽然有点笨重，但用起来还算不错。 
- **Obsidian's graph view** 是了解维基结构的最佳方式——哪些连接着什么，哪些页面是枢纽，哪些是孤儿
- **Marp** 是一种基于 Markdown 的幻灯片格式。Obsidian 有插件。它适合直接从维基内容生成演示。
- **Dataview** 是一个 Obsidian 插件，可以通过页面 frontmatter 运行查询。如果你的 LLM 在维基页面添加 YAML 前置（标签、日期、源代码计数），Dataview 可以生成动态表和列表。
- - 维基其实就是 Markdown 文件的 git 仓库。你可以免费获得版本历史、分支和协作功能。


观众贡献的技巧： 

- **索引优化** 我们开发了 OMEGA（[https://github.com/omega-memory/omega-memory](https://github.com/omega-memory/omega-memory)）来解决这个问题，采用局部语义搜索而非 Markdown。矢量嵌入 + FTS5 + 交叉编码器重新排序，全部在你的机器上。LongMemEval 在 50 毫秒取出时显示 95.4%。
- 刚 [https://github.com/omega-memory/omega-obsidian-plugin](https://github.com/omega-memory/omega-obsidian-plugin) 也寄了一个 Obsidian 插件，用于跨保险库的语义搜索。Obsidian 作为前端（完全符合这里描述的），OMEGA 作为底层的检索层。


```query
tag:#project
```
