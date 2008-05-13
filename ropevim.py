"""ropevim, a vim mode for using rope refactoring library"""
import ropemode.decorators
import ropemode.dialog
import ropemode.interface
import vim
from rope.base import taskhandle


class VIMUtils(object):

    def askdata(self, data, starting=None):
        """`data` is a `ropemode.dialog.Data` object"""
        ask_func = self.ask
        ask_args = {'prompt': data.prompt, 'starting': starting,
                    'default': data.default}
        if data.values:
            ask_func = self.ask_values
            ask_args['values'] = data.values
        elif data.kind == 'directory':
            ask_func = self.ask_directory
        return ask_func(**ask_args)

    def ask_values(self, prompt, values, default=None, starting=None, exact=True):
        if default:
            prompt = prompt
        numbered = [prompt]
        for index, value in enumerate(values):
            numbered.append('%s. %s' % (index + 1, value))
        result = int(call('inputlist(%s)' % numbered))
        if result != 0:
            return values[result - 1]

    def ask(self, prompt, default=None, starting=None):
        if starting is None:
            starting = ''
        return call('input("%s", "%s")' % (prompt, starting))

    def ask_directory(self, prompt, default=None, starting=None):
        return call('browsedir("%s", ".")' % prompt)

    def message(self, message):
        echo(message)

    def yes_or_no(self, prompt):
        return self.ask_values(prompt, ['yes', 'no']) == 'yes'

    def y_or_n(self, prompt):
        return self.yes_or_no(prompt)

    def get(self, name):
        pass

    def get_offset(self):
        lineno, colno = vim.current.window.cursor
        result = colno
        for line in vim.current.buffer[:lineno-1]:
            result += len(line) + 1
        return result

    def get_text(self):
        return '\n'.join(vim.current.buffer) + '\n'

    def get_region(self):
        pass

    def filename(self):
        return vim.current.buffer.name

    def is_modified(self):
        pass

    def goto_line(self, lineno):
        pass

    def insert_line(self, line, lineno):
        vim.current.buffer[lineno:lineno] = line

    def insert(self, text):
        pass

    def delete(self, start, end):
        pass

    def filenames(self):
        result = []
        for buffer in vim.buffers:
            if buffer.name:
                result.append(buffer.name)
        return result

    def save_files(self, filenames, ask=False):
        pass

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
        pass

    def show_doc(self, docs):
        echo(diffs)

    def preview_changes(self, diffs):
        echo(diffs)
        return self.y_or_n('Do the changes?')

    def local_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix, prekey='<F12>r')

    def global_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix, prekey='<F12>p')

    def add_hook(self, name, callback, hook):
        mapping = {'before_save': 'FileWritePre,BufWritePre',
                   'after_save': 'FileWritePost,BufWritePost',
                   'exit': 'VimLeave'}
        self._add_function(name, callback)
        vim.command('autocmd %s *.py call %s()' %
                    (mapping[hook], _vim_name(name)))

    def _add_command(self, name, callback, key, prefix, prekey):
        self._add_function(name, callback, prefix)
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
        self.update(0)

    def update(self, percent):
        if percent != 0:
            echo('%s ... %s%%%%' % (self.name, percent))
        else:
            echo('%s ... ' % self.name)

    def done(self):
        echo('%s ... done' % self.name)


class _VIMDo(object):

    def __call__(self, *args):
        vim.command.do('call ')

def echo(message):
    vim.command('echo "%s"' % message)

def call(command):
    vim.command('let s:result = %s' % command)
    return vim.eval('s:result')


ropemode.decorators.logger.message = echo
_interface = ropemode.interface.RopeMode(env=VIMUtils())
_interface.init()
