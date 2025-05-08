import asyncio
import hashlib
import inspect
import json
import os
from functools import wraps
from typing import Any, Callable, List, Optional, Union

import diskcache as dc


class DCache:
    def __init__(self, n_semaphore: int = 100, cache_dir: Optional[str] = None):
        """
        Create a DCache instance.

        Parameters:
            n_semaphore (int): Maximum number of parallel cache accesses.
            cache_dir (str): Path to the cache directory. Defaults to a ".dcache"
                             directory in the current working directory.
        """
        if cache_dir is None:
            cache_dir = os.path.join(os.getcwd(), ".dcache")
        os.makedirs(cache_dir, exist_ok=True)
        self.cache = dc.FanoutCache(cache_dir, shards=64, timeout=10)
        self.semaphore = asyncio.Semaphore(n_semaphore)

    def __call__(self, possible_func=None, *, required_kwargs=None):
        """
        When used as a decorator, DCache works in two ways:

          1. As a no-argument decorator:
                @dcache
                def my_func(...): ...

          2. As a parameterized decorator:
                @dcache(required_kwargs=["foo"])
                def my_func(...): ...

        The `required_kwargs` parameter (a list) determines which keyword
        arguments are needed for caching. If they are not present, the function
        is simply executed.

        Works with both synchronous and asynchronous functions.
        """
        if possible_func is not None and callable(possible_func):
            # Used as "@dcache" without explicit parameters.
            return self._make_decorator(required_kwargs or [])(possible_func)
        else:
            # Used as "@dcache(required_kwargs=[...])". Return a decorator.
            required_kwargs = required_kwargs or []
            def decorator(func):
                return self._make_decorator(required_kwargs)(func)
            return decorator

    def _make_decorator(self, required_kwargs: List[str]):
        def decorator(function: Callable) -> Callable:
            is_async = inspect.iscoroutinefunction(function)

            if is_async:
                @wraps(function)
                async def async_wrapper(*args, **kwargs):
                    # Only attempt caching if all required keyword arguments are present.
                    if required_kwargs and not all(k in kwargs for k in required_kwargs):
                        return await function(*args, **kwargs)

                    # Serialize args/kwargs and compute the cache key.
                    serialized = json.dumps({"args": self._serialize_args(args), 
                                            "kwargs": self._serialize_kwargs(kwargs)}, 
                                            sort_keys=True)
                    key = hashlib.sha256(serialized.encode()).hexdigest()

                    # Limit the number of concurrent cache accesses.
                    async with self.semaphore:
                        cached_result = await asyncio.to_thread(self.cache.get, key, None)
                    if cached_result is not None:
                        return cached_result

                    result = await function(*args, **kwargs)

                    async with self.semaphore:
                        await asyncio.to_thread(self.cache.set, key, result)
                    return result
                
                return async_wrapper
            else:
                @wraps(function)
                def sync_wrapper(*args, **kwargs):
                    # Only attempt caching if all required keyword arguments are present.
                    if required_kwargs and not all(k in kwargs for k in required_kwargs):
                        return function(*args, **kwargs)

                    # Serialize args/kwargs and compute the cache key.
                    serialized = json.dumps({"args": self._serialize_args(args), 
                                            "kwargs": self._serialize_kwargs(kwargs)}, 
                                            sort_keys=True)
                    key = hashlib.sha256(serialized.encode()).hexdigest()

                    # Check cache
                    cached_result = self.cache.get(key, None)
                    if cached_result is not None:
                        return cached_result

                    result = function(*args, **kwargs)
                    self.cache.set(key, result)
                    return result
                
                return sync_wrapper
            
        return decorator
    
    def _serialize_args(self, args):
        """
        Serialize function arguments for JSON encoding.
        Handles non-serializable objects by converting them to strings.
        """
        serialized_args = []
        for arg in args:
            try:
                # Test if the argument is JSON serializable
                json.dumps(arg)
                serialized_args.append(arg)
            except (TypeError, OverflowError):
                # If not serializable, convert to string representation
                serialized_args.append(str(arg))
        return serialized_args
    
    def _serialize_kwargs(self, kwargs):
        """
        Serialize function keyword arguments for JSON encoding.
        Handles non-serializable objects by converting them to strings.
        """
        serialized_kwargs = {}
        for key, value in kwargs.items():
            try:
                # Test if the value is JSON serializable
                json.dumps(value)
                serialized_kwargs[key] = value
            except (TypeError, OverflowError):
                # If not serializable, convert to string representation
                serialized_kwargs[key] = str(value)
        return serialized_kwargs


# Create a default object for easy importing.
dcache = DCache()