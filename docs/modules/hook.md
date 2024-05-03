## What is hook?

- `Hook`, as the name suggests, can be understood as a hook, its function is to hang something up when needed. Specifically, the explanation is: the hook function will attach our own implemented hook function to a target mounting point at a certain moment.
- A Hook is a mechanism that allows developers to insert custom code at specific moments in an application or framework. It is an event-triggering mechanism where these events can be system events, user actions, or other specific situations. By using hooks, developers can intervene in the behavior of an application when specific events occur, such as modifying data, adding functionality, executing custom logic, etc. Hooks typically exist in the form of callback functions, and when specific events occur, the system automatically calls these callback functions. The use of hooks enables flexible extension and customization, allowing the behavior of the application to be modified according to actual needs.
- For example, the concept of hooks is common in Windows desktop software development, especially various event triggering mechanisms: for example, listening to the left mouse button press event in C++ MFC programs. In MFC programs, a hook function onLeftKeyDown is provided, but this hook function does not implement the specific operation onLeftKeyDown for us. It only provides a hook for us. Therefore, when we need to handle it, we just need to override this function and mount the operation we need on this hook. If we do not mount it, the empty operation will be executed in the MFC event triggering mechanism.

Therefore, we can know that:
- The hook function is a pre-defined function in the program, and this function is in the original program flow (exposing a hook).
- If we need to implement a specific detail in a function block defined by a hook in the flow, we need to attach or register our implementation to the hook so that the hook function is available for the target.
- Hook is a programming mechanism and is not directly related to a specific language.
- Hooks are only used when registered, so in the original program flow, if not registered or mounted, it will execute nothing (i.e., no operation is performed).

## Hook & Life cycle
### 1. What is Life cycle
Lifecycle refers to a series of stages that an object or component goes through during creation, existence, and destruction. In these stages, specific operations can be performed or specific events can be handled to ensure the correct behavior and resource management of the object or component. It is like the human lifecycle, which includes stages such as infancy, childhood, adolescence, adulthood, and old age. Each stage is accompanied by different physiological, psychological development, and behaviors, ultimately forming a complete lifecycle.

### 2. Construction of hook with life cycle
Hooks are commonly used in conjunction with lifecycle methods, allowing developers to insert custom logic into the lifecycle of objects or components.

`promptulate` has built a Hook system that allows components of `promptulate` to have finer-grained function editing and custom function control. `promptulate` inserts user-specific code into specific execution nodes of Agent, llm, and Tool, and in the following text, we use the concept of lifecycle to refer to a specific execution node.

Specifically, you can mount hooks in the following lifecycles to perform specific functions:
- **Agent**
  - `on_agent_create` Triggered when the Agent is initialized
  - `on_agent_start` Triggered when the Agent starts running
  - `on_agent_result` Triggered when the Agent returns a result
- **llm**
  - `on_llm_create` Triggered when llm is initialized
  - `on_llm_start` Triggered when llm starts running
  - `on_llm_result` Triggered when llm returns a result
- **Tool**
  - `on_tool_create` Triggered when the Tool is initialized
  - `on_tool_start` Triggered when the Tool starts running
  - `on_tool_result` Triggered when the Tool returns a result

![](../images/hook_1.png)

### 3.example
The following example shows how to listen to various lifecycles of Agent Calculator and print corresponding log information (decorator definition)

```python
import promptulate as pne
from promptulate.hook import Hook
from promptulate.tools import calculator


@Hook.on_agent_create(hook_type="instance")
def handle_agent_create(**kwargs):
    print("math agent component create")


@Hook.on_agent_start(hook_type="instance")
def handle_agent_start(tool, *args, **kwargs):
    prompt = args[0]
    print(f"math agent instance hook start, user prompt: {prompt}, tool: {tool}")


@Hook.on_agent_result(hook_type="instance")
def handle_agent_result(**kwargs):
    result = kwargs["result"]
    print(f"math agent component result: {result}")


def main():
    hooks = [handle_agent_create, handle_agent_start, handle_agent_result]
    agent = pne.ToolAgent(tools=[calculator], hooks=hooks)
    result = agent.run("What is the 5 power of 6?")
    print(result)


if __name__ == "__main__":
    main()


```

The output result is as follows:

```text
math agent component create
math agent instance hook start, user prompt: What is the 5 power of 6?
math agent component result: 7776
7776
```

In the example above, hooks for on_agent_create, on_agent_start, and on_agent_result lifecycles are built, and the hooks are passed to the Calculator that needs to be mounted, thereby implementing the mounting of corresponding logic. Through args and kwargs, we can obtain the parameters passed during the lifecycle execution, such as in the on_agent_start lifecycle, we obtain the user input of Calculator; in the on_agent_result lifecycle, we obtain the result returned by Calculator.

