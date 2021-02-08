" Save the opportunity for some other Python interpreters (pypy?)
if has("python3")
  command! -buffer -nargs=+ PythonCmd python3 <args>
else
  finish
endif

if exists("g:load_ropevim")
   finish
endif

let g:load_ropevim = "py1.0"
if !exists("g:ropevim_virtualenv")
  if has("nvim")
    let g:ropevim_virtualenv = "~/.local/share/nvim/ropevim"
  else
    let g:ropevim_virtualenv = "~/.vim/ropevim"
  endif
endif
if !exists("g:ropevim_quiet")
  let g:ropevim_quiet = 0
endif

python3 << EndPython3
import collections
import os
import sys
import vim
from distutils.util import strtobool

def _get_python_binary(exec_prefix):
  try:
    default = vim.eval("g:pymode_python").strip()
  except vim.error:
    default = ""
  if default and os.path.exists(default):
    return default
  if sys.platform[:3] == "win":
    return exec_prefix / 'python.exe'
  return exec_prefix / 'bin' / 'python3'

def _get_pip(venv_path):
  if sys.platform[:3] == "win":
    return venv_path / 'Scripts' / 'pip.exe'
  return venv_path / 'bin' / 'pip'

def _get_virtualenv_site_packages(venv_path, pyver):
  if sys.platform[:3] == "win":
    return venv_path / 'Lib' / 'site-packages'
  return venv_path / 'lib' / f'python{pyver[0]}.{pyver[1]}' / 'site-packages'

def _initialize_ropevim_env(upgrade=False):
  pyver = sys.version_info[:2]
  if pyver < (3, 6):
    print("Sorry, ropevim requires Python 3.6+ to run.")
    return False

  from pathlib import Path
  import subprocess
  import venv
  virtualenv_path = Path(vim.eval("g:ropevim_virtualenv")).expanduser()
  virtualenv_site_packages = str(_get_virtualenv_site_packages(virtualenv_path, pyver))
  first_install = False
  if not virtualenv_path.is_dir():
    print('Please wait, one time setup for ropevim.')
    _executable = sys.executable
    _base_executable = getattr(sys, "_base_executable", _executable)
    try:
      executable = str(_get_python_binary(Path(sys.exec_prefix)))
      sys.executable = executable
      sys._base_executable = executable
      print(f'Creating a virtualenv in {virtualenv_path}...')
      print('(this path can be customized in .vimrc by setting g:ropevim_virtualenv)')
      venv.create(virtualenv_path, with_pip=True)
    except Exception:
      print('Encountered exception while creating virtualenv (see traceback below).')
      print(f'Removing {virtualenv_path}...')
      import shutil
      shutil.rmtree(virtualenv_path)
      raise
    finally:
      sys.executable = _executable
      sys._base_executable = _base_executable
    first_install = True
  if first_install:
    print('Installing ropevim with pip...')
  if upgrade:
    print('Upgrading ropevim with pip...')
  if first_install or upgrade:
    subprocess.run([str(_get_pip(virtualenv_path)), 'install', '-U', 'rope', 'ropevim', 'ropemode',], stdout=subprocess.PIPE)
    print('DONE! You are all set, thanks for waiting ✨ 🍰 ✨')
  if virtualenv_site_packages not in sys.path:
    sys.path.insert(0, virtualenv_site_packages)
  return True

if _initialize_ropevim_env():
  import ropevim
  import time

EndPython3

function! LoadRope()
  PythonCmd << EOF
import ropevim
from rope_omni import RopeOmniCompleter
EOF
endfunction

call LoadRope()

" The code below is an omni-completer for python using rope and ropevim.
" Created by Ryan Wooden (rygwdn@gmail.com)

function! RopeCompleteFunc(findstart, base)
    " A completefunc for python code using rope
    if (a:findstart)
        PythonCmd ropecompleter = RopeOmniCompleter(vim.eval("a:base"))
        PythonCmd vim.command("return %s" % ropecompleter.start)
    else
        PythonCmd vim.command("return %s" % ropecompleter.complete(vim.eval("a:base")))
    endif
endfunction
