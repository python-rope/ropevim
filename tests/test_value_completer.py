import pytest
from ropevim._value_completer import ValueCompleter


@pytest.fixture
def value_completer():
    return ValueCompleter()


def test_value_completer_empty_match(value_completer, mock_vim):
    value_completer.values = ["some_value"]
    value_completer("", None, None)

    assert mock_vim.recorded_commands == ["let s:completions = ['some_value']"]


def test_value_completer_choses_match_of_two(value_completer, mock_vim):
    value_completer.values = ["some_value", "some_other_value"]
    value_completer("some_o", None, None)

    assert mock_vim.recorded_commands == ["let s:completions = ['some_other_value']"]
