import logging

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.prompts import render_jinja_prompt
from config import BASE_URL, PROVIDER, MODEL, OPENROUTER_API_KEY
from tools.calculate import bash_python
from tools.news import get_news
from tools.price import get_price
from tools.search import search
from tools.trade import buy, sell
from utils import now_str

logger = logging.getLogger(__name__)


async def run_agent():
    graph = await build_agent_graph()

    input = HumanMessage(content=f"Please analyze and update today's ({now_str()}) positions.")

    async for event in graph.astream({"messages": input},
                                     config=RunnableConfig(recursion_limit=50),
                                     stream_mode="updates"):
        # Получаем сообщения от первого найденного узла графа
        messages = next(
            (event[node].get("messages", [])
             for node in ["model", "tools"]
             if node in event),
            []
        )
        for message in messages:
            if content := message.content.strip():
                logger.info(f"{message.type, content}")


async def build_agent_graph():
    system_prompt = await render_jinja_prompt()

    llm = ChatOpenAI(base_url=BASE_URL, model=f"{PROVIDER}/{MODEL}", api_key=OPENROUTER_API_KEY,
                     temperature=0.1, max_retries=5, timeout=10)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    tools = [bash_python, get_news, get_price, search, buy, sell]
    agent = prompt | llm.bind_tools(tools)

    async def call_model(state: MessagesState):
        try:
            response = await agent.ainvoke(state)
        except Exception as e:
            logger.error(f"Error in call_model: {e}")
            response = AIMessage(content=f"Произошла ошибка при обработке запроса: {str(e)}")
        return {"messages": [response]}

    # Построение графа
    builder = StateGraph(MessagesState)
    builder.add_node("model", call_model)
    builder.add_node("tools", ToolNode(tools, handle_tool_errors=True))

    # Маршрутизация
    builder.add_edge(START, "model")
    builder.add_conditional_edges("model", tools_condition)
    builder.add_edge("tools", "model")

    return builder.compile()
