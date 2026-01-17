# app/app.py
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import os
from datetime import datetime
from . import create_app, db
from .models import Task

app = create_app()

# ==================== ВЕБ-ИНТЕРФЕЙС ====================


@app.route("/")
def index():
    """Главная страница"""
    return render_template("index.html")


@app.route("/tasks")
def tasks_page():
    """Страница со списком задач"""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("tasks.html", tasks=tasks)


@app.route("/tasks/create", methods=["GET", "POST"])
def create_task():
    """Создание новой задачи"""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if title:
            task = Task(title=title, description=description)
            db.session.add(task)
            db.session.commit()
            flash("✅ Задача успешно создана!", "success")
            return redirect(url_for("tasks_page"))
        else:
            flash("❌ Название задачи обязательно!", "error")

    return render_template("create_task.html")


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    """Удаление задачи"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("✅ Задача успешно удалена!", "success")
    return redirect(url_for("tasks_page"))


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    """Переключение статуса задачи"""
    task = Task.query.get_or_404(task_id)

    if task.status == "pending":
        task.status = "completed"
    else:
        task.status = "pending"

    db.session.commit()
    flash("✅ Статус задачи обновлен!", "success")
    return redirect(url_for("tasks_page"))


# ==================== API ====================


@app.route("/api/health")
def api_health():
    """API для проверки здоровья приложения"""
    try:
        # Проверяем подключение к PostgreSQL
        db.session.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify(
        {
            "status": "healthy",
            "service": "Task Manager with PostgreSQL",
            "database": db_status,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    """API: Получить все задачи"""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def api_get_task(task_id):
    """API: Получить задачу по ID"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())


@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    """API: Создать новую задачу"""
    data = request.json

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        status=data.get("status", "pending"),
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    """API: Удалить задачу"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"})


# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================


def init_database():
    """Инициализация базы данных с тестовыми данными"""
    with app.app_context():
        # Добавляем тестовые данные если таблица пустая
        if Task.query.count() == 0:
            test_tasks = [
                Task(
                    title="Изучить Flask",
                    description="Изучить основы Flask",
                    status="in_progress",
                ),
                Task(
                    title="Настроить PostgreSQL",
                    description="Настроить базу данных",
                    status="pending",
                ),
                Task(
                    title="Написать тесты",
                    description="Создать unit-тесты",
                    status="pending",
                ),
            ]

            for task in test_tasks:
                db.session.add(task)

            db.session.commit()
            print(f"✅ Добавлено {len(test_tasks)} тестовых задач")


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Task Manager with PostgreSQL")
    print("=" * 60)
    print(f"📊 База данных: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("🌐 Веб-интерфейс: http://localhost:5000")
    print("📡 API Health: http://localhost:5000/api/health")
    print("=" * 60)

    # Инициализируем базу данных
    init_database()

    app.run(debug=True, host="0.0.0.0", port=5000)
