import vim

_completer = None


def get_value_completer(python_cmd):
    global _completer
    if _completer is None:
        _completer = ValueCompleter()
        vim.command(f"{python_cmd} import vim")
        vim.command(
            "function! RopeValueCompleter(A, L, P)\n"
            f'{python_cmd} args = [vim.eval("a:" + p) for p in "ALP"]\n'
            f"{python_cmd} ropevim._value_completer._completer(*args)\n"
            "return s:completions\n"
            "endfunction\n"
        )
    return _completer


class ValueCompleter:
    def __init__(self):
        self.values = []

    def __call__(self, arg_lead, cmd_line, cursor_pos):
        # don't know if self.values can be empty but better safe then sorry
        if self.values:
            if not isinstance(self.values[0], str):
                result = [
                    proposal.name
                    for proposal in self.values
                    if proposal.name.startswith(arg_lead)
                ]
            else:
                result = [
                    proposal
                    for proposal in self.values
                    if proposal.startswith(arg_lead)
                ]
            vim.command(f"let s:completions = {result}")
