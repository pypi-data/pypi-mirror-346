from enum import Enum
from typing import Any, Callable, Mapping, Self, Sequence

class Route:
    source: str
    waypoints: Sequence[str]

    def __init__(self, source: str, waypoints: Sequence[str]) -> None: ...

class InitialOffset(Enum):
    earliest = "earliest"
    latest = "latest"
    error = "error"

class OffsetResetConfig:
    auto_offset_reset: InitialOffset
    strict_offset_reset: bool

    def __init__(self, auto_offset_reset: InitialOffset, strict_offset_reset: bool) -> None: ...

class PyKafkaConsumerConfig:
    def __init__(
        self,
        bootstrap_servers: Sequence[str],
        group_id: str,
        auto_offset_reset: InitialOffset,
        strict_offset_reset: bool,
        max_poll_interval_ms: int,
        override_params: Mapping[str, str],
    ) -> None: ...

class PyKafkaProducerConfig:
    def __init__(
        self,
        bootstrap_servers: Sequence[str],
        override_params: Mapping[str, str],
    ) -> None: ...

class RuntimeOperator:
    @classmethod
    def Map(cls, route: Route, function: Callable[[Any], Any]) -> Self: ...
    @classmethod
    def StreamSink(
        cls, route: Route, topic_name: str, kafka_config: PyKafkaProducerConfig
    ) -> Self: ...

class ArroyoConsumer:
    def __init__(self, source: str, kafka_config: PyKafkaConsumerConfig, topic: str) -> None: ...
    def add_step(self, step: RuntimeOperator) -> None: ...
    def run(self) -> None: ...
    def shutdown(self) -> None: ...
