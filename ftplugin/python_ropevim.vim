if has("python3") && (get(g:, "ropevim_prefer_py3", 0) || get(b:, "ropevim_prefer_py3", 0))
  " Force the use of python3 also in python2 scripts.
  " This needs to be enabled explicitly: 
  " doing so should help with python3 compatiblity,
  " but could require dropping python2.6- support.
  command! -buffer -nargs=+ PythonCmd python3 <args>
elseif has("python2") || has("python")
  command! -buffer -nargs=+ PythonCmd python <args>
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
