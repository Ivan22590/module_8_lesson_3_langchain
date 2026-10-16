# Базовый LangChain-агент

Проект по официальному quickstart LangChain v1:
https://docs.langchain.com/oss/python/langchain/quickstart

Агент отвечает на вопросы и вызывает инструменты. Реализовано два инструмента:

- `get_weather` — демо-инструмент из quickstart (погода в городе)
- `get_order_status` — собственный инструмент для сценария автоматизации бизнеса (проверка статуса заказа по ID)

## Структура проекта

```
├── agent.py            # Агент: create_agent + два инструмента
├── requirements.txt    # Зависимости проекта
├── .env                # Секреты (не коммитится, см. .gitignore)
├── .env.example        # Шаблон .env — скопировать в .env и вписать ключ
└── .gitignore
```

## Установка и запуск

1. Создайте виртуальное окружение и установите зависимости:

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

2. Настройте API-ключ:

```powershell
Copy-Item .env.example .env
# Откройте .env и впишите реальный ключ OpenAI
```

3. Запустите агента:

```powershell
.venv\Scripts\python agent.py
```

Агент получит запрос «What is the status of order 1002?», сам вызовет
`get_order_status` и вернёт ответ модели.

## Как это работает

- Ключи читаются из `.env` через `python-dotenv` (`load_dotenv()` в `agent.py`).
- `create_agent` собирает агента: модель (`openai:gpt-4o-mini`) + инструменты + системный промпт.
- Модель сама решает, какой инструмент вызвать, по его названию и докстрингу.

## Возможные следующие шаги

- Добавить память диалога (checkpointer LangGraph)
- Подключить LangSmith для трассировки вызовов (см. закомментированные переменные в `.env.example`)
- Расширить список инструментов: CRM, почта, таблицы