from enum import Enum


class GetV1DesktopIdResponse429Status(str, Enum):
    ERROR = "error"

    def __str__(self) -> str:
        return str(self.value)
