# Combined with ToT in-depth reasoning Game24 
This demo shows using bfs+ToT+pne to implement Game24 with input data of 4, 5, 6, 10.

ToT (Tree of Thoughts) is an inference framework based on DFS(Depth First Search). 
After the introduction of ToT, LM will systematically explore a series of interrelated and most potential intermediate steps in a DFS manner when solving problems, namely "Thought". 
These thoughts are seen as the path to the final solution. 
If the current state is evaluated as unsolvable, the model will go back to the parent state and continue to explore other possibilities to ensure that effective solutions can be found to complex problems.

You see try the live demo [here](https://github.com/Undertone0809/promptulate/tree/main/example/tot).

## Output Effect

When you run the `./example/ToT/app.py`, you'll see an interface similar to the following:
```plaintext
ys: [
    '10 - 6 = 4 (left: 4 5 4)\n5 * 4 = 20 (left: 4 20)\nInput: 4 20\nInput: 4 20\n', 
    '10 - 6 = 4 (left: 4 5 4)\n5 * 4 = 20 (left: 4 20)\nInput: 4 20\n4 + 20 = 24 (left: 24)\n', 
    '10 - 6 = 4 (left: 4 5 4)\n5 * 4 = 20 (left: 4 20)\n4 + 20 = 24 (left: 24)\nAnswer: (5 * (10 - 6)) + 4 = 24\n', 
    '10 - 6 = 4 (left: 4 5 4)\n5 - 4 = 1 (left: 4 1)\nGiven the input `4 1`, the possible next steps are:\nGiven the input `4 1`, the possible next steps are:\n',
    '10 - 6 = 4 (left: 4 5 4)\n5 - 4 = 1 (left: 4 1)\nGiven the input `4 1`, the possible next steps are:\n\n']
    
Answer: (5 * (10 - 6)) + 4 = 24
```
**note:it's not deterministic, and sometimes the output can be wrong.**

## Step-by-Step Implementation

### Environment Setup

First, let's install all necessary libraries:

```text
# requirements.txt

aiohttp==3.8.4
aiosignal==1.3.1
async-timeout==4.0.2
attrs==23.1.0
backoff==2.2.1
certifi==2023.5.7
charset-normalizer==3.1.0
frozenlist==1.3.3
idna==3.4
mpmath==1.3.0
multidict==6.0.4
numpy==1.24.3
requests==2.31.0
sympy==1.12
tqdm==4.65.0
urllib3==2.0.2
yarl==1.9.2
pandas==2.0.3
pne
```

```bash
pip install -r requirements.txt
```

### Statistical table of Game24

Create a `./ToT/data/24.csv` statistical table for Game24 that contains multiple different indicators to evaluate and describe the difficulty and resolution time of different number combinations. Please refer to [here](https://github.com/Undertone0809/promptulate/tree/main/example/tot/data) for details

### Create the Game24 class

Create a `./ToT/tasks/game24.py` script and implement the `Game24Task` class:
```python
import os
import re

import pandas as pd
import sympy

from example.ToT.prompts.game24_prompts import (
    cot_prompt,
    propose_prompt,
    standard_prompt,
    value_last_step_prompt,
    value_prompt,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")


def get_current_numbers(y: str) -> str:
    last_line = y.strip().split("\n")[-1]
    return last_line.split("left: ")[-1].split(")")[0]


class Game24Task:
    """
    Input (x)   : a string of 4 numbers
    Output (y)  : a trajectory of 3 steps to reach 24
    Reward (r)  : 0 or 1, depending on whether the trajectory is correct
    Input Example:
        1 2 3 4
    Output Example:
        1 + 2 = 3 (left: 3 3 4)
        3 + 3 = 6 (left: 4 6)
        6 * 4 = 24 (left: 24)
        (1 + 2 + 3) * 4 = 24
    """

    def __init__(self, file="24.csv"):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        path = os.path.join(DATA_PATH, file)
        self.data = list(pd.read_csv(path)["Puzzles"])
        self.value_cache = {}
        self.steps = 4
        self.stops = ["\n"] * 4

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        print("self.data[idx]:", self.data[idx])
        return self.data[idx]

    def test_output(self, idx: int, output: str):
        expression = (
            output.strip().split("\n")[-1].lower().replace("answer: ", "").split("=")[0]
        )
        numbers = re.findall(r"\d+", expression)
        problem_numbers = re.findall(r"\d+", self.data[idx])
        if sorted(numbers) != sorted(problem_numbers):
            return {"r": 0}
        try:
            # print(sympy.simplify(expression))
            return {"r": int(sympy.simplify(expression) == 24)}
        except Exception:
            # print(e)
            return {"r": 0}

    @staticmethod
    def standard_prompt_wrap(x: str, y: str = "") -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y: str = "") -> str:
        return cot_prompt.format(input=x) + y

    @staticmethod
    def propose_prompt_wrap(x: str, y: str = "") -> str:
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == "24":
            prompt = cot_prompt.format(input=x) + "Steps:" + y
            # print([prompt])
        else:
            prompt = propose_prompt.format(input=current_numbers)
        return prompt

    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        last_line = y.strip().split("\n")[-1]
        if "left: " not in last_line:  # last step
            ans = last_line.lower().replace("answer: ", "")
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, answer=ans)
        current_numbers = get_current_numbers(y)
        return value_prompt.format(input=current_numbers)

    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split("\n")) == 4 and "answer" not in y.lower():
            return 0
        value_names = [_.split("\n")[-1] for _ in value_outputs]
        value_map = {"impossible": 0.001, "likely": 1, "sure": 20}  # TODO: ad hoc
        value = sum(
            value * value_names.count(name) for name, value in value_map.items()
        )
        return value

```

### Create prompt for evaluating and generating mathematical problems

Create a `./ToT/prompts/game24_prompts.py` prompt template for evaluating and generating mathematical problems, mainly used to determine whether a given number can be obtained by basic arithmetic operations (addition, subtraction, multiplication, division) to obtain 24.
```python
# 5-shot
standard_prompt = """Use numbers and basic arithmetic operations (+ - * /) to obtain 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Input: 4 9 10 13
Answer: (13 - 9) * (10 - 4) = 24
Input: 1 4 8 8
Answer: (8 / 4 + 1) * 8 = 24
Input: 5 5 5 9
Answer: 5 + 5 + 5 + 9 = 24
Input: {input}
"""

# 5-shot
cot_prompt = """Use numbers and basic arithmetic operations (+ - * /) to obtain 24.
Each step, you are only allowed to choose two of the remaining numbers
to obtain a new number.
Input: 4 4 6 8
Steps:
4 + 8 = 12 (left: 4 6 12)
6 - 4 = 2 (left: 2 12)
2 * 12 = 24 (left: 24)
Answer: (6 - 4) * (4 + 8) = 24
Input: 2 9 10 12
Steps:
12 * 2 = 24 (left: 9 10 24)
10 - 9 = 1 (left: 1 24)
24 * 1 = 24 (left: 24)
Answer: (12 * 2) * (10 - 9) = 24
Input: 4 9 10 13
Steps:
13 - 10 = 3 (left: 3 4 9)
9 - 3 = 6 (left: 4 6)
4 * 6 = 24 (left: 24)
Answer: 4 * (9 - (13 - 10)) = 24
Input: 1 4 8 8
Steps:
8 / 4 = 2 (left: 1 2 8)
1 + 2 = 3 (left: 3 8)
3 * 8 = 24 (left: 24)
Answer: (1 + 8 / 4) * 8 = 24
Input: 5 5 5 9
Steps:
5 + 5 = 10 (left: 5 9 10)
10 + 5 = 15 (left: 9 15)
15 + 9 = 24 (left: 24)
Answer: ((5 + 5) + 5) + 9 = 24
Input: {input}
"""

# 1-shot
propose_prompt = """Input: 2 8 8 14
Possible next steps:
2 + 8 = 10 (left: 8 10 14)
8 / 2 = 4 (left: 4 8 14)
14 + 2 = 16 (left: 8 8 16)
2 * 8 = 16 (left: 8 14 16)
8 - 2 = 6 (left: 6 8 14)
14 - 8 = 6 (left: 2 6 8)
14 /  2 = 7 (left: 7 8 8)
14 - 2 = 12 (left: 8 8 12)
Input: {input}
Possible next steps:
"""

value_prompt = """Evaluate if given numbers can reach 24 (sure/likely/impossible)
10 14
10 + 14 = 24
sure
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossible
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
sure
4 9 11
9 + 11 + 4 = 20 + 4 = 24
sure
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
I cannot obtain 24 now, but numbers are within a reasonable range
likely
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
I cannot obtain 24 now, but numbers are within a reasonable range
likely
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 are all too big
impossible
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 are all too small
impossible
{input}
"""

value_last_step_prompt = """Use numbers and basic arithmetic operations (+ - * /)
to obtain 24. Given an input and an answer, give a judgement (sure/impossible)
if the answer is correct, i.e. it uses each input exactly once and no other numbers,
and reach 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Judge: sure
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Judge: sure
Input: 4 9 10 13
Answer: (13 - 9) * (10 - 4) = 24
Judge:sure
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) + 1 = 25
Judge: impossible
Input: 2 9 10 12
Answer: 2 * (12 - 10) = 24
Judge:
impossible
Input: 4 9 10 13
Answer: (13 - 4) * (10 - 9) = 24
Judge: impossible
Input: {input}
Answer: {answer}
Judge:"""
```
Among them:
- Standard Prompt: Generates a straightforward answer that shows how to use a given number to get 24 through basic arithmetic operations
- CoT Prompt: Demonstrate the reasoning process at each step, step by step using a given number to get 24 through arithmetic operation
- Propose Prompt: Generates possible next steps and shows how to select two numbers from the current set of numbers to operate on
- Value Prompt: Assessing whether it is possible to get 24 through arithmetic operations for a given set of numbers
- Value Last Step Prompt: Evaluate whether the given answer is correct, i.e. whether each input number is used once and only once, and get 24 through arithmetic operation

### Create model for evaluating plan and generating text

Create a `./ToT/model.py` prompt template for evaluating and generating mathematical problems, mainly used to determine whether a given number can be obtained by basic arithmetic operations (addition, subtraction, multiplication, division) to obtain 24.
```python
import os

import promptulate as pne

api_key = os.getenv("API_KEY", "")
if api_key != "":
    api_key = api_key
else:
    print("Warning: API_KEY is not set")


def gpt(
    prompt,
    model="deepseek/deepseek-chat",
    temperature=0.7,
    max_tokens=1000,
    n=1,
    stop=None,
) -> list:
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(
        messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
    )


def chatgpt(
    messages,
    model="deepseek/deepseek-chat",
    temperature=0.7,
    max_tokens=1000,
    n=1,
    stop=None,
) -> list:
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = pne.chat(
            model=model,
            model_config={"api_key": api_key},
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            n=cnt,
            stop=stop,
        )

        outputs.extend([res])
    return outputs
```
### Create Breadth-first search (BFS) algorithm

Create a `./ToT/methods/bfs.py` Call the Game24Task class, model, and BFS to generate an evaluation solution
```python
import itertools
from functools import partial

import numpy as np

from example.ToT.model import gpt


def get_value(task, x, y, n_evaluate_sample, cache_value=True):
    value_prompt = task.value_prompt_wrap(x, y)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    if cache_value:
        task.value_cache[value_prompt] = value
    return value


def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
            local_value_cache[y] = value
        values.append(value)
    return values


def get_votes(task, x, ys, n_evaluate_sample):
    vote_prompt = task.vote_prompt_wrap(x, ys)
    vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    return values


def get_proposals(task, x, y):
    propose_prompt = task.propose_prompt_wrap(x, y)
    proposals = gpt(propose_prompt, n=1, stop=None)[0].split("\n")
    return [y + _ + "\n" for _ in proposals]


def get_samples(task, x, y, n_generate_sample, prompt_sample, stop):
    if prompt_sample == "standard":
        prompt = task.standard_prompt_wrap(x, y)
    elif prompt_sample == "cot":
        prompt = task.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f"prompt_sample {prompt_sample} not recognized")
    samples = gpt(prompt, n=n_generate_sample, stop=stop)
    return [y + _ for _ in samples]


def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print("gpt:", gpt)
    x = task.get_input(idx)  # input
    ys = [""]  # current output candidates
    infos = []
    for step in range(task.steps):
        # generation
        if args.method_generate == "sample":
            new_ys = [
                get_samples(
                    task,
                    x,
                    y,
                    args.n_generate_sample,
                    prompt_sample=args.prompt_sample,
                    stop=task.stops[step],
                )
                for y in ys
            ]
        elif args.method_generate == "propose":
            new_ys = [get_proposals(task, x, y) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))
        # evaluation
        if args.method_evaluate == "vote":
            values = get_votes(task, x, new_ys, args.n_evaluate_sample)
        elif args.method_evaluate == "value":
            values = get_values(task, x, new_ys, args.n_evaluate_sample)

        # selection
        if args.method_select == "sample":
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        elif args.method_select == "greedy":
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[
                : args.n_select_sample
            ]
        select_new_ys = [new_ys[select_id] for select_id in select_ids]

        # log
        if to_print:
            sorted_new_ys, sorted_values = zip(
                *sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True)
            )
            print(
                f"-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n"  # noqa
            )

        infos.append(
            {
                "step": step,
                "x": x,
                "ys": ys,
                "new_ys": new_ys,
                "values": values,
                "select_new_ys": select_new_ys,
            }
        )
        ys = select_new_ys
        print("new_ys:", ys)

    if to_print:
        print("ys:", ys)
    return ys, {"steps": infos}


def naive_solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    ys = get_samples(task, x, "", args.n_generate_sample, args.prompt_sample, stop=None)
    return ys, {}
```
### Create the app
Create a `./ToT/app.py` to test effect
```python
import argparse

from example.ToT.methods.bfs import solve
from example.ToT.tasks.game24 import Game24Task

args = argparse.Namespace(
    backend="deepseek/deepseek-chat",
    temperature=0.7,
    task="game24",
    naive_run=False,
    prompt_sample=None,
    method_generate="propose",
    method_evaluate="value",
    method_select="greedy",
    n_generate_sample=1,
    n_evaluate_sample=3,
    n_select_sample=5,
)

task = Game24Task()
ys, infos = solve(args, task, 900)
print(ys[0])
```

## Run the demo

You can find the project [here](https://github.com/Undertone0809/promptulate/tree/main/example/ToT). To run the application, follow these steps:

1. Fork the project by clicking [here](https://github.com/Undertone0809/promptulate/fork).
2. Clone the project locally:

   ```bash
   git clone https://github.com/Undertone0809/promptulate.git
   ```

3. Switch to the example directory:

   ```shell
   cd ./example/ToT
   ```

4. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

5. Run the application:

   ```shell
   python app.py
   ```

By following these instructions, you can easily set up and run ToT to solve in-depth reasoning Game24

Enjoy your game time!
