import pytest
import asyncio
from asyncx import TaskManager, Task, TaskError, TaskTimeoutError

async def sample_task(delay: float, result: str = "success"):
    await asyncio.sleep(delay)
    return result

async def failing_task():
    await asyncio.sleep(0.1)
    raise ValueError("Task failed")

@pytest.mark.asyncio
async def test_basic_task_execution():
    manager = TaskManager()
    task = Task("test_task", sample_task, args=(0.1,))
    result = await manager.run_task(task)
    assert result == "success"

@pytest.mark.asyncio
async def test_multiple_tasks():
    manager = TaskManager()
    tasks = [
        Task("task1", sample_task, args=(0.1,), priority=1),
        Task("task2", sample_task, args=(0.2,), priority=2),
    ]
    results = await manager.run_tasks(tasks)
    assert len(results) == 2
    assert results["task1"] == "success"
    assert results["task2"] == "success"

@pytest.mark.asyncio
async def test_task_timeout():
    manager = TaskManager()
    task = Task("timeout_task", sample_task, args=(2.0,), timeout=0.1)
    with pytest.raises(TaskTimeoutError):
        await manager.run_task(task)

@pytest.mark.asyncio
async def test_task_error_handling():
    manager = TaskManager()
    task = Task("error_task", failing_task)
    with pytest.raises(TaskError):
        await manager.run_task(task)
    assert "error_task" in manager.get_errors() 