> The meaning of the hook_type="instance" will be further explained in the section [Two Types of Hooks](#Two Types of Hooks)

Additionally, you can also define hooks using the functional declaration method, here is an equivalent example to the one above:

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

Of course, we recommend using the decorator method for declaration, which is more intuitive.

## Two Types of Hooks
In order to provide more fine-grained control, `promptulate` divides hooks into the following two types:

- **ComponentHook**
Component-level Hook, when mounted, will trigger the specified lifecycle of the same type of component simultaneously. For example, if you import five Tools to an Agent, you can use a component-level Hook to listen to the same lifecycle of the five Tools.

- **InstanceHook**
Instance-level Hook, mounts the Hook to a specific instance of a component, and the Hook function is only called when the instance triggers the corresponding lifecycle.

The following example demonstrates the usage of ComponentHook and InstanceHook.
The usage of InstanceHook is shown in the Agent Calculator example above.
The following example demonstrates the usage of component hook for Agent with 2 tools imported:

```python
import promptulate as pne
from promptulate import ChatOpenAI
from promptulate.hook import Hook
from promptulate.tools import calculator
from promptulate.tools.wikipedia import wikipedia_search

@Hook.on_tool_create(hook_type="component")
def handle_tool_create_by_component(*args, **kwargs):
    print("tool component create by component")

def main():
    llm = ChatOpenAI(model="gpt-4-1106-preview")
    agent = pne.ToolAgent(tools=[wikipedia_search, calculator],
                          llm=llm)
    response: str = agent.run("Tell me the year in which Tom Cruise's Top Gun was "
                              "released, and calculate the square of that year.")
    print(response)

if __name__ == "__main__":
    main()
```

## Custom Hook

Through the Hook system of `promptulate`, you can customize Hook systems in various components.

The following demonstrates a custom component hook for an Agent with 3 tools imported:
```python
import promptulate as pne
from promptulate.hook import Hook, HookTable
from promptulate.llms import ChatOpenAI
from promptulate.tools.math.tools import calculator
from promptulate.tools.wikipedia.tools import wikipedia_search
from promptulate.utils.color_print import print_text

# Define the component hook class
class MidStepOutHook:
    @staticmethod
    def handle_agent_start(*args, **kwargs):
        if kwargs.get("agent_type", None):
            print_text(f"[Agent] {kwargs['agent_type']} start...", "red")
        else:
            print_text("[Agent] Agent Start...", "red")

        if kwargs.get("_from", None) is None:
            print_text(f"[User instruction] {args[0]}", "blue")
        elif kwargs["_from"] == "agent":
            print_text(f"[Agent execution] {args[0]}", "blue")

    @staticmethod
    def handle_agent_plan(*args, **kwargs):
        print_text(f"[Plan] {kwargs['plan']}", "green")

    @staticmethod
    def handle_agent_revise_plan(*args, **kwargs):
        print_text(f"[Revised Plan] {kwargs['revised_plan']}", "green")

    @staticmethod
    def handle_agent_action(*args, **kwargs):
        print_text(f"[Thought] {kwargs['thought']}", "yellow")
        print_text(
            f"[Action] {kwargs['action']} args: {kwargs['action_input']}", "yellow"
        )

    @staticmethod
    def handle_agent_observation(*args, **kwargs):
        print_text(f"[Observation] {kwargs['observation']}", "yellow")

    @staticmethod
    def handle_agent_result(*args, **kwargs):
        if kwargs.get("_from", None) is None:
            print_text(f"[Agent Result] {kwargs['result']}", "green")
            print_text("[Agent] Agent End.", "pink")
        elif kwargs["_from"] == "agent":
            print_text(f"[Execute Result] {kwargs['result']}", "green")
            print_text("[Execute] Execute End.", "pink")

    @staticmethod
    def registry_hooks():
        """Registry and enable stdout hooks. StdoutHook can print colorful
        information."""
        Hook.registry_hook(
            HookTable.ON_AGENT_REVISE_PLAN,
            MidStepOutHook.handle_agent_revise_plan,
            "component",
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_ACTION, MidStepOutHook.handle_agent_action, "component"
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_OBSERVATION,
            MidStepOutHook.handle_agent_observation,
            "component",
        )

        
# Register hook function
MidStepOutHook.registry_hooks()

# Custom tool
def word_problem_tool(question: str) -> str:
    """
    Useful for when you need to answer logic-based/reasoning questions.

    Args:
        question(str): Detail question, the description of the problem requires a
        detailed question context. Include a description of the problem

    Returns:
        question answer
    """
    system_prompt: str = """You are a reasoning agent tasked with solving t he user's logic-based questions.
    Logically arrive at the solution, and be factual.
    In your answers, clearly detail the steps involved and give the final answer.
    Provide the response in bullet points."""  # noqa
    llm = ChatOpenAI()
    return llm(f"{system_prompt}\n\nQuestion:{question}Answer:")

# Create agent
llm = ChatOpenAI(model="gpt-4-1106-preview")
agent = pne.ToolAgent(tools=[wikipedia_search, calculator, word_problem_tool],
                      llm=llm)

response: str = agent.run("I have 3 apples and 4 oranges.I give half of my oranges "
                          "away and buy two dozen new ones,along with three packs of "
                          "strawberries.Each pack of strawberry has 30 "
                          "strawberries.How many total pieces of fruit do I have at "
                          "the end?")
print(response)
```

##  Custom lifecycle

> To be improved