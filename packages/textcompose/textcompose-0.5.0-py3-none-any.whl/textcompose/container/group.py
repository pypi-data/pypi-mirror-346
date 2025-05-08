from typing import Any, Optional

from textcompose.container.container import BaseContainer
from textcompose.content.content import Value, Condition


class Group(BaseContainer):
    def __init__(self, *children: Value, sep: Optional[str] = "\n", when: Condition | None = None) -> None:
        super().__init__(*children, when=when)
        self.sep = sep

    def render(self, context: dict[str, Any], **kwargs) -> str | None:
        if not self._check_when(context):
            return None

        parts = []
        for comp in self.children:
            if (part := self.resolve_value(comp, context, **kwargs)) is not None:
                parts.append(part)
        return self.sep.join(parts)
