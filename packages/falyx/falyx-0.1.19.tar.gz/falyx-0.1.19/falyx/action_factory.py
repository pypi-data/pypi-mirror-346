from typing import Callable

from falyx.action import BaseAction


class ActionFactoryAction(BaseAction):
    def __init__(
        self,
        name: str,
        factory: Callable[[dict], BaseAction],
        *,
        inject_last_result: bool = False,
        inject_last_result_as: str = "last_result",
    ):
        super().__init__(name, inject_last_result=inject_last_result, inject_last_result_as=inject_last_result_as)
        self.factory = factory

    async def _run(self, *args, **kwargs) -> BaseAction:
        kwargs = self._maybe_inject_last_result(kwargs)
        action = self.factory(kwargs)
        if not isinstance(action, BaseAction):
            raise TypeError(f"[{self.name}] Factory did not return a valid BaseAction.")
        return action
