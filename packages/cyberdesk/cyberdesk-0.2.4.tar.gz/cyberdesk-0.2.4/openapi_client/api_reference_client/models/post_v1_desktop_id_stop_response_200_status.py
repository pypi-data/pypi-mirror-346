from enum import Enum


class PostV1DesktopIdStopResponse200Status(str, Enum):
    ERROR = "error"
    PENDING = "pending"
    RUNNING = "running"
    TERMINATED = "terminated"

    def __str__(self) -> str:
        return str(self.value)
