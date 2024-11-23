---
tags:
  - git
---
**set proxy**

```sh
git config --global http.proxy 'http://127.0.0.1:10809'
git config --global https.proxy 'http://127.0.0.1:10809'
```

**unset proxy**

```sh
git config --global --unset http.proxy
git config --global --unset https.proxy
```