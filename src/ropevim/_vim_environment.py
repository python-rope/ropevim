import os
import re
import tempfile

import ropemode.decorators
import ropemode.environment
import ropemode.interface
import vim

variables = {
    "enable_autoimport": 1,
    "autoimport_underlineds": 0,
    "codeassist_maxfixes": 1,
    "enable_shortcuts": 1,
    "open_files_in_tabs": 0,
    "autoimport_modules": "[]",
    "confirm_saving": 0,
    "local_prefix": '"<C-c>r"',
    "global_prefix": '"<C-x>p"',
    "vim_completion": 0,
    "guess_project": 0,
}

shortcuts = {
    "code_assist": "<M-/>",
    "lucky_assist": "<M-?>",
    "goto_definition": "<C-c>g",
    "show_doc": "<C-c>d",
    "find_occurrences": "<C-c>f",
}

insert_shortcuts = {"code_assist": "<M-/>", "lucky_assist": "<M-?>"}

SEPARATOR = None

menu_structure = (
    "open_project",
    "close_project",
    "find_file",
    "undo",
    "redo",
    SEPARATOR,
    "rename",
    "extract_variable",
    "extract_method",
    "inline",
    "move",
    "restructure",
    "use_function",
    "introduce_factory",
    "change_signature",
    "rename_current_module",
    "move_current_module",
    "module_to_package",
    SEPARATOR,
    "code_assist",
    "goto_definition",
    "show_doc",
    "find_occurrences",
    "lucky_assist",
    "jump_to_global",
    "show_calltip",
)


