# PartyWatch Backend

This backend powers the PartyWatch app using FastAPI (Python), MongoDB (persistent storage), and Redis (real-time pub/sub, presence, cache).

## Structure

```
backend/
├── app/
│   ├── main.py             # FastAPI entrypoint
│   ├── api/                # API route modules
│   ├── models/             # Pydantic models
│   ├── db/                 # Database logic (MongoDB, Redis)
│   ├── services/           # Business logic
│   └── utils.py
├── requirements.txt
└── README.md
```

## Features
- REST API for rooms, users, chat, queue, polls
- WebSocket for real-time chat, presence, queue sync
- MongoDB for persistent storage
- Redis for pub/sub and fast presence

## Quickstart

1. Install Docker and Docker Compose
2. Run: `docker-compose up --build`
3. FastAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Environment Variables
- `MONGO_URI` (e.g. mongodb://mongo:27017)
- `REDIS_URL` (e.g. redis://redis:6379)
- `SECRET_KEY` (for JWT, optional)

## Connect Frontend
- Use REST endpoints for room, chat, queue, etc.
- Use WebSocket endpoint for real-time features

---
See each module for more details. 