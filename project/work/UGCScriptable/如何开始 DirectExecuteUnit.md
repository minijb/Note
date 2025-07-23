


```c#
    public class DirectExecuteUnit:BaseScriptUnit
    {
        //public ControlOutput Starter;
        protected override void Definition()
        {
            Exit = ControlOutput("Starter");
        }

        public override List<BaseLayout> GetLayoutDefine(Flow flow)
        {
            var l = base.GetLayoutDefine(flow);
            // var text = new TextLayout(this, $" {graph.Title}");
            // text.SetFontAndSize("robotocondensed-bold.ttf", 40);
            // l.Add(text);
            if (Exit.hasValidConnection && Exit.connection.destination.unit is BaseScriptUnit b)
            {
                FetchRootUnitLayout(b, l);
            }
            
            return l;
        }
        
    }
```


输出一个 controlflow 。 方便脚本的开始

