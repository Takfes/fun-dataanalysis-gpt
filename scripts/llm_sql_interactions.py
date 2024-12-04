from operator import itemgetter
from pprint import pprint

from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
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
response = chain.invoke({"question": "How many entries per date in the amazon table? Don't limit the results"})
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
# agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True, top_k=100)

my_suffix = """
    As a final step, I MUST ALWAYS respond with JUST the results - NOTHING ELSE - in a json format.
    """

my_suffix = """
    I should look at the tables in the database to see what I can query.
    Then I should query the schema of the most relevant tables.\n
    As a final step, I MUST ALWAYS respond with JUST the results - NOTHING ELSE - in a json format.
    """

my_suffix = """
    I should look at the tables in the database to see what I can query.
    Then I should query the schema of the most relevant tables.\n
    As a final step, I MUST ALWAYS respond with JUST the RAW RESULTS WITHOUT any further processing or ADDING extra text.
    """

message = "What's the count and agent rating by category in the amazon dataset? Order results in descending order based on count"

agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True, top_k=100, suffix=my_suffix)
# To check the prompt of the agent, you can use the following code:
agent_executor.agent.runnable.get_prompts()[0].pretty_print()
response = agent_executor.invoke({"input": message})
print(response["output"])

"""
# ==============================================================
# Test a zero-shot agent
# ==============================================================
"""

# Part 2: Prepare the sql prompt
MSSQL_AGENT_PREFIX = """

You are an agent designed to interact with a SQL database.
## Instructions:
- Given an input question, create a syntactically correct {dialect} query
to run, then look at the results of the query and return the answer.
- Unless the user specifies a specific number of examples they wish to
obtain, **ALWAYS** limit your query to at most {top_k} results.
- You can order the results by a relevant column to return the most
interesting examples in the database.
- Never query for all the columns from a specific table, only ask for
the relevant columns given the question.
- You have access to tools for interacting with the database.
- You MUST double check your query before executing it.If you get an error
while executing a query,rewrite the query and try again.
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
to the database.
- DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS
OF THE CALCULATIONS YOU HAVE DONE.
- Your response should be in Markdown. However, **when running  a SQL Query
in "Action Input", do not include the markdown backticks**.
Those are only for formatting the response, not for executing the command.
- ALWAYS, as part of your final answer, explain how you got to the answer
on a section that starts with: "Explanation:". Include the SQL query as
part of the explanation section.
- If the question does not seem related to the database, just return
"I don\'t know" as the answer.
- Only use the below tools. Only use the information returned by the
below tools to construct your query and final answer.
- Do not make up table names, only use the tables returned by any of the
tools below.
- as part of your final answer, please include the SQL query you used in json format or code format

## Tools:

"""

MSSQL_AGENT_FORMAT_INSTRUCTIONS = """

## Use the following format:

Question: the input question you must answer.
Thought: you should always think about what to do.
Action: the action to take, should be one of [{tool_names}].
Action Input: the input to the action.
Observation: the result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer.
Final Answer: the final answer to the original input question.

Example of Final Answer:
<=== Beginning of example

Action: query_sql_db
Action Input:
SELECT TOP (10) [base_salary], [grade]
FROM salaries_2023

WHERE state = 'Division'

Observation:
[(27437.0,), (27088.0,), (26762.0,), (26521.0,), (26472.0,), (26421.0,), (26408.0,)]
Thought:I now know the final answer
Final Answer: There were 27437 workers making 100,000.

Explanation:
I queried the `xyz` table for the `salary` column where the department
is 'IGM' and the date starts with '2020'. The query returned a list of tuples
with the bazse salary for each day in 2020. To answer the question,
I took the sum of all the salaries in the list, which is 27437.
I used the following query

```sql
SELECT [salary] FROM xyztable WHERE department = 'IGM' AND date LIKE '2020%'"
```
===> End of Example

"""

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,
    format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,
    llm=llm,
    toolkit=toolkit,
    top_k=30,
    verbose=True,
)

# To check the prompt of the agent, you can use the following code:
agent_executor.agent.runnable.get_prompts()[0].pretty_print()
response = agent_executor.invoke(message)
print(response["output"])
