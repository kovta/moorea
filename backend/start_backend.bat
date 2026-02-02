@echo off
cd /d d:\dev\match\moorea\backend
python -m uvicorn app.main:app --port 8000
