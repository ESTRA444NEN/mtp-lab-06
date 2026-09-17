# Лабораторная работа № 6 — веб-программирование на Python

Старостин Андрей Павлович, группа 221141, вариант 5, лабораторная № 6.

| Уровень | № | Задание | Реализация |
| --- | --- | --- | --- |
| Средний | 5 | Страница с Bootstrap | `flask_app.py`, `templates/index.html` |
| Средний | 7 | FastAPI endpoint возвращает JSON | `fastapi_app.py`: `/api/info` |
| Средний | 1 | Flask «Hello World» | `flask_app.py`: `/hello` |
| Повышенный | 6 | WebSocket-чат на FastAPI | `fastapi_app.py`: `/ws`, `chat.html` |
| Повышенный | 8 | Pydantic-схемы | `MessageIn`, `MessageOut` в `fastapi_app.py` |

Нужен Python 3.10 или новее. Установите зависимости: `python -m pip install -r requirements.txt`.

Откройте два терминала:

```bash
python flask_app.py
python -m uvicorn fastapi_app:app --port 8000
```

Flask: `http://127.0.0.1:5000/` и `/hello`. FastAPI: `http://127.0.0.1:8000/`, `/api/info`, `/docs`. Для демонстрации чата откройте главную страницу FastAPI в двух вкладках и отправьте сообщения. Чат хранит подключения только в памяти запущенного процесса; после перезапуска история не сохраняется. Запрос `POST /api/messages` проверяет вход и ответ по схемам Pydantic.

Проверка: `python -m unittest -v`. GitHub Actions устанавливает зависимости и проверяет Flask-страницу, JSON, схемы Pydantic и обмен сообщениями между двумя WebSocket-клиентами.
