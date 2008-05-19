"""ropevim, a vim mode for using rope refactoring library"""
import ropemode.decorators
import ropemode.interface
import ropemode.environment
import vim


class VimUtils(ropemode.environment.Environment):

    def ask(self, prompt, default=None, starting=None):
        if starting is None:
            starting = ''
        return call('input("%s", "%s")' % (prompt, starting))

    def ask_values(self, prompt, values, default=None, starting=None):
        self._print_values(values)
        starting = starting or default or ''
        _completer.values = values
        answer = call('input("%s", "%s", "customlist,RopeCompleter")' %
                      (prompt, starting))
        if answer.isdigit() and 0 <= int(answer) < len(values):
            return values[int(answer)]
        if not answer and 'cancel' in values:
            return 'cancel'
        return answer

    def _print_values(self, values):
        numbered = []
        for index, value in enumerate(values):
            numbered.append('%s. %s' % (index, str(value)))
        echo('\n'.join(numbered) + '\n')

    def ask_directory(self, prompt, default=None, starting=None):
        return call('input("%s", ".", "dir")' % prompt)

    def ask_completion(self, prompt, values, starting=None):
        return self.ask_values(prompt, values, starting=starting)

    def message(self, message):
        echo(message)

    def yes_or_no(self, prompt):
        return self.ask_values(prompt, ['yes', 'no']) == 'yes'

    def y_or_n(self, prompt):
        return self.yes_or_no(prompt)

    def get(self, name):
        return vim.eval('g:ropevim_%s' % name)

    def get_offset(self):
        result = self._position_to_offset(*vim.current.window.cursor)
        return result

    def _position_to_offset(self, lineno, colno):
        result = colno
        for line in self.buffer[:lineno-1]:
            result += len(line) + 1
        return result

    def get_text(self):
        return '\n'.join(self.buffer) + '\n'

    def get_region(self):
        start = self._position_to_offset(*self.buffer.mark('<'))
        end = self._position_to_offset(*self.buffer.mark('>'))
        return start, end

    @property
    def buffer(self):
        return vim.current.buffer

    def filename(self):
        return self.buffer.name

    def is_modified(self):
        return vim.eval('&modified')

    def goto_line(self, lineno):
        vim.current.window.cursor = (lineno, 0)

    def insert_line(self, line, lineno):
        self.buffer[lineno - 1:lineno - 1] = [line]

    def insert(self, text):
        lineno, colno = vim.current.window.cursor
        line = self.buffer[lineno - 1]
        self.buffer[lineno - 1] = line[:colno] + text + line[colno:]
        vim.current.window.cursor = (lineno, colno + len(text))

    def delete(self, start, end):
        lineno1, colno1 = self._offset_to_position(start)
        lineno2, colno2 = self._offset_to_position(end)
        lineno, colno = vim.current.window.cursor
        if lineno1 == lineno2:
            line = self.buffer[lineno1 - 1]
            self.buffer[lineno1 - 1] = line[:colno1] + line[colno2:]
            if lineno == lineno1 and colno >= colno1:
                diff = colno2 - colno1
                vim.current.window.cursor = (lineno, max(0, colno - diff))

    def _offset_to_position(self, offset):
        text = self.get_text()
        lineno = text.count('\n', 0, offset) + 1
        try:
            colno = offset - text.rindex('\n', 0, offset) - 2
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
        vim.command('wall')

    def reload_files(self, filenames, moves={}):
        initial = self.filename()
        for filename in filenames:
            if filename in moves:
                filename = moves[filename]
            self.find_file(filename)
        if initial:
            self.find_file(initial)

    def find_file(self, filename, readonly=False, other=False):
        vim.command('e %s' % filename)

    def create_progress(self, name):
        return VimProgress(name)

    def current_word(self):
        pass

    def push_mark(self):
        pass

    def prefix_value(self, prefix):
        return prefix

    def show_occurrences(self, locations):
        result = []
        for location in locations:
            result.append('%s:%s %s' % location)
        echo('\n'.join(result))

    def show_doc(self, docs, altview=False):
        if docs:
            echo(docs)

    def preview_changes(self, diffs):
        echo(diffs)
        return self.y_or_n('Do the changes?')

    def local_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix,
                          prekey=self.get('local_prefix'))

    def global_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix,
                          prekey=self.get('global_prefix'))

    def add_hook(self, name, callback, hook):
        mapping = {'before_save': 'FileWritePre,BufWritePre',
                   'after_save': 'FileWritePost,BufWritePost',
                   'exit': 'VimLeave'}
        self._add_function(name, callback)
        vim.command('autocmd %s *.py call %s()' %
                    (mapping[hook], _vim_name(name)))

    def _add_command(self, name, callback, key, prefix, prekey):
        self._add_function(name, callback, prefix)
        vim.command('command! %s call %s()' %
                    (_vim_name(name), _vim_name(name)))
        if key is not None:
            key = prekey + key.replace(' ', '')
            vim.command('map %s :call %s()<cr>' % (key, _vim_name(name)))

    def _add_function(self, name, callback, prefix=False):
        globals()[name] = callback
        arg = 'None' if prefix else ''
        vim.command('function! %s()\n' % _vim_name(name) +
                    'python ropevim.%s(%s)\n' % (name, arg) +
                    'endfunction\n')


