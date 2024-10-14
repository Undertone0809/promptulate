import argparse

from example.tot.methods.bfs import solve
from example.tot.tasks.game24 import Game24Task

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
# print("Answers:", ys[0])
