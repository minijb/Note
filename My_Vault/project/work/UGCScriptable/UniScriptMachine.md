
```c#
namespace Uni.Component
{
    public class UniScriptMachine : ScriptMachine
    {
        public Uni.Mod.UniModBlackboard Blackboard;
        public static UniLogger Logger = UniLogManager.Get<UniScriptMachine>(true);
        public List<string> internalScriptGUIDList = null;
        private Flow curflow;
        public List<uint> InnerScriptUsedNodeIdList;
        public List<uint> UsedInnerNodeIdList;
        public Dictionary<string, List<uint>> InnerScriptDataDict;

        public Flow CurFlow
        {
            get
            {
                if (curflow == null)
                    curflow = CreateFlow();
                return curflow;
            }
        }

        // public string BroadcastName;
        // public string ComponentName;
        // public UnitTitleType TitleType;

        public override FlowGraph DefaultGraph()
        {
            var graph = new FlowGraph();
            graph.ScriptMachine = this;
            var directUnit = new DirectExecuteUnit();
            graph.units.Add(directUnit);
            var titleUnit = new TitleUnit();
            graph.units.Add(titleUnit);
            directUnit.Exit.ValidlyConnectTo(titleUnit.Enter);
            return graph;
            // return new FlowGraph()
            // {
            //     units =
            //     {
            //         new DirectExecuteUnit()
            //     }
            // };
        }

        public void InitGraph(FlowGraph dataDeserializeBeforeGraph)
        {
            if (dataDeserializeBeforeGraph == null)
            {
                var graph = DefaultGraph();
                graph.ScriptMachine = this;
                nest.embed = graph;
            }
            else
            {
                dataDeserializeBeforeGraph.ScriptMachine = this;
                nest.embed = dataDeserializeBeforeGraph;
            }
        }

        public Flow CreateFlow()
        {
            Flow flow = Flow.New(reference);
            // flow.ScriptMachine = this;
            return flow;
        }

        public Flow DirectlyExecuteScriptGraph()
        {
            var flow = Flow.New(reference);
            var startUnit = GetStartUnit(graph);
            if (startUnit == null)
            {
                Debug.Log("start unit is null!");
                return flow;
            }

            // flow.ScriptMachine = this;
            flow.IsFinished = false;
            flow.StartCoroutine(startUnit.Exit);

            return flow;
        }

        public static DirectExecuteUnit GetStartUnit(FlowGraph graph)
        {
            foreach (var unit in graph.units)
            {
                if (unit is DirectExecuteUnit directExecuteUnit)
                {
                    return directExecuteUnit;
                }
            }
            return null;
        }

        public static void  ProcessUseData(FlowGraph graph, List<UnitUseData> useDataList, UniBroadcastScriptNode broadcastScriptNode = null)
        {
            if (graph != null && graph.units != null)
            {
                if (useDataList == null || useDataList.Count == 0)
                    return;

                foreach (var useData in useDataList)
                {
                    if (string.IsNullOrEmpty(useData.NewKey))
                        continue;
                    if (useData.UseType == UnitUseType.GlobalBlackBoard)
                    {
                        graph.units.ForEach(unit =>
                        {
                            if (unit is GetGlobalBlackboardVariableUnit globalUnit)
                            {
                                if (globalUnit.BlackboardKey == useData.OriginKey)
                                    globalUnit.BlackboardKey = useData.NewKey;
                            }
                        });
                    }
                    else if (useData.UseType == UnitUseType.PlayerBlackBoard)
                    {
                        graph.units.ForEach(unit =>
                        {
                            if (unit is GetUniPropertyDataUnit getUniPropertyUnit && getUniPropertyUnit.CheckPlayerVariable(out var index))
                            {
                                if (getUniPropertyUnit.PropertyInfo != null &&
                                    getUniPropertyUnit.PropertyInfo.Count > index)
                                {
                                    var key = getUniPropertyUnit.PropertyInfo[index];
                                    if (key == useData.OriginKey)
                                        getUniPropertyUnit.PropertyInfo[index] = useData.NewKey;
                                }
                            }
                        });
                    }
                    else if (useData.UseType == UnitUseType.Broadcast)
                    {
                        graph.units.ForEach(unit =>
                        {
                            if (unit is GetObjectCommandUnit commandUnit && commandUnit.CheckIsBroadcastCommand())
                            {
                                if (commandUnit.BroadcastName == useData.OriginKey)
                                    commandUnit.BroadcastName = useData.NewKey;
                            }
                        });

                        if (broadcastScriptNode != null && broadcastScriptNode.BroadcastName == useData.OriginKey)
                        {
                            broadcastScriptNode.BroadcastName = useData.NewKey;
                        }
                    }
                }
            }
        }

        public static BaseScriptUnit GetLastUnit(FlowGraph graph)
        {
            BaseScriptUnit unit = null;
            if (graph != null && graph.units != null)
            {
                unit = GetStartUnit(graph);
                while (unit != null && unit.Exit != null && unit.Exit.connection != null)
                {
                    if (unit.Exit.connection.destination?.unit is BaseScriptUnit nextUnit)
                    {
                        unit.isLastUnit = true;
                        unit = nextUnit;
                    }
                    else
                    {
                        break;
                    }
                }
            }
            return unit;
        }

        public string GetSerializeJson()
        {
            //var serializeData = this.Serialize(true);
            var serializeData = new UniUGCScriptJsonData(graph).Serialize(true);
            return serializeData.json;
        }

        public void DeserializeByJson(string json, ulong version = 0)
        {
            var sd = new SerializationData(json);
            object @this = this;
            try
            {
                sd.DeserializeInto(ref @this, true);
            }
            catch (Exception e)
            {
                sd = new SerializationData();
                sd.DeserializeInto(ref @this, true);
            }
            nest.source = GraphSource.Embed;
            ResumeInValidConnections();

            graph.ScriptMachine = this;
            TryFix(version);
        }

        private void TryFix(ulong version)
        {
            var v = new UniVersion(version);

            if (v.Major < 38)
            {
                List<IUnit> needRemove = new List<IUnit>();
                foreach (var unit in graph.units)
                {
                    if (unit is ConversationSentenceUnit old)
                    {
                        var newUnit = new NewConversationSentenceUnit();
                        graph.units.Add(newUnit);
                        newUnit.Spkear.SetDefaultValue(old.Spkear);
                        newUnit.SentenceContent.SetDefaultValue(old.SentenceContent);

                        if (old.Enter.hasValidConnection)
                        {
                            var preUnitOutputPort = old.Enter.connections.First().source;
                            old.Enter.Disconnect();
                            preUnitOutputPort.ValidlyConnectTo(newUnit.Enter);
                        }

                        if (old.Exit.hasValidConnection)
                        {
                            var nextUnitInputPort = old.Exit.connections.First().destination;
                            old.Exit.Disconnect();
                            newUnit.Exit.ValidlyConnectTo(nextUnitInputPort);
                        }

                        needRemove.Add(old);
                        // graph.units.Remove(old);
                    }
                    else if (unit is ConversationOptionUnit oldOptionUnit)
                    {
                        var newUnit = new NewConversationOptionUnit();
                        graph.units.Add(newUnit);
                        for (int i = NewConversationOptionUnit.DefaultOptionNum - 1; i >= 0; i--)
                        {
                            newUnit.RemoveBranch(i);
                        }

                        if (oldOptionUnit.Enter.hasValidConnection)
                        {
                            var preUnitOutputPort = oldOptionUnit.Enter.connections.First().source;
                            oldOptionUnit.Enter.Disconnect();
                            preUnitOutputPort.ValidlyConnectTo(newUnit.Enter);
                        }

                        if (oldOptionUnit.Exit.hasValidConnection)
                        {
                            var nextUnitInputPort = oldOptionUnit.Exit.connections.First().destination;
                            oldOptionUnit.Exit.Disconnect();
                            newUnit.Exit.ValidlyConnectTo(nextUnitInputPort);
                        }

                        for (int i = 0; i < oldOptionUnit.OptionTexts.Count; i++)
                        {
                            newUnit.AddBranch();
                            newUnit.OptionsList[i].SetDefaultValue(oldOptionUnit.OptionTexts[i]);
                            if (oldOptionUnit.Branches[i].hasValidConnection)
                            {
                                var nextPort = oldOptionUnit.Branches[i].connection.destination;
                                oldOptionUnit.Branches[i].Disconnect();
                                newUnit.BranchList[i].ValidlyConnectTo(nextPort);
                            }
                        }


                        needRemove.Add(oldOptionUnit);
                    }
                }

                for (int i = needRemove.Count - 1; i >= 0; i--)
                {
                    graph.units.Remove(needRemove[i]);
                }

                needRemove.Clear();
            }
        }

        public void DeserializeBlackboard(byte[] data)
        {
            Blackboard = new Uni.Mod.UniModBlackboard();
            if (data == null)
            {
                return;
            }
            Blackboard.Deserialize(data);
        }

        private void ResumeInValidConnections()
        {
            List<InvalidConnection> childToParent = new List<InvalidConnection>();
            foreach (var invalidConnection in graph.invalidConnections)
            {
                if (invalidConnection.source.key.Contains("_Parent") && invalidConnection.destination.key.Contains("_FromChildren"))
                {
                    childToParent.Add(invalidConnection);
                    var portToParent = invalidConnection.source.unit.TryGetPortToParent();
                    if (portToParent == null)
                    {
                        (invalidConnection.source.unit as Unit).AddPortToParent();
                        portToParent = invalidConnection.source.unit.TryGetPortToParent();
                    }

                    var portFromChild = invalidConnection.destination.unit.TryGetPortFromChildren();
                    if (portFromChild == null)
                    {
                        (invalidConnection.source.unit as Unit).AddPortFromChildren();
                        portFromChild = invalidConnection.destination.unit.TryGetPortFromChildren();
                    }

                    portToParent.ValidlyConnectTo(portFromChild);
                }
            }

            for (int i = childToParent.Count - 1; i >= 0; i--)
            {
                graph.invalidConnections.Remove(childToParent[i]);
            }
            childToParent.Clear();
        }
    }
}
```

