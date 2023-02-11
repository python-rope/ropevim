from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MockBuffer:
    name: str


@dataclass
class MockWindow:
    buffer: MockBuffer


@dataclass
class MockTab:
    windows: List[MockWindow] = field(default_factory=list)

    def add_window(self, name):
        self.windows.append(MockWindow(MockBuffer(name)))


@dataclass
class MockCurrent:
    tabpage: Optional[MockTab]
    window: Optional[MockWindow]
    buffer: Optional[MockBuffer]


class MockVim:
    def __init__(self):
        self.recorded_commands = []
        self.results = defaultdict(list)
        self.tabpages = []
        self.current = MockCurrent(None, None, None)

    @property
    def buffers(self):
        return [window.buffer for tab in self.tabpages for window in tab.windows]

    def add_tab(self):
        tab = MockTab()
        self.tabpages.append(tab)
        return tab

    def reset(self):
        self.recorded_commands = []

    def command(self, command):
        self.recorded_commands.append(command)

    def set_eval(self, expression, value):
        self.results[expression].append(value)

    def eval(self, expression):
        return self.results[expression].pop()
