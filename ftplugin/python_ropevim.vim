" Save the opportunity for some other Python interpreters (pypy?)
if has("python3")
  command! -buffer -nargs=+ PythonCmd python3 <args>
else
  finish
endif

function! LoadRope()
  PythonCmd << EOF
import ropevim

if not hasattr(ropevim, "__version__") or ropevim.__version__ != "0.9.0":
    print(
        "Mismatching version for pip installed ropevim,"
        " please run 'pip install --upgrade ropevim' and make sure"
        " the version of the ropevim vim plugin is up to date"
    )
else:
    ropevim.load_ropevim()
EOF
endfunction

call LoadRope()
