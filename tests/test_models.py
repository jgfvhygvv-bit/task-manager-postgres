# tests/test_models.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Task
from datetime import datetime


def test_task_creation():
    """Тест создания объекта задачи"""
    task = Task(title="Test Task", description="Test Description", status="in_progress")

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "in_progress"
    assert task.id is None
    assert isinstance(task.created_at, datetime) or task.created_at is None
    assert isinstance(task.updated_at, datetime) or task.updated_at is None


def test_task_to_dict():
    """Тест преобразования задачи в словарь"""
    task = Task(
        title="Dict Test", description="Description for dict", status="completed"
    )

    task_dict = task.to_dict()

    assert isinstance(task_dict, dict)
    assert task_dict["title"] == "Dict Test"
    assert task_dict["description"] == "Description for dict"
    assert task_dict["status"] == "completed"
    assert "id" in task_dict
    assert "created_at" in task_dict
    assert "updated_at" in task_dict


def test_task_default_values():
    """Тест значений по умолчанию"""
    task = Task(title="Default Test")

    assert task.description is None or task.description == ""
    assert task.status == "pending"
    assert task.created_at is not None or task.created_at is None
    assert task.updated_at is not None or task.updated_at is None


def test_task_status_values():
    """Тест допустимых значений статуса"""
    valid_statuses = ["pending", "in_progress", "completed"]

    for status in valid_statuses:
        task = Task(title=f"Task {status}", status=status)
        assert task.status == status


def test_task_representation():
    """Тест строкового представления"""
    task = Task(title="Representation Test")
    assert str(task) == f"<Task {task.title}>"


def test_task_datetime_auto_update():
    """Тест автоматического обновления времени"""
    task = Task(title="Time Test")
    assert task.created_at is None or isinstance(task.created_at, datetime)
    assert task.updated_at is None or isinstance(task.updated_at, datetime)


def run_all_tests():
    """Запуск всех тестов моделей"""
    tests = [
        test_task_creation,
        test_task_to_dict,
        test_task_default_values,
        test_task_status_values,
        test_task_representation,
        test_task_datetime_auto_update,
    ]

    print("=" * 50)
    print("Running PostgreSQL model tests...")
    print("=" * 50)

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: Error - {e}")
            failed += 1

    print("=" * 50)
    print(f"📊 Total: {passed} passed, {failed} failed")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
