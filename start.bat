@echo off
cd Backend
call venv\Scripts\activate
uvicorn main:app --reload
pause