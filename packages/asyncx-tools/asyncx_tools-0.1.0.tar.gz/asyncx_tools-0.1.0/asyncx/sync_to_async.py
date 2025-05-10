import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Optional, TypeVar, cast

T = TypeVar('T')

def sync_to_async(
    func: Callable[..., T],
    thread_sensitive: bool = True,
    executor: Optional[ThreadPoolExecutor] = None
) -> Callable[..., Any]:
    """
    同期関数を非同期関数に変換するデコレータ

    Args:
        func: 変換対象の同期関数
        thread_sensitive: スレッドセーフティを考慮するかどうか
        executor: 使用するThreadPoolExecutor（指定しない場合は新規作成）

    Returns:
        非同期関数
    """
    if asyncio.iscoroutinefunction(func):
        return func

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        if thread_sensitive:
            # スレッドセーフティを考慮する場合
            loop = asyncio.get_running_loop()
            current_executor = executor or ThreadPoolExecutor()
            try:
                return await loop.run_in_executor(
                    current_executor,
                    functools.partial(func, *args, **kwargs)
                )
            finally:
                if executor is None:
                    current_executor.shutdown(wait=False)
        else:
            # スレッドセーフティを考慮しない場合
            return await asyncio.to_thread(func, *args, **kwargs)

    return cast(Callable[..., Any], wrapper)

def async_to_sync(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    非同期関数を同期関数に変換するデコレータ

    Args:
        func: 変換対象の非同期関数

    Returns:
        同期関数
    """
    if not asyncio.iscoroutinefunction(func):
        return func

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            # 既存のイベントループが動作中の場合
            import concurrent.futures
            fut = asyncio.run_coroutine_threadsafe(func(*args, **kwargs), loop)
            return fut.result()
        else:
            # 新しいイベントループを作成
            return asyncio.run(func(*args, **kwargs))
    return wrapper 