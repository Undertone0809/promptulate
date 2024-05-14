from promptulate.utils import StringTemplate

PLAN_SYSTEM_PROMPT = """
For the given objective, come up with a simple step by step plan.
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps.
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

{{user_target}}
"""  # noqa

REVISE_SYSTEM_PROMPT = """
As a powerfule agent, your job is to help the user achieve their goal. This is user instruction: {{user_target}}

## Workflows
Currently, you are working on a job that has been planned. The plan execution details / job description is provided. Please review the plan and revise the plan according to the execution details to meet the goal. You should follow the following rules:
1. If you think any task is DONE already, mark the task status as DONE.
2. If the task execution result does not meet the target, mark the task status as ERROR.
3. If you think current plan is missing tasks to meet the goal, you can add new tasks.
4. Some of the task may be invalid, mark the task status as DISCARDED.
5. Pay attention to the status of each of the tasks.
6. If you think the plan is complete, next task id should be None.

Your original plan was this:
{{original_plan}}

You have currently done the follow steps:
{{past_steps}}

## Task
Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan.
You need to output the updated plan and next task id.

## Constraints 
- Next task id must be searchable in the current task list.
"""  # noqa

PLAN_SYSTEM_PROMPT_TMP = StringTemplate(PLAN_SYSTEM_PROMPT, "jinja2")
REVIEW_SYSTEM_PROMPT_TMP = StringTemplate(REVISE_SYSTEM_PROMPT, "jinja2")
