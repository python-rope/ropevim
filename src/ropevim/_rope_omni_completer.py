import ropemode.interface
import vim

_ropecompleter = None


def get_omni_completer(code_assist, environment, python_cmd):
    global _ropecompleter
    if _ropecompleter is None:
        _ropecompleter = RopeOmniCompleter(code_assist, environment)
        vim.command(
            "function! RopeCompleteFunc(findstart, base)\n"
            '    " A completefunc for python code using rope\n'
            "    if (a:findstart)\n"
            f"        {python_cmd} ropecompleter = ropevim._rope_omni_completer._ropecompleter\n"
            f'        {python_cmd} vim.command("return %s" % ropecompleter.get_start())\n'
            "    else\n"
            f'        {python_cmd} vim.command("return %s" % ropecompleter.complete())\n'
            "    endif\n"
            "endfunction\n"
        )
    return _ropecompleter


class RopeOmniCompleter:
    """The class used to complete python code."""

    def __init__(self, code_assist, environment):
        self._environment = environment
        self._assist = code_assist

    def vim_string(self, inp):
        """Creates a vim-friendly string from a group of
        dicts, lists and strings.
        """

        def conv(obj):
            if isinstance(obj, list):
                return "[" + ",".join([conv(o) for o in obj]) + "]"
            elif isinstance(obj, dict):
                return (
                    "{"
                    + ",".join(
                        [
                            "%s:%s" % (conv(key), conv(value))
                            for key, value in obj.items()
                        ]
                    )
                    + "}"
                )
            else:
                return '"%s"' % str(obj).replace('"', '\\"')

        return conv(inp)

    def _get_dict(self, prop):
        ci = self._environment._extended_completion(prop)
        ci["info"] = prop.get_doc() or " "
        return ci

    def complete(self):
        """Gets a completion list using a given base string."""
        if vim.eval("complete_check()") != "0":
            return []

        try:
            proposals = self._assist._calculate_proposals()
        except Exception:  # a bunch of rope stuff
            return []

        ps = [self._get_dict(p) for p in proposals]
        return self.vim_string(ps)

    def get_start(self):
        """Gets the starting column for vim completion."""
        try:
            base_len = self._assist.offset - self._assist.starting_offset
            return int(vim.eval("col('.')")) - base_len - 1
        except Exception:
            return -1
