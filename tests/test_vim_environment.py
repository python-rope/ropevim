from ropevim._value_completer import ValueCompleter
from ropevim._vim_environment import VimEnvironment


def test_find_empty_file(mock_vim):
    vim_environment = VimEnvironment(ValueCompleter(), "python3")

    tab = mock_vim.add_tab()
    tab.add_window("")
    tab.add_window("some_file")

    vim_environment.find_file("some_file")

    assert mock_vim.current.tabpage == tab
    assert mock_vim.current.buffer.name == "some_file"