`UniScriptMachine`

类继承自 `ScriptMachine`，用于在 Unity 中管理和执行脚本机器。该类包含多个字段和方法，用于处理脚本机器的初始化、执行、序列化和反序列化等功能。类中定义了几个字段，包括 `Blackboard`、`Logger`、`internalScriptGUIDList`、`curflow`、`InnerScriptUsedNodeIdList`、`UsedInnerNodeIdList` 和 `InnerScriptDataDict`。这些字段用于存储脚本机器的黑板数据、日志记录器、内部脚本 GUID 列表、当前流程、内部脚本使用的节点 ID 列表和内部脚本数据字典等信息。`CurFlow` 属性用于获取当前流程，如果 `curflow` 为空，则调用 `CreateFlow` 方法创建一个新的流程。

`DefaultGraph` 方法用于创建一个默认的流程图。该方法首先将当前脚本机器实例赋值给流程图的 `ScriptMachine` 属性。然后，创建一个 `DirectExecuteUnit` 实例，并将其添加到流程图的单元集合中。接着，创建一个 `TitleUnit` 实例，并将其添加到流程图的单元集合中。最后，将 `DirectExecuteUnit` 的 `Exit` 连接到 `TitleUnit` 的 `Enter`，并返回创建的流程图。通过这种方式，`DefaultGraph` 方法确保了流程图中至少包含一个起始单元和一个标题单元，并且它们之间有有效的连接。

