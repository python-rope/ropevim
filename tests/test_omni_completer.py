from unittest.mock import MagicMock

from ropevim._rope_omni_completer import RopeOmniCompleter
from ropevim._vim_environment import VimEnvironment


def test_rope_omni_completer_get_start(mock_vim):
    mock_code_assist = MagicMock()

    mock_code_assist.offset = 40
    mock_code_assist.starting_offset = 10

    mock_vim.set_eval("col('.')", 50)

    omni_completer = RopeOmniCompleter(
        mock_code_assist, VimEnvironment(MagicMock(), "python3")
    )

    assert omni_completer.get_start() == 19
