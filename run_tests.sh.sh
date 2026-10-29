#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
pytest --cov=src --cov-report=html:htmlcov --cov-report=term-missing tests/
echo "HTML-отчёт: $(pwd)/htmlcov/index.html"