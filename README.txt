======================
 ropevim, rope in vim
======================

Ropevim is a vim mode that uses rope_ library to provide features like
refactorings and code-assists.  You should install rope_ library
before using ropevim.

.. _rope: http://rope.sf.net/


New Features
============


Setting Up
==========

First add ropevim folder to the ``PYTHONPATH`` (or install it using
``python setup.py install``).

Then load ``ropevim.vim`` in vim.  That can be done either by adding
``source path/to/ropevim.vim`` to your ``~/.vimrc`` or copying it to
``~/.vim/plugin/`` folder.

If you don't want to install rope and ropevim you can add something
like this to your ``~/.vimrc``::

  let $PYTHONPATH .= ":/path/to/rope:/path/to/ropevim"
  source /path/to/ropevim.vim

For using the repository version of rope, see ``docs/ropevim.txt``.


Getting Started
===============

Enabling Autoimport
-------------------

Rope can propose and automatically import global names in other
modules.  Rope maintains a cache of global names for each project.  It
updates the cache only when modules are changed; if you want to cache
all your modules at once, use ``RopeGenerateAutoimportCache``.  It
will cache all of the modules inside the project plus those whose
names are listed in ``ropevim_autoimport_modules`` list::

  # add the name of modules you want to autoimport
  let g:ropevim_autoimport_modules = ["os", "shutil"]

Now if you are in a buffer that contains::

  rmtree

and you execute ``RopevimAutoImport`` you'll end up with::

  from shutil import rmtree
  rmtree

Also ``RopeCodeAssist`` and ``RopeLuckyAssist`` propose auto-imported
names by using ``name : module`` style.  Selecting them will import
the module automatically.


Filtering Resources
-------------------

Some refactorings, restructuring and find occurrences take an option
called resources.  This option can be used to limit the resources on
which a refactoring should be applied.

It uses a simple format: each line starts with either '+' or '-'.
Each '+' means include the file (or its children if it's a folder)
that comes after it.  '-' has the same meaning for exclusion.  So
using::

  +rope
  +ropetest
  -rope/contrib

means include all python files inside ``rope`` and ``ropetest``
folders and their subfolder, but those that are in ``rope/contrib``.
Or::

  -ropetest
  -setup.py

means include all python files inside the project but ``setup.py`` and
those under ``ropetest`` folder.


Finding Occurrences
-------------------

The find occurrences command (``C-c f`` by default) can be used to
find the occurrences of a python name.  If ``unsure`` option is
``yes``, it will also show unsure occurrences; unsure occurrences are
indicated with a ``?`` mark in the end.


Dialog ``batchset`` Command
---------------------------

When you use ropevim dialogs there is a command called ``batchset``.
It can set many options at the same time.  After selecting this
command from dialog base prompt, you are asked to enter a string.

``batchset`` strings can set the value of configs in two ways.  The
single line form is like this::

  name1 value1
  name2 value2

That is the name of config is followed its value.  For multi-line
values you can use::

  name1
   line1
   line2

  name2
   line3

Each line of the definition should start with a space or a tab.  Note
that blank lines before the name of config definitions are ignored.

``batchset`` command is useful when performing refactorings with long
configs, like restructurings::

  pattern ${pycore}.create_module(${project}.root, ${name})

  goal generate.create_module(${project}, ${name})

  imports
   from rope.contrib import generate

  args
   pycore: type=rope.base.pycore.PyCore
   project: type=rope.base.project.Project

.. ignore the two-space indents

This is a valid ``batchset`` string for restructurings.  When using
batchset, you usually want to skip initial questions.  That can be
done by prefixing refactorings.

Just for the sake of completeness, the reverse of the above
restructuring can be::

  pattern ${create_module}(${project}, ${name})

  goal ${project}.pycore.create_module(${project}.root, ${name})

  args
   create_module: name=rope.contrib.generate.create_module
   project: type=rope.base.project.Project


Variables
=========

* ``ropevim_codeassist_maxfixes``: The maximum number of syntax errors
  to fix for code assists.  The default value is ``1``.
* ``ropevim_local_prefix``: The prefix for ropevim refactorings.
  Defaults to ``C-c r``.
* ``ropevim_global_prefix``: The prefix for ropevim project commands
  Defaults to ``C-x p``.
* ``ropevim_enable_shortcuts``: Shows whether to bind ropevim
  shortcuts keys.  Defaults to ``t``.

* ``ropevim_enable_autoimport``: Shows whether to enable autoimport.
  Defaults to ``nil``.
* ``ropevim_autoimport_modules``: The name of modules whose global
  names should be cached.  `rope-generate-autoimport-cache' reads this
  list and fills its cache.
* ``ropevim_autoimport_underlineds``: If set, autoimport will cache
  names starting with underlines, too.


Keybinding
==========

Uses almost the same keybinding as ropemacs.  Note that global
commands have a ``C-x p`` prefix and local commands have a ``C-c r``
prefix.  You can change that (see variables_ section).

================  ============================
Key               Command
================  ============================
C-x p o           RopeOpenProject
C-x p k           RopeCloseProject
C-x p f           RopeFindFile
C-x p 4 f         RopeFindFileOtherWindow
C-x p u           RopeUndo
C-x p r           RopeRedo
C-x p c           RopeProjectConfig
C-x p n [mpfd]    RopeCreate(Module|Package|File|Directory)
                  RopeWriteProject

C-c r r           RopeRename
C-c r l           RopeExtractVariable
C-c r m           RopeExtractMethod
C-c r i           RopeInline
C-c r v           RopeMove
C-c r x           RopeRestructure
C-c r u           RopeUseFunction
C-c r f           RopeIntroduceFactory
C-c r s           RopeChangeSignature
C-c r 1 r         RopeRenameCurrentModule
C-c r 1 v         RopeMoveCurrentModule
C-c r 1 p         RopeModuleToPackage

C-c r o           RopeOrganizeImports
C-c r n [vfcmp]   RopeGenerate(Variable|Function|Class|Module|Package)

C-c r a /         RopeCodeAssist
C-c r a g         RopeGotoDefinition
C-c r a d         RopeShowDoc
C-c r a f         RopeFindOccurrences
C-c r a ?         RopeLuckyAssist
C-c r a j         RopeJumpToGlobal
C-c r a c         RopeShowCalltip
                  RopeAnalyzeModule

                  RopeAutoImport
                  RopeGenerateAutoimportCache
===============   ============================


Shortcuts
---------

Some commands are used very frequently; specially the commands in
code-assist group.  You can define your own shortcuts like this::

  :map <C-c>g :call RopeGotoDefinition()

Ropevim itself comes with a few shortcuts.  These shortcuts will be
used only when ``ropevim_enable_shortcuts`` is set.

================  ============================
Key               Command
================  ============================
M-/               RopeCodeAssist
M-?               RopeLuckyAssist
C-c g             RopeGotoDefinition
C-c d             RopeShowDoc
C-c f             RopeFindOccurrences
================  ============================


Contributing
============

Send your bug reports, feature requests and patches to `rope-dev (at)
googlegroups.com`_.

.. _`rope-dev (at) googlegroups.com`: http://groups.google.com/group/rope-dev


License
=======

This program is under the terms of GPL (GNU General Public License).
Have a look at ``COPYING`` file for more information.