def _vim_name(name):
    tokens = name.split('_')
    newtokens = ['Rope'] + [token.title() for token in tokens]
    return ''.join(newtokens)


class VimProgress(object):

    def __init__(self, name):
        self.name = name
        self.last = 0
        self.per_dot = 2
        echo('%s ' % self.name)

    def update(self, percent):
        dots = (100 - self.last) / self.per_dot
        if dots:
            self.last += dots * self.per_dot
            self._echon('.' * dots)

    def done(self):
        self._echon(' done')

    def _echon(self, message):
        vim.command('echon "%s"' % message)


def echo(message):
    vim.command('echo "%s"' % message)

def call(command):
    vim.command('let s:result = %s' % command)
    return vim.eval('s:result')


class _ValueCompleter(object):

    def __init__(self):
        self.values = []
        vim.command('python import vim')
        vim.command('function! RopeCompleter(A, L, P)\n'
                    'python args = [vim.eval("a:" + p) for p in "ALP"]\n'
                    'python ropevim._completer(*args)\n'
                    'return s:completions\n'
                    'endfunction\n')

    def __call__(self, arg_lead, cmd_line, cursor_pos):
        result = [value for value in self.values if value.startswith(arg_lead)]
        vim.command('let s:completions = %s' % result)


variables = {'ropevim_enable_autoimport': 1,
             'ropevim_autoimport_underlineds': 0,
             'ropevim_codeassist_maxfixes' : 1,
             'ropevim_enable_shortcuts' : 1,
             'ropevim_autoimport_modules': '[]',
             'ropevim_confirm_saving': 0,
             'ropevim_local_prefix': '"<C-c>r"',
             'ropevim_global_prefix': '"<C-x>p"'}

shortcuts = {'code_assist': '<M-/>',
             'lucky_assist': '<M-?>',
             'goto_definition': '<C-c>g',
             'show_doc': '<C-c>d',
             'find_occurrences': '<C-c>f'}

def _init_variables():
    for variable, default in variables.items():
        vim.command('if !exists("g:%s")\n' % variable +
                    '  let g:%s = %s\n' % (variable, default))

def _enable_shortcuts():
    if VimUtils().get('enable_shortcuts'):
        for command, shortcut in shortcuts.items():
            vim.command('map %s :call %s()<cr>' %
                        (shortcut, _vim_name(command)))

ropemode.decorators.logger.message = echo
_completer = _ValueCompleter()

_init_variables()
_interface = ropemode.interface.RopeMode(env=VimUtils())
_interface.init()
_enable_shortcuts()
