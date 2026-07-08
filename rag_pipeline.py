from typing import TypedDict, List
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import re
import asyncio

from config import TOP_K
from vectorstore import build_vectorstore

# State type
class RAGState(TypedDict, total=False):
    question: str
    retrieved_docs: List[str]
    generated_sql: str
    validated_sql: str
    sql_result: List[dict]
    messages: List[dict]

# Init vectorstore & models
vectordb = build_vectorstore()
retriever = vectordb.as_retriever(search_kwargs={"k": TOP_K})

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

sql_prompt = PromptTemplate.from_template("""
        You are a SQL generator. Based on the following context, generate a SINGLE READ-ONLY SQLite SELECT query (no semicolons, no multiple statements).
        Context:
        {context}
        
        Question:
        {question}
        
        Return only the SQL SELECT statement.
        """)

async def retriever_node(state: RAGState) -> RAGState:
    docs = await retriever.ainvoke(state["question"])
    state["retrieved_docs"] = [d.page_content for d in docs]
    return state

async def sql_generator_node(state: RAGState) -> RAGState:
    """
    Generate SQL from the retrieved documents and user question.
    Cleans LLM output, removes markdown/code fences, and ensures only SELECT statements remain.
    """
    context = "\n\n".join(state.get("retrieved_docs", []))
    prompt_text = sql_prompt.format(context=context, question=state["question"])
    out = await llm.ainvoke(prompt_text)
    if hasattr(out, "content"):
        out = out.content
    out = str(out).strip()
    out = re.sub(r"```(?:sql)?\n?", "", out, flags=re.IGNORECASE).replace("```", "").strip()
    match = re.search(r"(select\b.*)", out, flags=re.IGNORECASE | re.DOTALL)
    if match:
        out = match.group(1).strip()
    else:
        out = ""
    out = out.rstrip(";").strip()
    state["generated_sql"] = out
    return state

async def main():
    question = input("Enter your question: ")
    state: RAGState = {"question": question}
    state = await retriever_node(state)
    print("\n--- Retrieved Docs ---\n", *state["retrieved_docs"], sep="\n\n")
    state = await sql_generator_node(state)
    print("\n--- Generated SQL ---\n", state["generated_sql"])

if __name__ == "__main__":
    asyncio.run(main())
