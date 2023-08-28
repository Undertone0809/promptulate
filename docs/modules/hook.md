## What is hook?

- What is hook？钩子`hook`，顾名思义，可以理解是一个挂钩，作用是有需要的时候挂一个东西上去。具体的解释是：钩子函数是把我们自己实现的hook函数在某一时刻挂接到目标挂载点上。
- Hook是一种机制，允许开发者在应用程序或框架中的特定时刻插入自定义代码。它是一种事件触发机制，这些事件可以是系统事件、用户操作或其他特定情况。通过使用钩子，开发者可以在特定事件发生时干预应用程序的行为，例如修改数据、添加功能、执行自定义逻辑等。Hook通常以回调函数的形式存在，当特定事件发生时，系统会自动调用这些回调函数。钩子的使用可以实现灵活的扩展和定制，使得应用程序的行为可以根据实际需求进行修改。
- 举个例子，Hook的概念在windows桌面软件开发很常见，特别是各种事件触发的机制; 比如C++的MFC程序中，要监听鼠标左键按下的时间，MFC提供了一个onLeftKeyDown的钩子函数。很显然，MFC框架并没有为我们实现onLeftKeyDown具体的操作，只是为我们提供一个钩子，当我们需要处理的时候，只要去重写这个函数，把我们需要操作挂载在这个钩子里，如果我们不挂载，MFC事件触发机制中执行的就是空的操作。

因此我们可以知道：
- Hook函数是程序中预定义好的函数，这个函数处于原有程序流程当中（暴露一个钩子出来）。
- 我们需要再在有流程中钩子定义的函数块中实现某个具体的细节，需要把我们的实现，挂接或者注册（register）到钩子里，使得hook函数对目标可用。
- Hook是一种编程机制，和具体的语言没有直接的关系。
- 钩子只有注册的时候，才会使用，所以原有程序的流程中，没有注册或挂载时，执行的是空（即没有执行任何操作）

## Hook与生命周期

`promptulate`构建了一个Hook（钩子）系统，可以让`promptulate`的组件有更加细力度的功能编辑与自定义功能控制，`promptulate`在Agent，llm，Tool特定的执行节点插入用户特定的代码，下面我们用生命周期的概念来代指某个特定的执行节点。

具体地，你可以在以下几种生命周期中构建Hook。

- **Agent**
  - `on_agent_create` 在Agent初始化时触发
  - `on_agent_start` 在Agent开始运行时触发
  - `on_agent_result` 在Agent返回结果时触发
- **llm**
  - `on_llm_create` 在llm初始化时触发
  - `on_llm_start` 在llm开始运行时触发
  - `on_llm_result` 在llm返回结果时触发
- **Tool**
  - `on_tool_create` 在Tool初始化时触发
  - `on_tool_start` 在Tool开始运行时触发
  - `on_tool_result` 在Tool返回结果时触发

![](images/hook_1.png)

有了Hook，你可以在上面指定的生命周期中进行Hook挂载，从而执行特定的功能。下面的示例展示了如何监听Tool Calculator的各个生命周期并打印对应日志信息（装饰器定义）。


```python
from promptulate.hook import Hook
from promptulate.tools import Calculator


@Hook.on_tool_create(hook_type="instance")
def handle_tool_create(*args, **kwargs):
    print("math tool component create")


@Hook.on_tool_start(hook_type="instance")
def handle_tool_start(*args, **kwargs):
    prompt = args[0]
    print(f"math tool instance hook start, user prompt: {prompt}")


@Hook.on_tool_result(hook_type="instance")
def handle_tool_result(**kwargs):
    result = kwargs["result"]
    print(f"math tool component result: {result}")


def main():
    hooks = [handle_tool_create, handle_tool_start, handle_tool_result]
    tool = Calculator(hooks=hooks)
    result = tool.run("6的五次方等于多少")
    print(result)


if __name__ == "__main__":
    main()

```

输出结果如下：

```text
math tool component create
math tool instance hook start, user prompt: 6的五次方等于多少
math tool component result: 7776
7776
```

在上面的示例中，对on_tool_create、on_tool_start、on_tool_result三个生命周期构建了Hook，并且将Hook传入到需要被挂载的Calculator中，以此实现对应逻辑的挂载。通过args和kwargs，我们可以获取到生命周期执行过程中的传参，如在on_tool_start生命周期中，我们获取到了Calculator的用户输入；在on_tool_result生命周期中，我们获取到了Calculator的返回的结果。

> hook_type="instance"参数的含义在下文[hook的两种类型](#hook的两种类型)会进一步讲解。

此外，你也可以使用函数式声明的方式定义Hook，下面是一个与上面等价的示例：

```python
from promptulate.hook import Hook, HookTable
from promptulate.llms import ChatOpenAI


def handle_start(*args, **kwargs):
    print(f"llm instance start hook: {args[0]}")


def handle_result(*args, **kwargs):
    print(f"llm instance result hook: {kwargs['result']}")



Hook.registry_hook(HookTable.ON_LLM_START, handle_start, "instance")
Hook.registry_hook(HookTable.ON_LLM_RESULT, handle_result, "instance")
hooks = [handle_start, handle_result]
llm = ChatOpenAI(hooks=hooks)
llm("hello")
```

当然，我们推荐使用装饰器的方式进行声明，更为直观一些。


## Hook的两种类型

为了让Hook可以提供更加细粒度的调控，`promptulate`中将Hook分为了以下两种类型：

- **ComponentHook**

组件级Hook，挂载时将同时触发同一类型组件的指定生命周期，例如，假如你给Agent导入了五个Tool，这个时候你可以使用组件级Hook，用一个Hook函数对五个Tool的同一生命周期进行监听。

- **InstanceHook**

实例级Hook，将Hook挂载到指定组件的实例中，其只有在实例触发对应的生命周期时，Hook函数才会被调用。

下面的示例展示了ComponentHook和InstanceHook的使用方式。

```python
from promptulate.hook import Hook
from promptulate.tools import Calculator


@Hook.on_tool_create(hook_type="component")
def handle_tool_create_by_component(*args, **kwargs):
    print("math tool component create by component")


@Hook.on_tool_create(hook_type="instance")
def handle_tool_create_by_instance(*args, **kwargs):
    print("math tool component create by instance")


def main():
    hooks = [handle_tool_create_by_instance]
    tool = Calculator(hooks=hooks)
    result = tool.run("6的五次方等于多少")
    print(result)


if __name__ == "__main__":
    main()
```


## 自定义Hook

通过 `promptulate`的Hook系统，你可以在各个组件中自定义Hook系统。


## 自定义生命周期

> 待完善