class VimEnvironment(ropemode.environment.Environment):
    def __init__(self, completer, python_cmd):
        self._completer = completer
        self._python_cmd = python_cmd

    def load_variables(self):
        for var in variables.items():
            self.set(*var)

    def load_shortcuts(self):
        if self.get("enable_shortcuts"):
            for shortcut in shortcuts.items():
                self.set_shortcut(*shortcut)
            for shortcut in insert_shortcuts.items():
                self.set_insert_shortcut(*shortcut)

    def load_menu(self):
        self.add_menu(menu_structure)
        self.add_menu(menu_structure, "PopUp.&Ropevim")

    def ask(self, prompt, default=None, starting=None):
        if starting is None:
            starting = ""
        if default is not None:
            prompt = prompt + ("[%s] " % default)
        result = vim.eval('input("%s", "%s")' % (prompt, starting))
        if default is not None and result == "":
            return default
        return result

    def ask_values(self, prompt, values, default=None, starting=None, show_values=None):
        if show_values or (show_values is None and len(values) < 14):
            self._print_values(values)
        if default is not None:
            prompt = prompt + ("[%s] " % default)
        starting = starting or ""
        self._completer.values = values
        answer = vim.eval(
            'input("%s", "%s", "customlist,RopeValueCompleter")' % (prompt, starting)
        )
        if answer is None:
            if "cancel" in values:
                return "cancel"
            return
        if default is not None and not answer:
            return default
        if answer.isdigit() and 0 <= int(answer) < len(values):
            return values[int(answer)]
        return answer

    def _print_values(self, values):
        numbered = []
        for index, value in enumerate(values):
            numbered.append("%s. %s" % (index, str(value)))
        self.message("\n".join(numbered) + "\n")

    def ask_directory(self, prompt, default=None, starting=None):
        return vim.eval('input("%s", ".", "dir")' % prompt)

    def ask_completion(self, prompt, values, starting=None):
        if self.get("vim_completion") and "i" in vim.eval("mode()"):
            if not self.get("extended_complete", False):
                proposals = ",".join(
                    "'%s'" % self._completion_text(proposal) for proposal in values
                )
            else:
                proposals = ",".join(
                    self._extended_completion(proposal) for proposal in values
                )

            col = int(vim.eval('col(".")'))
            if starting:
                col -= len(starting)
            command = "call complete(%s, [%s])" % (col, proposals)
            vim.command(command.encode(self._get_encoding()))
            return None
        return self.ask_values(prompt, values, starting=starting, show_values=False)

    def message(self, message):
        print(message)

    def yes_or_no(self, prompt):
        return self.ask_values(prompt, ["yes", "y", "no", "n"]).lower() in ["yes", "y"]

    def y_or_n(self, prompt):
        return self.yes_or_no(prompt)

    def get(self, name, default=None):
        vimname = "g:ropevim_%s" % name
        if str(vim.eval('exists("%s")' % vimname)) == "0":
            return default
        result = vim.eval(vimname)
        if isinstance(result, str) and result.isdigit():
            return int(result)
        return result

    def get_offset(self):
        result = self._position_to_offset(*self.cursor)
        return result

    def _get_encoding(self):
        return vim.eval("&encoding")

    def _encode_line(self, line):
        return line.encode(self._get_encoding())

    def _decode_line(self, line):
        if hasattr(line, "decode"):
            return line.decode(self._get_encoding())
        else:
            return line

    def _position_to_offset(self, lineno, colno):
        result = min(colno, len(self.buffer[lineno - 1]) + 1)
        for line in self.buffer[: lineno - 1]:
            line = self._decode_line(line)
            result += len(line) + 1
        return result

    def get_text(self):
        return self._decode_line("\n".join(self.buffer)) + "\n"

    def get_region(self):
        beg_mark = self.buffer.mark("<")
        end_mark = self.buffer.mark(">")
        if beg_mark and end_mark:
            start = self._position_to_offset(*beg_mark)
            end = self._position_to_offset(*end_mark) + 1
            return start, end
        else:
            return 0, 0

    @property
    def buffer(self):
        return vim.current.buffer

    def _get_cursor(self):
        lineno, col = vim.current.window.cursor
        line = self._decode_line(vim.current.line[:col])
        col = len(line)
        return (lineno, col)

    def _set_cursor(self, cursor):
        lineno, col = cursor
        line = self._decode_line(vim.current.line)
        line = self._encode_line(line[:col])
        col = len(line)
        vim.current.window.cursor = (lineno, col)

    cursor = property(_get_cursor, _set_cursor)

    def filename(self):
        return self.buffer.name

    def is_modified(self):
        return vim.eval("&modified")

    def goto_line(self, lineno):
        self.cursor = (lineno, 0)

    def insert_line(self, line, lineno):
        self.buffer[lineno - 1 : lineno - 1] = [line]

    def insert(self, text):
        lineno, colno = self.cursor
        line = self.buffer[lineno - 1]
        self.buffer[lineno - 1] = line[:colno] + text + line[colno:]
        self.cursor = (lineno, colno + len(text))

    def delete(self, start, end):
        lineno1, colno1 = self._offset_to_position(start - 1)
        lineno2, colno2 = self._offset_to_position(end - 1)
        lineno, colno = self.cursor
        if lineno1 == lineno2:
            line = self.buffer[lineno1 - 1]
            self.buffer[lineno1 - 1] = line[:colno1] + line[colno2:]
            if lineno == lineno1 and colno >= colno1:
                diff = colno2 - colno1
                self.cursor = (lineno, max(0, colno - diff))

    def _offset_to_position(self, offset):
        text = self.get_text()
        lineno = text.count("\n", 0, offset) + 1
        try:
            colno = offset - text.rindex("\n", 0, offset) - 1
        except ValueError:
            colno = offset
        return lineno, colno

    def filenames(self):
        result = []
        for buffer in vim.buffers:
            if buffer.name:
                result.append(buffer.name)
        return result

    def save_files(self, filenames):
        vim.command("wall")

    def reload_files(self, filenames, moves={}):
        initial = self.filename()
        for filename in filenames:
            self.find_file(moves.get(filename, filename), force=True)
        if initial:
            self.find_file(initial)

    def _open_file(self, filename, new=False):
        # TODO deprecated ... for now it is just an equivalent to
        # g:ropevim_goto_def_newwin == 'tabnew'
        if int(vim.eval("g:ropevim_open_files_in_tabs")):
            new = "tabnew"

        if new in ("new", "vnew", "tabnew"):
            vim.command(new)
        vim.command("edit! %s" % filename)

    @staticmethod
    def _samefile(file1, file2):
        # Breaks under Jython and other platforms, but I guess it should
        # be enough.
        if os.name == "posix" and os.path.exists(file1) and os.path.exists(file2):
            return os.path.samefile(file1, file2)
        else:
            # it is a way more complicated, the following does not deal
            # with hard links on Windows
            # for better discussion see
            # http://stackoverflow.com/q/8892831/164233
            return os.path.normcase(os.path.normpath(file1)) == os.path.normcase(
                os.path.normpath(file2)
            )

    def find_file(self, filename, readonly=False, other=False, force=False):
        """
        Originally coming from Emacs, so the definition is the same as
        the Emacs Lisp function find-file ... "

        (find-file FILENAME &optional WILDCARDS)

        Edit file FILENAME.
        Switch to a buffer visiting file FILENAME,
        creating one if none already exists.
        """
        if filename not in self.filenames() or force:
            self._open_file(filename, new=other)
        else:
            found = False
            for tab in vim.tabpages:
                for win in tab.windows:
                    if self._samefile(win.buffer.name, filename):
                        vim.current.tabpage = tab
                        vim.current.window = win
                        vim.current.buffer = win.buffer
                        found = True
                        break
            if not found:
                self._open_file(filename, new=other)

        if readonly:
            vim.command("set nomodifiable")

    def create_progress(self, name):
        return VimProgress(name)

    def current_word(self):
        return vim.eval('expand("<cword>")')

    def push_mark(self):
        vim.command("mark `")

    def prefix_value(self, prefix):
        return prefix

    def show_occurrences(self, locations):
        self._quickfixdefs(locations)

    def _quickfixdefs(self, locations):
        filename = os.path.join(tempfile.gettempdir(), tempfile.mktemp())
        try:
            self._writedefs(locations, filename)
            vim.command("let old_errorfile = &errorfile")
            vim.command("let old_errorformat = &errorformat")
            vim.command("set errorformat=%f:%l:\ %m")
            vim.command("cfile " + filename)
            vim.command("let &errorformat = old_errorformat")
            vim.command("let &errorfile = old_errorfile")
        finally:
            os.remove(filename)

    def _writedefs(self, locations, filename):
        tofile = open(filename, "w")
        try:
            for location in locations:
                # FIXME seems suspicious lineno = location.lineno
                err = "%s:%d: %s %s\n" % (
                    os.path.relpath(location.filename),
                    location.lineno,
                    location.note,
                    location.line_content,
                )
                self.message(err)
                tofile.write(err)
        finally:
            tofile.close()

    def show_doc(self, docs, altview=False):
        if docs:
            self.message(docs)

    def preview_changes(self, diffs):
        self.message(diffs)
        return self.y_or_n("Do the changes? ")

    def local_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix, prekey=self.get("local_prefix"))

    def global_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix, prekey=self.get("global_prefix"))

    def add_hook(self, name, callback, hook):
        mapping = {
            "before_save": "FileWritePre,BufWritePre",
            "after_save": "FileWritePost,BufWritePost",
            "exit": "VimLeave",
        }
        self._add_function(name, callback)
        vim.command("autocmd %s *.py call %s()" % (mapping[hook], self._vim_name(name)))

    def _add_command(self, name, callback, key, prefix, prekey):
        self._add_function(name, callback, prefix)
        vim.command(
            "command! -range %s call %s()"
            % (self._vim_name(name), self._vim_name(name))
        )
        if key is not None:
            key = prekey + key.replace(" ", "")
            vim.command("noremap %s :call %s()<cr>" % (key, self._vim_name(name)))

    def _add_function(self, name, callback, prefix=False):
        globals()[name] = callback
        arg = "None" if prefix else ""
        vim.command(
            "function! %s() range\n" % self._vim_name(name)
            + "%s ropevim._vim_environment.%s(%s)\n" % (self._python_cmd, name, arg)
            + "endfunction\n"
        )

    def _completion_data(self, proposal):
        return proposal

    _docstring_re = re.compile("^[\s\t\n]*([^\n]*)")

    def _extended_completion(self, proposal):
        # we are using extended complete and return dicts instead of strings.
        # `ci` means "completion item". see `:help complete-items`
        ci = {"word": proposal.name}

        scope = proposal.scope[0].upper()
        type_ = proposal.type
        info = None

        if proposal.scope == "parameter_keyword":
            scope = " "
            type_ = "param"
            if not hasattr(proposal, "get_default"):
                # old version of rope
                pass
            else:
                default = proposal.get_default()
                if default is None:
                    info = "*"
                else:
                    info = "= %s" % default

        elif proposal.scope == "keyword":
            scope = " "
            type_ = "keywd"

        elif proposal.scope == "attribute":
            scope = "M"
            if proposal.type == "function":
                type_ = "meth"
            elif proposal.type == "instance":
                type_ = "prop"

        elif proposal.type == "function":
            type_ = "func"

        elif proposal.type == "instance":
            type_ = "inst"

        elif proposal.type == "module":
            type_ = "mod"

        if info is None:
            obj_doc = proposal.get_doc()
            if obj_doc:
                info = self._docstring_re.match(obj_doc).group(1)
            else:
                info = ""

        if type_ is None:
            type_ = " "
        else:
            type_ = type_.ljust(5)[:5]
        ci["menu"] = " ".join((scope, type_, info))
        ret = "{%s}" % ",".join(
            '"%s":"%s"' % (key, value.replace('"', '\\"'))
            for (key, value) in ci.items()
        )
        return ret

    def set(self, variable, value):
        vim.command(
            'if !exists("g:ropevim_%s")\n' % variable
            + "  let g:ropevim_%s = %s\n" % (variable, value)
        )

    def _vim_name(self, name):
        tokens = name.split("_")
        newtokens = ["Rope"] + [token.title() for token in tokens]
        return "".join(newtokens)

    def set_shortcut(self, command, shortcut):
        vim.command("noremap %s :call %s()<cr>" % (shortcut, self._vim_name(command)))

    def set_insert_shortcut(self, command, shortcut):
        command_name = self._vim_name(command) + "InsertMode"
        vim.command(
            "func! %s()\n" % command_name
            + "call %s()\n" % self._vim_name(command)
            + 'return ""\n'
            "endfunc"
        )
        vim.command("imap %s <C-R>=%s()<cr>" % (shortcut, command_name))

    def add_menu(self, menu_structure, root_node="&Ropevim"):
        cmd_tmpl = "%s <silent> %s.%s :call %s()<cr>"

        vim.command("silent! aunmenu %s" % root_node)

        for i, cb in enumerate(menu_structure):
            if cb is None:
                vim.command("amenu <silent> %s.-SEP%s- :" % (root_node, i))
                continue

            # use_function -> Use\ Function
            name = cb.replace("_", "\ ").title()

            for cmd in ("amenu", "vmenu"):
                vim.command(cmd_tmpl % (cmd, root_node, name, self._vim_name(cb)))


class VimProgress:
    def __init__(self, name):
        self.name = name
        self.last = 0
        print("%s ... " % self.name)

    def update(self, percent):
        try:
            vim.eval("getchar(0)")
        except vim.error:
            raise KeyboardInterrupt("Task %s was interrupted!" % self.name)
        if percent > self.last + 4:
            print("%s ... %s%%%%" % (self.name, percent))
            self.last = percent

    def done(self):
        print("%s ... done" % self.name)
