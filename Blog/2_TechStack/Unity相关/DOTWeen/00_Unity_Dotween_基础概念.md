
1. 清理残留
`.DoKill()`
2. 让动画不受 timeScale 影响
`transform.DOMoveX(5f, 2).SetUpdate(true);`
3. 类型 -- Tween
`Tween tween = transform.DOMoveX(5f, 2).SetUpdate(true);`

可以用作拓展，灵活性更好

