from promptulate.utils.string_template import StringTemplate

PROMPT_TEMPLATE = """You are provided a math problem, you should transalte it into a math expression.

## Output format
Output the following JSON format, No explanation:
{"expression": "the expression need to calculate"}

For example:
1. 
Question: What is 37593 * 67?
Output:
{"expression": "37593 * 67"}

2.
Question: What is 37593^(1/5)?
Output:
{"expression": "37593**(1/5)"}

## Question
{{question}}
"""  # noqa

prompt_template = StringTemplate(PROMPT_TEMPLATE, template_format="jinja2")
