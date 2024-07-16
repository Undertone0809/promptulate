from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine, text

username = "root"
password = "123456"
hostname = "localhost"
port = "3306"
database = "world"
connection_string = (
    f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
)
# 创建Engine对象
engine = create_engine(connection_string)

db = SQLDatabase(engine)
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    api_key="sk-78ced6783e9e43c68a24c05470b985b0",
    base_url="https://api.deepseek.com",
)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
context = toolkit.get_context()
tools = toolkit.get_tools()
messages = [
    HumanMessagePromptTemplate.from_template("{input}"),
    AIMessage(content=SQL_FUNCTIONS_SUFFIX),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]

prompt = ChatPromptTemplate.from_messages(messages)
prompt = prompt.partial(**context)
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
)
agent_executor.invoke({"input": "请帮我在city表中查询出所有城市名称"})
