from unittest.mock import patch

import pytest

from .mock_vim import MockVim

_mock_vim = MockVim()
patch.dict("sys.modules", vim=_mock_vim).start()


@pytest.fixture
def mock_vim():
    _mock_vim.reset()
    return _mock_vim
