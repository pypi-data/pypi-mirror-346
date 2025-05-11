class BaseCommand:
    def __init__(self, db_context: str) -> None:
        self._db_context = db_context

    async def execute(self) -> int:
        raise NotImplementedError


class ChildCommand(BaseCommand):
    async def execute(self) -> int:
        return 2

