# LMS FastAPI OOP
An OOP-structured Learning Management System API using FastAPI + MySQL (SQLAlchemy).

## Run
1) Create DB:
   CREATE DATABASE lmsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
2) Copy env:
   copy .env.example .env  (Windows)  |  cp .env.example .env (Linux/Mac)
3) Install:
   pip install -r requirements.txt
4) Start:
   uvicorn app.main:app --reload --port 8090
5) Docs:
   http://127.0.0.1:8090/docs
