
- Lua分析器--- 基础 [github](https://github.com/EmmyLuaLs/emmylua-analyzer-rust)
- Rider插件--- [github](https://github.com/EmmyLua/Intellij-EmmyLua2)
- vscode插件--- [github](https://marketplace.visualstudio.com/items?itemName=tangzx.emmylua)

## 1. Rider 插件安装

1. 直接安装插件
2. 使用 [SnippetGenerator](https://github.com/ak47007tiger/EmmyLuaXLuaSnippetGenerator) 通过反射生成 Snippet
3. 创建 `.emmyrc.json` 

关键字段 ： 

- "Runtime"
- "workspace"  ： 放入Lua文件的根目录
- "diagnostics.globals" ： 放入全局变量白名单


```json
{
  "$schema": "https://raw.githubusercontent.com/EmmyLuaLs/emmylua-analyzer-rust/refs/heads/main/crates/emmylua_code_analysis/resources/schema.json",
  "codeAction": {
    "insertSpace": false
  },
  "codeLens": {
    "enable": true
  },
  "completion": {
    "enable": true,
    "autoRequire": true,
    "autoRequireFunction": "require",
    "autoRequireNamingConvention": "keep",
    "autoRequireSeparator": ".",
    "callSnippet": false,
    "postfix": "@",
    "baseFunctionIncludesName": true
  },
  "diagnostics": {
    "enable": true,
    "disable": [],
    "enables": [],
    "globals": [
    ],
    "globalsRegex": [],
    "severity": {},
    "diagnosticInterval": 500
  },
  "doc": {
    "syntax": "md"
  },
  "documentColor": {
    "enable": true
  },
  "hover": {
    "enable": true
  },
  "hint": {
    "enable": true,
    "paramHint": true,
    "indexHint": true,
    "localHint": true,
    "overrideHint": true,
    "metaCallHint": true
  },
  "inlineValues": {
    "enable": true
  },
  "references": {
    "enable": true,
    "fuzzySearch": true,
    "shortStringSearch": false
  },
  "reformat": {
    "externalTool": null,
    "externalToolRangeFormat": null,
    "useDiff": false
  },
  "resource": {
    "paths": []
  },
  "runtime": {
    "version": "LuaLatest",
    "requireLikeFunction": ["import", "load", "dofile"],
    "frameworkVersions": ["love2d", "openresty", "nginx"],
    "extensions": [".lua", ".lua.txt", ".luau"],
    "requirePattern": ["?.lua", "?/init.lua", "lib/?.lua"],
    "classDefaultCall": {
      "functionName": "new",
      "forceNonColon": false,
      "forceReturnSelf": true
    },
    "nonstandardSymbol": ["continue"],
    "special": {
      "errorf": "error"
    }
  },
  "semanticTokens": {
    "enable": true
  },
  "signature": {
    "detailSignatureHelper": true
  },
  "strict": {
    "requirePath": false,
    "typeCall": false,
    "arrayIndex": true,
    "metaOverrideFileDefine": true,
    "docBaseConstMatchBaseType": true
  },
  "workspace": {
    "ignoreDir": [],
    "ignoreGlobs": [],
    "library": [],
    "workspaceRoots": ["Assets/Script/Lua"],
    "preloadFileSize": 0,
    "encoding": "utf-8",
    "moduleMap": [],
    "reindexDuration": 5000,
    "enableReindex": false
  }
}

```


## 2. Debug


使用 vscode  attch 模式， rider 调试功能有bug
