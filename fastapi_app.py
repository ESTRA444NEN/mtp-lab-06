"""FastAPI JSON endpoint, Pydantic models, and a local WebSocket chat."""

from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, ValidationError

app = FastAPI(title="Лабораторная № 6 — вариант 5")


class MessageIn(BaseModel):
    author: str = Field(min_length=1, max_length=30)
    text: str = Field(min_length=1, max_length=500)


class MessageOut(MessageIn):
    sent_at: datetime


clients: set[WebSocket] = set()


@app.get("/api/info")
def info() -> dict[str, str]:
    """Return a JSON response, exercise 7."""
    return {"message": "Привет FastAPI!", "laboratory": "6", "variant": "5"}


@app.post("/api/messages", response_model=MessageOut)
def validate_message(message: MessageIn) -> MessageOut:
    """Demonstrate request and response validation with Pydantic."""
    return MessageOut(**message.model_dump(), sent_at=datetime.now(timezone.utc))


@app.get("/", response_class=HTMLResponse)
def chat_page() -> str:
    return Path(__file__).with_name("chat.html").read_text(encoding="utf-8")


@app.websocket("/ws")
async def chat(socket: WebSocket) -> None:
    await socket.accept()
    clients.add(socket)
    try:
        while True:
            raw = await socket.receive_text()
            try:
                message = MessageIn.model_validate_json(raw)
            except ValidationError:
                await socket.send_json({"error": "Укажите автора и текст (до 500 символов)"})
                continue
            outgoing = MessageOut(**message.model_dump(), sent_at=datetime.now(timezone.utc))
            for client in tuple(clients):
                try:
                    await client.send_json(outgoing.model_dump(mode="json"))
                except (WebSocketDisconnect, RuntimeError):
                    clients.discard(client)
    except WebSocketDisconnect:
        pass
    finally:
        clients.discard(socket)
