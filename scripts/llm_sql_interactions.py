from operator import itemgetter
from pprint import pprint

from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from pyprojroot import here

"""
# ==============================================================
# Define LLM to use
# ==============================================================
"""
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0)

"""
# ==============================================================
# Define SQL Database
# ==============================================================
"""
sqldb_directory = here("data/myduckdb.db")

db = SQLDatabase.from_uri(f"duckdb:///{sqldb_directory}")
print(db.dialect)
print(db.get_usable_table_names())
context = db.get_context()
pprint(context)
table_info = db.get_table_info(["amazon"])
pprint(table_info)
db.run("SELECT * FROM amazon LIMIT 10;")

"""
# ==============================================================
# Create SQL Query Chain
# ==============================================================
"""
chain = create_sql_query_chain(llm, db)
chain.get_prompts()[0].pretty_print()
# response = chain.invoke({"question": "How many rows are there in the zomato table?"})
response = chain.invoke({"question": "How many entries per date in the amazon table?"})
# response holds the query object
print(response)
# here is how to run the query - manually
db.run(response)

"""
# ==============================================================
# Enhance SQL Query Chain with Query Execution
# ==============================================================
"""

# altogether
question = {"question": "How many entries per date in the amazon table? Bring me all entries"}
query_chain = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)
chain_with_query_execution = query_chain | execute_query
chain_with_query_execution.invoke(question)

# inspect the prompt
query_chain.get_prompts()[0].pretty_print()
# inspect the generated query
pprint(query_chain.invoke(question))
# inspect the query execution tool
type(execute_query)
print(execute_query.name)
print(execute_query.description)


"""
# ==============================================================
# Enhance SQL Query Chain with Query Execution and Answering
# ==============================================================
"""
system_role = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n
    Question: {question}\n
    SQL Query: {query}\n
    SQL Result: {result}\n
    Answer:
    """

write_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)
answer_prompt = PromptTemplate.from_template(system_role)
answer = answer_prompt | llm | StrOutputParser()

# Even though the query key is not explicitly mentioned in the system_role template at this point, it is being prepared for later use.
# The system_role template does not need to know about the query key initially; it is filled with the actual values at the end of the chain.
chain = RunnablePassthrough.assign(query=write_query).assign(result=itemgetter("query") | execute_query) | answer

chain.invoke({"question": "How many entries per date in the amazon table?"})

"""
# ==============================================================
# Create SQL Agent
# ==============================================================
"""
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True, top_k=100)

# To check the prompt of the agent, you can use the following code:
agent_executor.agent.runnable.get_prompts()[0].pretty_print()

message = "What's the count and agent rating by category in the amazon dataset? Order results in descending order based on count"
response = agent_executor.invoke({"input": message})
print(response["output"])

"""
# ==============================================================
# Fiddling with the SQL Agent
# ==============================================================
"""
custom_prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad"],
    template="""
    ================================ System Message ================================

    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct duckdb query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 100 results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the below tools. Only use the information returned by the below tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    You MUST return the results directly as raw data without any additional explanation or post-processing.

    If the question does not seem related to the database, just return "I don't know" as the answer.


    ================================ Human Message =================================

    {input}

    ================================== Ai Message ==================================

    I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.

    ============================= Messages Placeholder =============================

    {agent_scratchpad}
    """,
)

agent_executor = create_sql_agent(llm=llm, db=db, agent_type="openai-tools", prompt=custom_prompt, verbose=True)


# To check the prompt of the agent, you can use the following code:
agent_executor.agent.runnable.get_prompts()[0].pretty_print()
# [x for x in dir(agent_executor.agent.runnable) if not x.startswith("_")]


# message = "What's the count and agent rating by category in the amazon dataset? Order results in descending order based on count"
# message = "What's the number of sales per order date in the amazon dataset? Order results in ascending order based on order date. if more than 100 lines, return 100 first lines"
message = "what's the average delivery time per traffic, area and order_date for the amazon dataset?"

response = agent_executor.invoke({"input": message})

print(response["output"])
