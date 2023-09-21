from promptulate.utils.string_template import StringTemplate

PROMPT_TEMPLATE = """
现在你是一个智能音箱，用户将向你输入”{question}“，
请判断用户是否是以下意图 
{rule_key}
如果符合你只需要回答数字标号，如1，请不要输出你的判断和额外的解释。
如果都不符合，你需要输出无法找到对应电器和对应的原因，请不要输出任何数字。
"""
prompt_template = StringTemplate(PROMPT_TEMPLATE)
