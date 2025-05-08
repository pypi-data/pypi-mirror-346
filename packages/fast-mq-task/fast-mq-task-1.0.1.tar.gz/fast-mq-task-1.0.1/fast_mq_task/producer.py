# -*- coding: utf-8 -*-
import time
from aio_pika import Message, DeliveryMode
from .client import RabbitMQClient
from .models import TaskMessage


# --------------------------
# 生产者模块 (producer.py)
# --------------------------
class TaskProducer(RabbitMQClient):
    async def publish_task(self, task: TaskMessage):
        # 确保队列定义
        _, exchange = await self.ensure_declare(task_type=task.task_type)

        message = Message(
            body=task.json().encode(),
            content_type="application/json",
            headers={
                "x-task-type": task.task_type,
                "x-created-at": time.time()
            },
            delivery_mode=DeliveryMode.PERSISTENT  # 添加消息持久化
        )
        await exchange.publish(
            message=message,
            routing_key=task.get_routing_key()
        )
