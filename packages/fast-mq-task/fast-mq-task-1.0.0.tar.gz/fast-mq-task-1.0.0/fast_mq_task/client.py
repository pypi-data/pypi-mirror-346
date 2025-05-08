# -*- coding: utf-8 -*-
import logging
from typing import Dict, Union
from aio_pika import connect, Exchange, ExchangeType, Channel, Queue
from aio_pika.abc import AbstractExchange, AbstractQueue

from .keys import get_default_exchange_name, get_default_routing_key, get_default_queue_name


# --------------------------
# 客户端基础模块 (client.py)
# --------------------------
class RabbitMQClient:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channels: Dict[str, Channel] = {}
        self.exchanges: Dict[str, Union[Exchange, AbstractExchange]] = {}
        self.queues: Dict[str, Union[Queue, AbstractQueue]] = {}

    async def connect(self):
        self.connection = await connect(self.amqp_url)
        return self

    async def close(self):
        for channel in self.channels.values():
            await channel.close()
        await self.connection.close()

    async def get_channel(self, task_type: str, prefetch: int = 4) -> Channel:
        task_type = task_type or 'default'
        if task_type not in self.channels:
            channel = await self.connection.channel()
            await channel.set_qos(
                prefetch_count=prefetch
            )
            logging.info(f"信道定义: task_type={task_type}, prefetch={prefetch}")
            self.channels[task_type] = channel

        return self.channels[task_type]

    async def get_exchange(self, channel: Channel, exchange_name: str = None, exchange_type: str = "topic") -> Exchange:
        # 统一交换器类型为小写
        exchange_type = exchange_type.lower()

        # 添加交换器类型校验
        if exchange_type not in ["direct", "topic", "fanout", "headers"]:
            raise ValueError(f"Invalid exchange type: {exchange_type}")
        if not exchange_name:
            exchange_name = get_default_exchange_name()

        if exchange_name not in self.exchanges:
            self.exchanges[exchange_name] = await channel.declare_exchange(
                name=exchange_name,
                type=exchange_type,
                durable=True,  # 持久化交换器
                auto_delete=False,
                arguments={
                    "x-queue-type": "quorum"  # 使用高可用队列类型
                }
            )
            logging.info(f"交换机定义: exchange={exchange_name}, type={exchange_type}")

        return self.exchanges[exchange_name]

    async def ensure_declare(self, task_type: str, prefetch: int = 10):
        # 创建专属channel避免相互影响
        channel = await self.get_channel(task_type, prefetch)

        exchange_key = get_default_exchange_name()
        exchange_type = ExchangeType.TOPIC
        routing_key = get_default_routing_key(task_type)
        queue_key = get_default_queue_name(task_type)

        # 声明交换器和队列
        exchange = await self.get_exchange(channel=channel, exchange_name=exchange_key, exchange_type=exchange_type)
        if queue_key not in self.queues:
            queue = await channel.declare_queue(
                name=queue_key,
                durable=True,
                arguments={
                    'x-max-priority': 10  # 支持优先级队列
                }
            )
            await queue.bind(exchange, routing_key)
            self.queues[queue_key] = queue

        return self.queues[queue_key], exchange
