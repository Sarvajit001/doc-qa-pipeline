from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from pipeline import get_vectorstore

# llm = ChatGroq(model="llama-3.3-70b-versatile", max_tokens=1024, temperature=0)
llm = ChatGroq(model="openai/gpt-oss-120b", max_tokens=1024, temperature=0)


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


SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

For ANY question that could relate to a document's content - even loosely -
you MUST use the search_document tool first, rather than answering from your own knowledge.
Only skip search_document if the question is clearly unrelated to any document, like pure math or general chit-chat.

Use the calculator tool for any math or arithmetic question.

Never write or generate code, regardless of what is asked.
If asked to write code, politely refuse and explain you're a document assistant, not a code generator.

If search_document returns "No relevant content found in the document", say clearly
that the document doesn't contain that information - do not guess or use outside knowledge.

Always tell the user which tool(s) you used, or explicitly say you used no tool and why."""


def run_agent(user_input: str, filepath: str = None, max_retries: int = 2):
    tools = [calculator]
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
            return final_message.content
        except Exception as e:
            last_error = e
            print(f"[AGENT RETRY {attempt + 1}] Tool call failed, retrying... ({e})")

    return f"Sorry, I had trouble processing that request after {max_retries + 1} attempts. Please try rephrasing your question."