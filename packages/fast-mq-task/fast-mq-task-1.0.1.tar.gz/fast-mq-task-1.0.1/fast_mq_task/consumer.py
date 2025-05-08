# -*- coding: utf-8 -*-
import asyncio
import inspect
import logging
import traceback
from functools import partial
from typing import Callable, Dict
from aio_pika import IncomingMessage
from .client import RabbitMQClient
from .decorators import TaskRegistry
from .models import TaskMessage, RabbitMeta
from concurrent.futures import ThreadPoolExecutor


# --------------------------
# 消费者模块 (consumer.py)
# --------------------------
class TaskConsumer(RabbitMQClient):
    def __init__(
            self,
            amqp_url: str,
            task_config: Dict[str, Dict] = None,  # 新增任务专属配置
            default_prefetch: int = 10
    ):
        super().__init__(amqp_url)
        self.task_config = task_config or {}
        self.default_prefetch = default_prefetch
        self._running = False
        self._executors: Dict[str, ThreadPoolExecutor] = {}  # 任务专属线程池
        self._semaphores: Dict[str, asyncio.Semaphore] = {}  # 异步信号量控制

    async def _init_resources(self):
        """初始化每个任务的执行资源"""
        for idx, task_type in enumerate(TaskRegistry._handlers):
            # 创建独立线程池
            config = self.task_config.get(task_type, {})
            max_workers = config.get('max_workers', 4)
            self._executors[task_type] = ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix=f"Worker-{task_type}-"
            )

            # 创建异步信号量
            prefetch = config.get('prefetch', self.default_prefetch)
            self._semaphores[task_type] = asyncio.Semaphore(prefetch)
            logging.info(f'消费者初始化[{idx}]: task_type={task_type}, prefetch={prefetch}, max_workers={max_workers}')

    async def _process_message(self, rabbit_meta: RabbitMeta, msg: IncomingMessage):
        """处理消息的优化版本"""
        async with msg.process():
            try:
                handler: Callable = rabbit_meta.handler_func
                # 获取任务配置
                task_type = rabbit_meta.task_type
                semaphore = self._semaphores[task_type]
                executor = self._executors[task_type]

                # 使用专属信号量控制并发
                async with semaphore:
                    task = TaskMessage.parse_raw(msg.body)

                    if inspect.iscoroutinefunction(handler):
                        # 异步任务直接await
                        await handler(task)
                    else:
                        # 同步任务放入专属线程池
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(
                            executor,
                            partial(handler, task)
                        )
            except Exception as e:
                logging.error(f"处理失败: {traceback.format_exc()}")

    async def _setup_queues(self):
        """队列初始化优化"""
        for rabbit_meta in TaskRegistry._handlers.values():
            queue, _ = await self.ensure_declare(task_type=rabbit_meta.task_type, prefetch=rabbit_meta.prefetch or self.default_prefetch)

            # 为每个队列创建独立消费者
            await queue.consume(
                partial(self._process_message, rabbit_meta)
            )

    async def start(self):
        """启动消费者"""
        await self._init_resources()
        await self._setup_queues()
        self._running = True
        while self._running:
            await asyncio.sleep(1)

    async def stop(self):
        """优雅关闭"""
        self._running = False
        for executor in self._executors.values():
            executor.shutdown(wait=True)
        await super().close()