`InitGraph` 方法用于初始化脚本机器的流程图。方法接受一个 `FlowGraph` 类型的参数 `dataDeserializeBeforeGraph`，表示在反序列化之前的数据流程图。如果传入的 `dataDeserializeBeforeGraph` 为空，则调用 `DefaultGraph` 方法创建一个默认的流程图，并将当前脚本机器实例赋值给流程图的 `ScriptMachine` 属性。然后，将创建的流程图嵌入到脚本机器的嵌套结构中。如果传入的 `dataDeserializeBeforeGraph` 不为空，则直接将当前脚本机器实例赋值给 `dataDeserializeBeforeGraph` 的 `ScriptMachine` 属性，并将其嵌入到脚本机器的嵌套结构中。通过这种方式，`InitGraph` 方法确保了脚本机器在初始化时总是有一个有效的流程图，无论是默认创建的还是从外部传入的。

`CreateFlow` 方法用于创建一个新的流程对象，并返回该对象。`DirectlyExecuteScriptGraph` 方法用于直接执行脚本图，首先获取起始单元，如果起始单元为空，则记录错误信息并返回流程。否则，启动协程从起始单元的 `Exit` 开始执行流程。`GetStartUnit` 方法用于获取流程图中的起始单元，遍历流程图中的所有单元，如果某个单元是 `DirectExecuteUnit` 类型，则返回该单元。

`ProcessUseData` 方法用于处理使用数据，遍历 `useDataList` 列表中的每个 `useData` 对象，并根据 `useData` 的类型更新流程图中的相应单元。`GetLastUnit` 方法用于获取流程图中的最后一个单元，从起始单元开始，沿着连接遍历所有单元，直到找到最后一个单元。

`GetSerializeJson` 方法用于将流程图序列化为 JSON 字符串。`DeserializeByJson` 方法用于从 JSON 字符串反序列化流程图，并尝试修复无效连接。`TryFix` 方法用于根据版本号修复流程图中的单元，如果版本号小于 38，则将旧的对话单元替换为新的对话单元，并更新连接。

`DeserializeBlackboard` 方法用于反序列化黑板数据。`ResumeInValidConnections` 方法用于恢复无效连接，遍历无效连接列表，找到父子连接，并重新连接它们。总体来说，这段代码实现了一个功能丰富的脚本机器类，提供了脚本机器的初始化、执行、序列化和反序列化等功能。通过这些方法，可以方便地在 Unity 中管理和操作脚本机器，提高开发效率。