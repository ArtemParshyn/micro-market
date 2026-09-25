# FastAPI → RabbitMQ → Telegram

API publishes to a queue; the bot consumes and sends messages to Telegram.

## Setup

```bash
cp .env.example .env   # set BOT_TOKEN
docker compose up -d --build
```

- API: http://localhost:8000/health
- RabbitMQ UI: http://localhost:15672 (`guest`/`guest`)

```bash
curl -X POST http://localhost:8000/send \
  -H "Content-Type: application/json" \
  -d '{"chat_id": 123456789, "text": "hello"}'
```

User must `/start` the bot first. Get `chat_id` via [@userinfobot](https://t.me/userinfobot).
