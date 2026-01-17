# tests/test_app.py
import sys
import os
import pytest
import json

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Task
from app.config import TestingConfig


@pytest.fixture
def app():
    """Создание тестового приложения с тестовой конфигурацией"""
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()


@pytest.fixture
def init_database(app):
    """Инициализация тестовой базы данных"""
    with app.app_context():
        # Добавляем тестовые задачи
        tasks = [
            Task(title="Test Task 1", description="Description 1"),
            Task(title="Test Task 2", description="Description 2", status="completed"),
        ]

        for task in tasks:
            db.session.add(task)

        db.session.commit()

        yield db


def decode_response(response):
    """Декодируем response.data в строку"""
    if hasattr(response, "data") and response.data:
        try:
            return response.data.decode("utf-8", errors="ignore")
        except:
            return str(response.data)
    return ""


def test_index_page(client):
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    content = decode_response(response)
    assert "Task Manager" in content


def test_health_api(client):
    """Тест API здоровья"""
    response = client.get("/api/health")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "database" in data


def test_tasks_page(client, init_database):
    """Тест страницы задач"""
    response = client.get("/tasks")
    assert response.status_code == 200

    content = decode_response(response)
    assert "задачи" in content.lower() or "tasks" in content.lower()


def test_create_task_page(client):
    """Тест страницы создания задачи"""
    response = client.get("/tasks/create")
    assert response.status_code == 200

    content = decode_response(response)
    assert "создать" in content.lower() or "create" in content.lower()


def test_api_get_tasks(client, init_database):
    """Тест API получения задач"""
    response = client.get("/api/tasks")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2


def test_api_create_task(client):
    """Тест API создания задачи"""
    new_task = {"title": "API Test Task", "description": "Test Description"}

    response = client.post("/api/tasks", json=new_task, content_type="application/json")

    assert response.status_code == 201

    data = json.loads(response.data)
    assert data["title"] == new_task["title"]
    assert "id" in data


def test_api_delete_task(client, init_database):
    """Тест API удаления задачи"""
    # Создаем задачу для удаления
    new_task = {"title": "Task to delete"}
    create_response = client.post("/api/tasks", json=new_task)
    task_id = json.loads(create_response.data)["id"]

    # Удаляем задачу
    delete_response = client.delete(f"/api/tasks/{task_id}")
    assert delete_response.status_code == 200

    # Проверяем что задача удалена
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_api_get_nonexistent_task(client):
    """Тест получения несуществующей задачи"""
    response = client.get("/api/tasks/9999")
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "error" in data


def test_task_model():
    """Тест модели задачи"""
    task = Task(title="Model Test", description="Test Description", status="pending")

    assert task.title == "Model Test"
    assert task.status == "pending"
    assert task.description == "Test Description"
    assert task.id is None

    # Проверяем метод to_dict
    task_dict = task.to_dict()
    assert "title" in task_dict
    assert "status" in task_dict
    assert "created_at" in task_dict


def test_create_task_via_form(client):
    """Тест создания задачи через форму"""
    response = client.post(
        "/tasks/create",
        data={"title": "Test Task via Form", "description": "Test Description"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    content = decode_response(response).lower()
    assert "задача" in content or "task" in content


def test_delete_task_via_form(client, init_database):
    """Тест удаления задачи через форму"""
    # Сначала создаем задачу через API
    new_task = {"title": "Task to delete via form"}
    create_response = client.post("/api/tasks", json=new_task)
    task_id = json.loads(create_response.data)["id"]

    # Удаляем через форму
    response = client.post(f"/tasks/{task_id}/delete", follow_redirects=True)
    assert response.status_code == 200

    # Проверяем что задача удалена
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_toggle_task_status(client, init_database):
    """Тест переключения статуса задачи"""
    # Получаем первую задачу
    response = client.get("/api/tasks")
    tasks = json.loads(response.data)
    task_id = tasks[0]["id"]

    # Переключаем статус через форму
    response = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert response.status_code == 200

    # Проверяем что статус изменился
    get_response = client.get(f"/api/tasks/{task_id}")
    task = json.loads(get_response.data)
    assert task["status"] in ["pending", "completed"]


if __name__ == "__main__":
    pytest.main(["-v", __file__])
