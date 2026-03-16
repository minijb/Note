---
tags:
  - 面试
---
## PlayerPrefs json 二进制 存储的区别

PlayerPrefs类是一种轻量级的，用于数据存储和检索的工具，它允许我们在玩家的设备上存储少量的数据
- 通过键值对
- 对于简单数据结构

json ： 字符串，适合网络传输
二进制 ： 容量小


## 有限状态机

### 基础的有限状态机

FSM -- 有限状态机

**定义状态 --- enum** 

```c#
/// <summary>
/// Place the labels for the Transitions in this enum. —— 在此枚举中放置转换的标签。
/// Don't change the first label, NullTransition as FSMSystem class uses it. —— 不要改变第一个标签：NullTransition，因为FSMSystem类使用它。
/// </summary>
public enum Transition
{
    NullTransition = 0, // Use this transition to represent a non-existing transition in your system —— 使用此转换表示系统中不存在的转换
    Game,               //转到游戏
    Menu                //转到菜单
}

/// <summary>
/// Place the labels for the States in this enum. ——  在此枚举中放置状态的标签。
/// Don't change the first label, NullStateID as FSMSystem class uses it.不要改变第一个标签：NullStateID，因为FSMSystem类使用它。
/// </summary>
public enum StateID
{
    NullStateId = 0, // Use this ID to represent a non-existing State in your system —— 使用此ID表示系统中不存在的状态
    Menu,            //菜单
    Game             //游戏
}
```

**定义 FSM 中的状态 主要用以同意管理，所有可行的状态**

