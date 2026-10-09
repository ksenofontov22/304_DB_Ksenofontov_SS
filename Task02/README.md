# Task02 - ETL для SQLite

## Требования к окружению

- **Python 3** (проверка: `python3 --version`)
- **SQLite** - консольный клиент `sqlite3` в `PATH` (проверка: `sqlite3 --version`)
- **Bash** (Linux/macOS/Git Bash) для запуска `db_init.bat`

## Структура

| Файл | Назначение |
|------|-----------|
| `db_init.bat` | Скрипт генерирует db_init.sql и создаёт заполненную базу movies_rating.db. |
| `make_db_init.py` | генератор SQL-скрипта |
| `db_init.sql` | результат работы генератора |
| `movies_rating.db` | итоговая база SQLite |
| `movies.csv`, `ratings.csv`, `tags.csv`, `users.txt` | исходные данные |

## Запуск

```bash
bash db_init.bat
