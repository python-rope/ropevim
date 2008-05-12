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
        echo(prompt)
        numbered = []
        for index, value in enumerate(values):
            numbered.append('%s. %s' % (index, value))
        result = call('inputlist(%s)' % numbered)
        return values[int(result)]

    def ask(self, prompt, default=None, starting=None):
        return call('input("%s")' % prompt)

    def ask_directory(self, prompt, default=None, starting=None):
        return call('browsedir("%s", ".")' % prompt)

    def message(self, message):
        echo(message)

    def yes_or_no(self, prompt):
        return call('confirm("%s")' % prompt)

    def y_or_n(self, prompt):
        pass

    def get(self, name):
        pass

    def get_offset(self):
        pass

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
        pass

    def find_file(self, filename, readonly=False, other=False):
        pass

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
        pass

    def preview_changes(self, diffs):
        pass

    def local_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix, prekey='<F12>r')

    def global_command(self, name, callback, key=None, prefix=False):
        self._add_command(name, callback, key, prefix, prekey='<F12>p')

    def add_hook(self, name, callback, hook):
        pass

    def _add_command(self, name, callback, key, prefix, prekey):
        globals()[name] = callback
        arg = '0' if prefix else ''
        vim.command('function! %s()\n' % _vim_name(name) +
                    'python ropevim.%s(%s)\n' % (name, arg) +
                    'endfunction\n')
        if key is not None:
            key = prekey + key.replace(' ', '')
            vim.command('map %s :call %s()' % (key, _vim_name(name)))


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
