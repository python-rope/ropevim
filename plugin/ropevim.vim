if !has("python")
    finish
endif

" Add s:script_path referencing ropevim bundle directory
let s:script_path = fnameescape(expand('<sfile>:p:h:h'))

function! LoadRope()
python << EOF
import ropevim
import sys
sys.path.insert(0, vim.eval('expand(s:script_path)'))
from rope_omni import RopeOmniCompleter
EOF
endfunction

call LoadRope()

" The code below is an omni-completer for python using rope and ropevim.
" Created by Ryan Wooden (rygwdn@gmail.com)

function! RopeCompleteFunc(findstart, base)
    " A completefunc for python code using rope
    if (a:findstart)
        py ropecompleter = RopeOmniCompleter(vim.eval("a:base"))
        py vim.command("return %s" % ropecompleter.start)
    else
        py vim.command("return %s" % ropecompleter.complete(vim.eval("a:base")))
    endif
endfunction
