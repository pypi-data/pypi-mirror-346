from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import rich

if TYPE_CHECKING:
    from rich.console import Console


@dataclass
class MessageStyle:
    icon: str
    label: str
    icon_color: str
    bg_color: str
    text_color: str
    icon_bg: str


BLANK = "\u2800"
DEFAULT_STYLE = {
    "success": MessageStyle(
        icon="✔",
        label="Success",
        icon_color="#16A34A",
        bg_color="#DCFCE7",
        text_color="#14532D",
        icon_bg="#16A34A",
    ),
    "error": MessageStyle(
        icon="✖",
        label="Error",
        icon_color="#DC2626",
        bg_color="#FEE2E2",
        text_color="#7F1D1D",
        icon_bg="#DC2626",
    ),
    "warning": MessageStyle(
        icon="⚠",
        label="Warning",
        icon_color="#D97706",
        bg_color="#FEF3C7",
        text_color="#78350F",
        icon_bg="#D97706",
    ),
    "info": MessageStyle(
        icon="🛈",
        label="Info",
        icon_color="#2563EB",
        bg_color="#DBEAFE",
        text_color="#1E3A8A",
        icon_bg="#2563EB",
    ),
}


class Logger:
    def __init__(
        self,
        console: Console | None = None,
        style: dict[str, MessageStyle] | None = None,
    ) -> None:
        if not style:
            self.style: dict[str, MessageStyle] = DEFAULT_STYLE
        else:
            self.style: dict[str, MessageStyle] = style

        if not console:
            self.console = rich.get_console()
        else:
            self.console = console

        self.max_label_length = max(len(s.label) for s in self.style.values())

    def _print_message(self, text: str, style: MessageStyle) -> None:
        padded_label = f"{style.icon}  {style.label.ljust(self.max_label_length)}  -"

        prefix = (
            f"[on {style.icon_bg}]{BLANK}[/on {style.icon_bg}]"
            f"[on {style.bg_color}]{BLANK}[/on {style.bg_color}]"
            f"[bold {style.icon_color} on {style.bg_color}]{padded_label}[/bold {style.icon_color} on {style.bg_color}]"
            f"[on {style.bg_color}]{BLANK}[/on {style.bg_color}]"
        )
        content = f"[bold {style.text_color} on {style.bg_color}]{text}[/bold {style.text_color} on {style.bg_color}]"
        suffix_length = max(
            self.console.width
            - len(text)
            - len(style.icon)
            - self.max_label_length
            - 10,
            0,
        )
        suffix = f"[on {style.bg_color}]{BLANK * suffix_length}[/on {style.bg_color}]"
        message = prefix + content + suffix
        self.console.print(message)

    def success(self, text: str) -> None:
        self._print_message(text, self.style["success"])

    def error(self, text: str) -> None:
        self._print_message(text, self.style["error"])

    def warning(self, text: str) -> None:
        self._print_message(text, self.style["warning"])

    def info(self, text: str) -> None:
        self._print_message(text, self.style["info"])

