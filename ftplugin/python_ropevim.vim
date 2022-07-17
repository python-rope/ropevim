" Save the opportunity for some other Python interpreters (pypy?)
if has("python3")
  command! -buffer -nargs=+ PythonCmd python3 <args>
else
  finish
endif

function! LoadRope()
  PythonCmd << EOF
import ropevim

ropevim.load_ropevim()
EOF
endfunction

call LoadRope()
