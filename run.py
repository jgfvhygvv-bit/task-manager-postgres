# run.py
#!/usr/bin/env python
"""Точка входа для запуска приложения"""
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.app import app

    print("=" * 60)
    print("🚀 Task Manager with PostgreSQL")
    print("=" * 60)
    print("📊 База данных: PostgreSQL")
    print("🌐 Веб-интерфейс: http://localhost:5000")
    print("📡 API Health: http://localhost:5000/api/health")
    print("📡 API Tasks: http://localhost:5000/api/tasks")
    print("=" * 60)
    print("💾 Данные хранятся в PostgreSQL:")
    print(f"   База: {app.config.get('POSTGRES_DB', 'taskmanager')}")
    print(f"   Хост: {app.config.get('POSTGRES_HOST', 'localhost')}")
    print(f"   Порт: {app.config.get('POSTGRES_PORT', '5432')}")
    print("=" * 60)

    app.run(debug=True, host="0.0.0.0", port=5000)

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nСтруктура проекта должна быть:")
    print("task_manager_postgres/")
    print("├── app/")
    print("│   ├── templates/")
    print("│   ├── __init__.py")
    print("│   ├── app.py")
    print("│   ├── models.py")
    print("│   └── config.py")
    print("├── tests/")
    print("├── requirements.txt")
    print("└── run.py")
    sys.exit(1)
