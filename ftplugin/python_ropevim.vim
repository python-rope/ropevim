" Save the opportunity for some other Python interpreters (pypy?)
if has("python3")
  command! -buffer -nargs=+ PythonCmd python3 <args>
else
  finish
endif

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
