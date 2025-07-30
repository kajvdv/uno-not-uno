import sys

import logging

import uvicorn

logger = logging.basicConfig(level=logging.DEBUG)

uvicorn.run("app.main:app")