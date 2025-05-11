from .example import BaseCommand


class ChildCommand2(BaseCommand):
    async def execute(self) -> int:
        return 3
