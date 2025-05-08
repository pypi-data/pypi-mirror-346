# -*- coding: utf-8 -*-
import logging
from typing import Callable, Dict
from .models import RabbitMeta


# --------------------------
# 装饰器模块 (decorators.py)
# --------------------------
class TaskRegistry:
    _handlers: Dict[str, RabbitMeta] = {}

    @classmethod
    def register(cls, task_type: str) -> Callable:
        # 新增参数校验
        if not task_type:
            raise ValueError("`task_type`不能全部为空")

        def decorator(func: Callable) -> Callable:
            meta = RabbitMeta(
                task_type=task_type,
                handler_func=func
            )
            cls._handlers[task_type] = meta
            logging.info(f"处理器注册: task_type={task_type}, exchange={meta.queue_key}, func={func}")

            return func

        return decorator


task_handler = TaskRegistry.register
