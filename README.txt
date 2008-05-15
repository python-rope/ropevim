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


Variables
=========

* ``ropevim_codeassist_maxfixes``: The maximum number of syntax errors
  to fix for code assists.  The default value is ``1``.
* ``ropevim_local_prefix``: The prefix for ropemacs refactorings.
  Defaults to ``C-c r``.
* ``ropevim_global_prefix``: The prefix for ropemacs project commands
  Defaults to ``C-x p``.
* ``ropevim_enable_shortcuts``: Shows whether to bind ropemacs
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
