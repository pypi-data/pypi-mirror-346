from typing import Any

from textcompose.content.content import BaseContent, Condition


class Format(BaseContent):
    def __init__(self, template: str, when: Condition | None = None) -> None:
        super().__init__(when=when)
        self.template = template

    def render(self, context: dict[str, Any], **kwargs) -> str | None:
        if not self._check_when(context, **kwargs):
            return None
        return self.template.format_map(context)
