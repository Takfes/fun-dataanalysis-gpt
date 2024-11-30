### RESROUCES

- [Dataset : Amazon Delivery Dataset](https://www.kaggle.com/datasets/sujalsuthar/amazon-delivery-dataset)
- [Dataset : Zomato Delivery Operations Analytics Dataset](https://www.kaggle.com/datasets/saurabhbadole/zomato-delivery-operations-analytics-dataset)
- [Dataset : Logistics Company Dataset For SQL](https://www.kaggle.com/datasets/aashokaacharya/logistics-company-dataset-for-sql?select=employee_manages_shipment.csv)
- [API reference - langchain](https://python.langchain.com/api_reference/reference.html)

### RAG ON TEXT DATA

- knowledge base consisting of md, pdf files - rag through vector database to provide agent information
- for this we gonna use embeddings model, chromadb
- make sure that the pipeline is triggered when there are new files to embbed

- [prepare vectordb video](https://youtu.be/xsCedrNP9w8?si=OcuHTf7uZZiA7Abi&t=2629)
- [prepare vectordb](https://github.com/Farzad-R/Advanced-QA-and-RAG-Series/blob/main/AgentGraph-Intelligent-Q%26A-and-RAG-System/src/prepare_vector_db.py)
- [PyPDFLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFLoader.html#langchain_community.document_loaders.pdf.PyPDFLoader)
- [RecursiveCharacterTextSplitter](https://python.langchain.com/api_reference/text_splitters/character/langchain_text_splitters.character.RecursiveCharacterTextSplitter.html#langchain_text_splitters.character.RecursiveCharacterTextSplitter)
- [Chroma](https://python.langchain.com/api_reference/chroma/vectorstores/langchain_chroma.vectorstores.Chroma.html#langchain_chroma.vectorstores.Chroma)

- [query vectordb video](https://youtu.be/xsCedrNP9w8?si=_f63JC74Ft7cg2db&t=2906)
- [query vectordb](https://youtu.be/xsCedrNP9w8?si=OcuHTf7uZZiA7Abi&t=2629)
- [rag_tool.ipynb](https://github.com/Farzad-R/Advanced-QA-and-RAG-Series/blob/main/AgentGraph-Intelligent-Q%26A-and-RAG-System/Notebooks/Tools/RAG_tool_step_by_step/rag_tool.ipynb)
- [OpenAIEmbeddings](https://python.langchain.com/api_reference/openai/embeddings/langchain_openai.embeddings.base.OpenAIEmbeddings.html#langchain_openai.embeddings.base.OpenAIEmbeddings)
- "You will receive a user's query and possible content where the answer might be. If the answer is found, provide it, if not, state that the answer does not exist."

### RAG ON TABULAR DATA (MIEH!)

- [rag on tabular video](https://youtu.be/ZtltjSjFPDg?si=xebvDt4sthLfLokv&t=444)
-

### SQL AGENT

- [create sql chain](https://github.com/Farzad-R/Advanced-QA-and-RAG-Series/blob/main/AgentGraph-Intelligent-Q%26A-and-RAG-System/Notebooks/Tools/sql_agents/sql_agent_chain_steps.ipynb)
- [SQLDatabase](https://python.langchain.com/api_reference/community/utilities/langchain_community.utilities.sql_database.SQLDatabase.html#langchain_community.utilities.sql_database.SQLDatabase.get_table_info)
- QuerySQLDataBaseTool, create_sql_query_chain, create_sql_agent
- create_sql_query_chain is designed for simple queries, while create_sql_agent can handle complex, multi-step interactions. can perform iterative querying, error correction, and handle conditional logic, whereas the chain executes a single query per user input.
- [create sql agent video](https://youtu.be/ZtltjSjFPDg?si=-7Y6jyZ2j0bkMcb4&t=1731)
- [create sqsl agent github](https://github.com/Farzad-R/Advanced-QA-and-RAG-Series/blob/main/Q%26A-and-RAG-with-SQL-and-TabularData/explore/3_query_and_QA_sqldb.ipynb)

### THINGS TO TRY

- insights from graph [gpt-4-vision-preview model](https://www.youtube.com/watch?v=LO8c7oXG32M)
- [text-to-sql-visualization](https://www.youtube.com/watch?v=LRcjlXL9hPA) this brings an agent that reads the llm response and decides which is the best visualization to present the results
- langgraph studio
- configurations file and pyprojroot package
- [msft lida visualization](https://www.youtube.com/watch?v=U9K1Cu45nMQ)
- [chat2plot](https://github.com/nyanp/chat2plot?utm_source=chatgpt.com)
- [dash chat visual through code](https://www.youtube.com/watch?v=Phix-s5NPUA)
