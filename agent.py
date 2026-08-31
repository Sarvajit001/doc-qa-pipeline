from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from pipeline import get_vectorstore
from tavily import TavilyClient
from dotenv import load_dotenv
# from importlib import import_module
import os
import sys
import sqlite3

load_dotenv()


# try:
#     TavilyClient = import_module("tavily").TavilyClient
# except (ImportError, AttributeError) as exc:
#     TavilyClient = None
#     _tavily_import_error = exc

DB_PATH = "./agent_conversation.db"


print("PYTHON:", sys.executable)
print("TAVILY KEY EXISTS:", bool(os.getenv("TAVILY_API_KEY")))


def _get_tavily_client():
   
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# llm = ChatGroq(model="llama-3.3-70b-versatile", max_tokens=1024, temperature=0)
llm = ChatGroq(model="openai/gpt-oss-120b", max_tokens=1024, temperature=0)


#initializing database connection
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_input TEXT NOT NULL,
            agent_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
init_db()    
    
def log_conversation(session_id,user_input, agent_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO agent_conversations (session_id,user_input, agent_response)
        VALUES (?, ?, ?)
    ''', (session_id,user_input, agent_response))
    conn.commit()
    conn.close()
    
    
def get_conversation_history(session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_input, agent_response
        FROM agent_conversations
        WHERE session_id = ?
        ORDER BY timestamp ASC
    ''', (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"user_input": q, "agent_response": a} for q,a in rows]

def clear_conversation_history(session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM agent_conversations WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()        


def make_search_tool(filepath: str):
    @tool
    def search_document(question: str) -> str:
        """
        Searches the document for content relevant to the question.
        Use this tool whenever the question could relate to the document's content.
        """
        vectorstore = get_vectorstore(filepath)
        retriever = vectorstore.as_retriever()
        context_docs = retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in context_docs])
        return context if context else "No relevant content found in the document."

    return search_document


@tool
def calculator(expression: str) -> str:
    """
    Evaluates a basic math expression and returns the result.
    Use this tool whenever the question involves a calculation, like addition,
    multiplication, percentages, or any arithmetic.
    Example input: "47 * 89" or "(120 + 30) / 2"
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Could not evaluate expression: {e}"
    
@tool
def web_search(query: str) -> str:
    """
    Searches the internet for current or external information.
    Use this for recent news, current events, current statistics,
    weather, sports information, etc.
    """

    response = _get_tavily_client().search(query=query,max_results=3)
    results = response.get("results", [])
    return "\n\n".join(
        f"{result.get('title', '')}\n{result.get('content', '')}\n{result.get('url', '')}"
        for result in results
    ) or "No web results found."


SYSTEM_PROMPT = """
You are a helpful assistant with access to three tools.

1. search_document:
   Use this when the user's question is related to the uploaded document.

2. web_search:
   Use this when the user asks for current, recent, external,
   Search the web for external and current information.
   live or time-sensitive information such as:
   - recent news
   - latest news
   - current events
   - current sports statistics
   - live cricket scores
   - current weather
   - recent incidents
   - historical information that should be verified

3. calculator:
   Use this for mathematical calculations.

For document-related questions, use search_document and answer
only from the retrieved document context.

For current or external information, use web_search.

For mathematical questions, use calculator.

If a question requires multiple tools, you may use more than one tool.

If a document search returns no relevant information,
do not guess an answer from outside knowledge.

You may generate code when the user explicitly asks for it.

Always tell the user which tool or tools were used.
"""

# Practice merge - trivial change
def run_agent(user_input: str, filepath: str = None,session_id: str = None, max_retries: int = 2):
    tools = [calculator,web_search]
    if filepath:
        tools.append(make_search_tool(filepath))

    agent_executor = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            result = agent_executor.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            final_message = result["messages"][-1]
            log_conversation(session_id, user_input, final_message.content)
            print("saved to conversation log")
            return final_message.content
        except Exception as e:
            last_error = e
            print(f"[AGENT RETRY {attempt + 1}] Tool call failed, retrying... ({e})")

    return f"Sorry, I had trouble processing that request after {max_retries + 1} attempts. Please try rephrasing your question."