from promptulate.utils.string_template import StringTemplate

PROMPT_TEMPLATE = """Now you are an intelligent voice assistant,
 and the user will input "{question}" to you.
Please determine if the user has one of the following intents:
{rule_key}
If it matches, please respond with a corresponding numeric label, such as 1.
Please avoid providing any additional explanations or judgments.
If none of them match, please indicate that you couldn't identify
the user's intent and provide a reason,without providing any numbers."""
prompt_template = StringTemplate(PROMPT_TEMPLATE)
