class BaseCommand:
    def __init__(self, db_context: str) -> None:
        self._db_context = db_context

    async def execute(self) -> int:
        raise NotImplementedError


class ChildCommand(BaseCommand):
    async def execute(self) -> int:
        return 2


class ChildCommand2(BaseCommand):
    async def execute(self) -> int:
        return 3


class Command2:
    def __init__(self, db_context: str) -> None:
        self._nani_ctx = db_context

    async def execute(self) -> int:
        return 3
