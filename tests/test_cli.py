import pytest
import sys
from pathlib import Path
from src.cli import main


def test_cli_no_input(capsys):
    """Тест: отсутствует параметр input"""
    with pytest.raises(SystemExit):
        main([])


def test_cli_file_not_found(capsys):
    """Тест: файл не найден"""
    result = main(["--input", "/nonexistent/file.log"])
    assert result == 1
    captured = capsys.readouterr()
    assert "не найден" in captured.err or "not found" in captured.err


def test_cli_empty_file(tmp_path, capsys):
    """Тест: пустой файл"""
    empty_file = tmp_path / "empty.log"
    empty_file.write_text("")
    result = main(["--input", str(empty_file)])
    assert result == 0


def test_cli_basic_run(tmp_path, capsys):
    """Тест: базовый запуск"""
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created\n"
        "2026-09-01T00:20:18Z | ERROR | payment-worker | PAYMENT_TIMEOUT | Payment provider timed out\n"
    )
    result = main(["--input", str(log_file)])
    assert result == 0
    captured = capsys.readouterr()
    assert "Корректных строк" in captured.out or "Valid lines" in captured.out


def test_cli_with_filters(tmp_path, capsys):
    """Тест: фильтрация по уровню и источнику"""
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created\n"
        "2026-09-01T00:20:18Z | ERROR | payment-worker | PAYMENT_TIMEOUT | Payment provider timed out\n"
        "2026-09-01T00:47:04Z | ERROR | auth-api | AUTH_TOKEN_EXPIRED | Access token expired\n"
    )
    result = main([
        "--input", str(log_file),
        "--level", "ERROR",
        "--source", "payment-worker"
    ])
    assert result == 0
    captured = capsys.readouterr()
    assert "Matched events: 1" in captured.out or "Событий после фильтра: 1" in captured.out


def test_cli_with_time_filter(tmp_path, capsys):
    """Тест: фильтрация по времени"""
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created\n"
        "2026-09-02T00:20:18Z | ERROR | payment-worker | PAYMENT_TIMEOUT | Payment provider timed out\n"
    )
    result = main([
        "--input", str(log_file),
        "--from", "2026-09-02T00:00:00Z",
        "--to", "2026-09-03T00:00:00Z"
    ])
    assert result == 0
    captured = capsys.readouterr()
    assert "Matched events: 1" in captured.out or "Событий после фильтра: 1" in captured.out


def test_cli_output_json(tmp_path, capsys):
    """Тест: вывод в JSON"""
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created\n"
    )
    output_file = tmp_path / "report.json"
    result = main([
        "--input", str(log_file),
        "--output", str(output_file),
        "--format", "json"
    ])
    assert result == 0
    assert output_file.exists()


def test_cli_output_csv(tmp_path, capsys):
    """Тест: вывод в CSV"""
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created\n"
    )
    output_file = tmp_path / "report.csv"
    result = main([
        "--input", str(log_file),
        "--output", str(output_file),
        "--format", "csv"
    ])
    assert result == 0
    assert output_file.exists()


def test_cli_invalid_lines(tmp_path, capsys):
    """Тест: обработка ошибочных строк"""
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created\n"
        "invalid line\n"
        "2026-09-01T00:20:18Z | ERROR | payment-worker | PAYMENT_TIMEOUT | Payment provider timed out\n"
    )
    result = main(["--input", str(log_file)])
    assert result == 0
    captured = capsys.readouterr()
    assert "Ошибочных строк" in captured.out or "Invalid lines" in captured.out