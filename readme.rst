Ropevim Omnicompleter
---------------------

An omni-completer for python using rope and ropevim. Designed to work
nicely with supertab.

This code uses a lot of internal functions, etc. from rope and ropemode so
it is likely to break. You have been warned.

Created by Ryan Wooden (rygwdn at gmail dot com)

This plugin requires ropevim_. You can install it with ``pip install ropevim``
or ``easy_install ropevim``.

.. _ropevim: http://rope.sourceforge.net/ropevim.html

Installation
------------

This plugin should be easily installed with pathogen or similar. If you're
not using something like that, just place the files in the appropriate
directory in your ``~/.vim`` directory.

Once installed, you can enable it by putting something like this in your ``.vimrc``::
    autocmd FileType python setlocal omnifunc=RopeCompleteFunc
