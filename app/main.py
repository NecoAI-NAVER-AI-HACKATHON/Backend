# app/main.py
from __future__ import annotations

import logging
from fastapi import FastAPI
from app.application import Application


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


app: FastAPI = Application().create_app()
