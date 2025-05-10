import asyncio
from typing import List, Optional, Callable, Any, Dict
from dataclasses import dataclass
from .exceptions import TaskError, TaskTimeoutError

@dataclass
class Task:
    """非同期タスクを表すクラス"""
    name: str
    func: Callable[..., Any]
    priority: int = 0
    timeout: Optional[float] = None
    args: tuple = ()
    kwargs: Dict[str, Any] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}

class TaskManager:
    """非同期タスクを管理するクラス"""
    
    def __init__(self, max_concurrent_tasks: int = 10):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self._tasks: List[Task] = []
        self._results: Dict[str, Any] = {}
        self._errors: Dict[str, Exception] = {}

    async def add_task(self, task: Task) -> None:
        """タスクを追加する"""
        self._tasks.append(task)
        self._tasks.sort(key=lambda x: x.priority, reverse=True)

    async def run_task(self, task: Task) -> Any:
        """単一のタスクを実行する"""
        try:
            async with self.semaphore:
                if task.timeout:
                    result = await asyncio.wait_for(
                        task.func(*task.args, **task.kwargs),
                        timeout=task.timeout
                    )
                else:
                    result = await task.func(*task.args, **task.kwargs)
                self._results[task.name] = result
                return result
        except asyncio.TimeoutError:
            error = TaskTimeoutError(f"Task {task.name} timed out after {task.timeout} seconds")
            self._errors[task.name] = error
            raise error
        except Exception as e:
            self._errors[task.name] = e
            raise TaskError(f"Error in task {task.name}: {str(e)}") from e

    async def run_tasks(self, tasks: Optional[List[Task]] = None) -> Dict[str, Any]:
        """複数のタスクを実行する"""
        if tasks:
            self._tasks = tasks
            self._tasks.sort(key=lambda x: x.priority, reverse=True)

        if not self._tasks:
            return {}

        # すべてのタスクを並行して実行
        await asyncio.gather(
            *(self.run_task(task) for task in self._tasks),
            return_exceptions=True
        )

        return self._results

    def get_results(self) -> Dict[str, Any]:
        """タスクの実行結果を取得する"""
        return self._results

    def get_errors(self) -> Dict[str, Exception]:
        """タスクの実行エラーを取得する"""
        return self._errors

    def clear(self) -> None:
        """タスク管理の状態をクリアする"""
        self._tasks.clear()
        self._results.clear()
        self._errors.clear() 