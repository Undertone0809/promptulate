from promptulate.utils import StringTemplate

PLAN_SYSTEM_PROMPT = """
For the given objective, come up with a simple step by step plan.
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps.
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

{{user_target}}
"""  # noqa

REVISE_SYSTEM_PROMPT = """
For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

Your objective was this:
{{user_target}}

Your original plan was this:
{{original_plan}}

You have currently done the follow steps:
{{past_steps}}

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan.
"""  # noqa

PLAN_SYSTEM_PROMPT_TMP = StringTemplate(PLAN_SYSTEM_PROMPT, "jinja2")
REVIEW_SYSTEM_PROMPT_TMP = StringTemplate(REVISE_SYSTEM_PROMPT, "jinja2")
