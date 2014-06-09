if !has("python")
    finish
endif

function! LoadRope()
python << EOF
import ropevim
from rope_omni import RopeOmniCompleter
EOF
endfunction

call LoadRope()

" See http://stackoverflow.com/questions/3105307/
" and even better is
" https://github.com/ervandew/supertab/blob/master/plugin/supertab.vim#L863
" autocmd CursorMovedI *
"     \ if pumvisible() == 0 && bufname("%") != "[Command Line]" |
"     \   pclose |
"     \ endif
" autocmd InsertLeave *
"     \ if pumvisible() == 0 && bufname("%") != "[Command Line]" |
"     \   pclose|
"     \ endif
function! s:ClosePreview() " {{{
    let preview = 0
    for bufnum in tabpagebuflist()
        if getwinvar(bufwinnr(bufnum), '&previewwindow')
            let preview = 1
            break
        endif
    endfor
    if preview
        pclose
    endif
endfunction " }}}

augroup supertab_close_preview
    autocmd!
    autocmd InsertLeave,CursorMovedI * call s:ClosePreview()
augroup END

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
