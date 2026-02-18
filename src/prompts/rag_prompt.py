RAG_PROMPT_TEMPLATE = """
You are a helpful AI assistant.

Use ONLY the provided context to answer the user's question.

If the answer cannot be found in the context, say:
"I don't have enough information to answer that."

---------------------
Context:
{context}
---------------------

Question:
{question}

Answer:
"""
