# Анализатор журналов событий

## Бизнес-требования
Службе поддержки нужен CLI-инструмент для поиска частых ошибок в логах нескольких компонентов. Файл может быть большим — чтение построчно, без загрузки в память.

## Формат строки
timestamp | level | source | eventCode | message

- timestamp — ISO 8601 UTC
- level: TRACE, DEBUG, INFO, WARN, ERROR
- символ | внутри полей запрещён

## Реализованный функционал
- Фильтрация по интервалу времени (from — включительно, to — исключительно), уровню и источнику.
- Подсчёт корректных и ошибочных строк, событий после фильтрации.
- Сводка по уровням и источникам, top-N кодов ошибок.
- Вывод в терминал + сохранение отчёта в JSON или CSV.
- Обработка пустого и отсутствующего файла.
- Для ошибочной строки отображается её номер.

## Архитектура
- src/parser.py — разбор строки
- src/filters.py — фильтрация
- src/aggregator.py — агрегация
- src/writer.py — вывод (terminal / json / csv)
- src/cli.py — CLI-интерфейс

## CLI-параметры
- --input (обязательный) — путь к файлу лога
- --from — начало интервала (ISO 8601, включительно)
- --to — конец интервала (ISO 8601, исключительно)
- --level — уровень: TRACE/DEBUG/INFO/WARN/ERROR
- --source — источник события
- --top — количество кодов ошибок в топе (по умолчанию 5)
- --format — формат отчёта: json или csv (по умолчанию json)
- --output — путь к файлу отчёта

## Примеры запуска

1. Все ошибки за 1 сентября:
python -m src.cli --input logs_events_sample.log --level ERROR --from 2026-09-01T00:00:00Z --to 2026-09-02T00:00:00Z --output report.json

2. Top-10 ошибок шлюза в CSV:
python -m src.cli --input logs_events_sample.log --source gateway --level ERROR --top 10 --output report.csv --format csv

3. Только payment-worker:
python -m src.cli --input logs_events_sample.log --source payment-worker

## Развёртывание (WSL)
sudo apt update && sudo apt install python3 python3-pip python3-venv -y
cd log_analyzer
chmod +x run_tests.sh
./run_tests.sh

## Зависимости
pytest>=8.0
pytest-cov>=5.0

## Тестирование
Запуск тестов и формирование HTML-отчёта одной командой:
./run_tests.sh

## Метрика покрытия
- Целевое покрытие: 80%
- Фактическое покрытие: 97%
- Исключения: src/__init__.py, src/__main__.py

## Путь к HTML-отчёту
./htmlcov/index.html

## Пример отчёта
Файл report.json содержит: matched, by_level, by_source, top_errors, valid, invalid, errors.
