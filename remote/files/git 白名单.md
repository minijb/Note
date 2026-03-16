---
tags:
  - git
---

感叹号 `!` 用于将规则变成白名单。它匹配所有目录，但由于它不匹配这些目录中的任何内容，因此 Git 目前还不会仅通过这两行来跟踪任何文件。

```txt
*
!*/

# track this file
!.gitignore

# whitelist everything in ./config/
!config/
```