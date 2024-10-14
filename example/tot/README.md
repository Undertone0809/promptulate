# ToT
This demo shows using pne+tot to implement Game24 with input data of 4, 5, 6, 10.

ToT (Tree of Thoughts) is an inference framework based on DFS(Depth First Search). 
After the introduction of ToT, LM will systematically explore a series of interrelated and most potential intermediate steps in a DFS manner when solving problems, namely "Thought". 
These thoughts are seen as the path to the final solution. 
If the current state is evaluated as unsolvable, the model will go back to the parent state and continue to explore other possibilities to ensure that effective solutions can be found to complex problems.

You see try the live demo [here](https://github.com/Undertone0809/promptulate/tree/main/example/tot).

# Quick Start
1. Clone the repository and install the dependencies

```shell
git clone https://www.github.com/Undertone0809/promptulate
```

2. Switch the current directory to the example

```shell
cd ./example/tot
```

3. Run the application

```shell
python app.py
```

# Output
And the output would be something like (note it's not deterministic, and sometimes the output can be wrong):
```text
ys: [
    '10 - 6 = 4 (left: 4 5 4)\n5 * 4 = 20 (left: 4 20)\nInput: 4 20\nInput: 4 20\n', 
    '10 - 6 = 4 (left: 4 5 4)\n5 * 4 = 20 (left: 4 20)\nInput: 4 20\n4 + 20 = 24 (left: 24)\n', 
    '10 - 6 = 4 (left: 4 5 4)\n5 * 4 = 20 (left: 4 20)\n4 + 20 = 24 (left: 24)\nAnswer: (5 * (10 - 6)) + 4 = 24\n', 
    '10 - 6 = 4 (left: 4 5 4)\n5 - 4 = 1 (left: 4 1)\nGiven the input `4 1`, the possible next steps are:\nGiven the input `4 1`, the possible next steps are:\n',
    '10 - 6 = 4 (left: 4 5 4)\n5 - 4 = 1 (left: 4 1)\nGiven the input `4 1`, the possible next steps are:\n\n']
    
Answer: (5 * (10 - 6)) + 4 = 24
```