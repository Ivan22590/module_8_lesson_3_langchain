"""
Базовый LangChain-агент по образцу официального quickstart:
https://docs.langchain.com/oss/python/langchain/quickstart

Два инструмента:
- get_weather      — демо-инструмент из quickstart
- get_order_status — собственный инструмент (сценарий автоматизации бизнеса)
"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool

# Загружаем переменные окружения из .env (ключ OPENAI_API_KEY и др.)
load_dotenv()


# --- Инструмент из примера quickstart -------------------------------------
@tool
def get_weather(city: str) -> str:
    """Возвращает текущую погоду для указанного города."""
    return f"It's always sunny in {city}!"


# --- Собственный инструмент (автоматизация бизнеса: статус заказа) --------
ORDERS = {
    "1001": {"status": "shipped",    "items": "Keyboard",   "eta": "2026-10-20"},
    "1002": {"status": "processing", "items": "Monitor",    "eta": "2026-10-24"},
    "1003": {"status": "delivered",  "items": "USB Cable",  "eta": None},
}


@tool
def get_order_status(order_id: str) -> str:
    """Возвращает текущий статус заказа клиента по его идентификатору."""
    order = ORDERS.get(order_id)
    if order is None:
        return f"Order {order_id} not found."
    eta_part = f", ETA: {order['eta']}" if order["eta"] else ""
    return (
        f"Order {order_id}: status = {order['status']}, "
        f"items = {order['items']}{eta_part}"
    )


def main() -> None:
    # Ключ читается из .env (через load_dotenv) или из переменных окружения.
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY не задан.\n"
            "Скопируйте .env.example в .env и впишите туда реальный ключ,\n"
            "либо задайте его в PowerShell: $env:OPENAI_API_KEY = 'sk-...'"
        )

    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[get_weather, get_order_status],
        system_prompt=(
            "You are a helpful customer service assistant. "
            "Use tools to answer questions about weather and order statuses."
        ),
    )

    # Тестовый запрос, задействующий собственный инструмент
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What is the status of order 1002?"}]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()