```c#
/// <summary>
/// This class represents the States in the Finite State System.该类表示有限状态系统中的状态。
/// Each state has a Dictionary with pairs (transition-state) showing 每个状态都有一个对显示(转换状态)的字典
/// which state the FSM should be if a transition is fired while this state is the current state.如果在此状态为当前状态时触发转换，则FSM应处于那种状态。
/// Method Reason is used to determine which transition should be fired .方法原因用于确定应触发哪个转换。
/// Method Act has the code to perform the actions the NPC is supposed do if it's on this state.方法具有执行NPC动作的代码应该在这种状态下执行。
/// </summary>
public abstract class FSMState : MonoBehaviour
{
    public    Dictionary<Transition, StateID> map = new Dictionary<Transition, StateID>(); //字典 《转换，状态ID》
    protected StateID                         stateID;                                     //私有ID
    public    StateID                         ID                                           //状态ID
    {
        get { return stateID; }
    }


    protected GameManager manager; //保证子类状态可以访问到总控 GameManager
    public    GameManager Manager
    {
        set { manager = value; }
    }


    /// <summary>
    /// 添加转换
    /// </summary>
    /// <param name="trans">转换状态</param>
    /// <param name="id">转换ID</param>
    public void AddTransition(Transition trans, StateID id)
    {
        if (trans == Transition.NullTransition) // Check if anyone of the args is invalid —— //检查是否有参数无效
        {
            Debug.LogError("FSMState ERROR: NullTransition is not allowed for a real transition");
            return;
        }

        if (id == StateID.NullStateId)
        {
            Debug.LogError("FSMState ERROR: NullStateID is not allowed for a real ID");
            return;
        }

        if (map.ContainsKey(trans)) // Since this is a Deterministic FSM,check if the current transition was already inside the map —— 因为这是一个确定性FSM，检查当前的转换是否已经在字典中
        {
            Debug.LogError("FSMState ERROR: State " + stateID.ToString() + " already has transition " + trans.ToString() +
                           "Impossible to assign to another state");
            return;
        }

        map.Add(trans, id);
    }


    /// <summary>
    /// This method deletes a pair transition-state from this state's map. —— 该方法从状态映射中删除一对转换状态。
    /// If the transition was not inside the state's map, an ERROR message is printed. —— 如果转换不在状态映射内，则会打印一条错误消息。
    /// </summary>
    public void DeleteTransition(Transition trans)
    {
        if (trans == Transition.NullTransition) // Check for NullTransition —— 检查状态是否为空
        {
            Debug.LogError("FSMState ERROR: NullTransition is not allowed");
            return;
        }

        if (map.ContainsKey(trans)) // Check if the pair is inside the map before deleting —— 在删除之前，检查这一对是否在字典中
        {
            map.Remove(trans);
            return;
        }
        Debug.LogError("FSMState ERROR: Transition " + trans.ToString() + " passed to " + stateID.ToString() +
                       " was not on the state's transition list");
    }


    /// <summary>
    /// This method returns the new state the FSM should be if this state receives a transition and—— 如果该状态接收到转换,该方法返回FSM应该为新状态
    /// 得到输出状态
    /// </summary>
    public StateID GetOutputState(Transition trans)
    {
        if (map.ContainsKey(trans)) // Check if the map has this transition —— 检查字典中是否有这个状态
        {
            return map[trans];
        }
        return StateID.NullStateId;
    }


    /// <summary>
    /// This method is used to set up the State condition before entering it. —— 该方法用于在进入状态条件之前设置状态条件。
    /// It is called automatically by the FSMSystem class before assigning it to the current state.—— 在分配它之前，FSMSystem类会自动调用它到当前状态
    /// </summary>
    public virtual void DoBeforeEntering()
    {
    }


    /// <summary>
    /// 此方法用于在FSMSystem更改为另一个变量之前进行任何必要的修改。在切换到新状态之前，FSMSystem会自动调用它。
    /// This method is used to make anything necessary, as reseting variables
    /// before the FSMSystem changes to another one. It is called automatically
    /// by the FSMSystem before changing to a new state.
    /// </summary>
    public virtual void DoBeforeLeaving()
    {
    }


    /// <summary>
    /// 这个方法决定状态是否应该转换到它列表上的另一个NPC是对这个类控制的对象的引用
    /// This method decides if the state should transition to another on its list
    /// NPC is a reference to the object that is controlled by this class
    /// </summary>
    public virtual void Reason()
    {
    }


    /// <summary>
    /// 这种方法控制了NPC在游戏世界中的行为。
    /// NPC做的每一个动作、动作或交流都应该放在这里
    /// NPC是这个类控制的对象的引用
    /// This method controls the behavior of the NPC in the game World.
    /// Every action, movement or communication the NPC does should be placed here
    /// NPC is a reference to the object that is controlled by this class
    /// </summary>
    public virtual void Act()
    {
    }
}
```


**状态列表**

