ROUTER_PROMPT = "Classify the following legal query into one of: 'rag' for document retrieval, 'general' for general chat, 'task' for specific tasks like clause analysis, risk assessment, or summarization.\n\nQuery: {query}\n\nRespond with only the category."
GENERAL_PROMPT = "You are a helpful legal assistant. Answer the following query: {query}"
TASK_PROMPT = "Perform the legal task described in the query. This could be clause analysis, risk assessment, or summarization.\n\nQuery: {query}"
EVALUATOR_PROMPT = "Evaluate the quality of the following legal response. Provide feedback and a score out of 10.\n\nResponse: {response}"