```c#
/// <summary>
///  FSMSystem class represents the Finite State Machine class.FSMSystem类表示有限状态机类。
///  It has a List with the States the NPC has and methods to add, 它句有一个状态列表，NPC有添加、删除状态和更改机器当前状态的方法。
///  delete a state, and to change the current state the Machine is on.
/// </summary>
public class FSMSystem
{
    private List<FSMState> states; //状态集

    // The only way one can change the state of the FSM is by performing a transition 改变FSM状态的唯一方法是进行转换
    // Don't change the CurrentState directly 不要直接改变当前状态
    private StateID currentStateID;
    public  StateID CurrentStateID
    {
        get { return currentStateID; }
    }
    private FSMState currentState;
    public  FSMState CurrentState
    {
        get { return currentState; }
    }


    /// <summary>
    /// 默认构造函数
    /// </summary>
    public FSMSystem()
    {
        states = new List<FSMState>();
    }


    /// <summary>
    /// 设置当前状态
    /// </summary>
    /// <param name="state">初始状态</param>
    public void SetCurrentState(FSMState state)
    {
        currentState   = state;
        currentStateID = state.ID;
        state.DoBeforeEntering(); //开始前状态切换
    }


    /// <summary>
    /// This method places new states inside the FSM, —— 这个方法在FSM内部放置一个放置一个新状态
    /// or prints an ERROR message if the state was already inside the List. —— 或者，如果状态已经在列表中，则打印错误消息。
    /// First state added is also the initial state. 第一个添加的状态也是初始状态。
    /// </summary>
    public void AddState(FSMState fsmState, GameManager manager)
    {
        // Check for Null reference before deleting 删除前判空
        if (fsmState == null)
        {
            Debug.LogError("FSM ERROR: Null reference is not allowed");
        }
        else // First State inserted is also the Initial state, —— 插入的第一个状态也是初始状态，// the state the machine is in when the simulation begins —— 状态机是在模拟开始时
        {
            fsmState.Manager = manager; //给每个状态添加总控 GameManager

            if (states.Count == 0)
            {
                states.Add(fsmState);
                return;
            }


            foreach (FSMState state in states) // Add the state to the List if it's not inside it 如果状态不在列表中，则将其添加到列表中  （添加状态ID）
            {
                if (state.ID == fsmState.ID)
                {
                    Debug.LogError("FSM ERROR: Impossible to add state " + fsmState.ID.ToString() +
                                   " because state has already been added");
                    return;
                }
            }

            states.Add(fsmState);
        }
    }


    /// <summary>
    /// This method delete a state from the FSM List if it exists,  —— 这个方法从FSM列表中删除一个存在的状态，
    ///   or prints an ERROR message if the state was not on the List. —— 或者，如果状态不存在，则打印错误信息
    /// </summary>
    public void DeleteState(StateID id)
    {
        if (id == StateID.NullStateId) // Check for NullState before deleting —— 判空
        {
            Debug.LogError("FSM ERROR: NullStateID is not allowed for a real state");
            return;
        }


        foreach (FSMState state in states) // Search the List and delete the state if it's inside it  搜索列表并删除其中的状态
        {
            if (state.ID == id)
            {
                states.Remove(state);
                return;
            }
        }
        Debug.LogError("FSM ERROR: Impossible to delete state " + id.ToString() +
                       ". It was not on the list of states");
    }


    /// <summary>
    /// This method tries to change the state the FSM is in based on
    /// the current state and the transition passed. If current state
    ///  doesn't have a target state for the transition passed, 
    /// an ERROR message is printed.
    /// 该方法尝试根据当前状态和已通过的转换改变FSM所处的状态。如果当前状态没有传递的转换的目标状态，则输出错误消息。
    /// </summary>
    public void PerformTransition(Transition trans)
    {
        if (trans == Transition.NullTransition) // Check for NullTransition before changing the current state 在更改当前状态之前检查是否有NullTransition
        {
            Debug.LogError("FSM ERROR: NullTransition is not allowed for a real transition");
            return;
        }


        StateID id = currentState.GetOutputState(trans); // Check if the currentState has the transition passed as argument 检查currentState是否将转换作为参数传递
        if (id == StateID.NullStateId)
        {
            Debug.LogError("FSM ERROR: State " + currentStateID.ToString() + " does not have a target state " +
                           " for transition " + trans.ToString());
            return;
        }


        currentStateID = id; // Update the currentStateID and currentState		更新当前状态和ID
        foreach (FSMState state in states)
        {
            if (state.ID == currentStateID)
            {
                currentState.DoBeforeLeaving(); // Do the post processing of the state before setting the new one 在设置新状态之前是否对状态进行后处理
                currentState = state;
                currentState.DoBeforeEntering(); // Reset the state to its desired condition before it can reason or act 在它推动和动作之前，重置状态到它所需的条件
                break;
            }
        }
    }
}
```

## 行为树

### 基础节点

Seqencer ： 流控制 -- 控制一个流的执行，
按顺序执行之后的节点，一旦一个失败，Seqencer失败。 --- and

selector : 全部失败的时候，返回失败 ---- or




## AB 包加载流程

## UI性能分析
