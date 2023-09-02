How to Contribute
=================

Currently you have to send me your changes as patch files or mercurial patch
bundles via mail to:

Goetz Pfeiffer <Goetz.Pfeiffer@helmholtz-berlin.de>

If there is interest in contributing on a larger scale I may create a github
mirror in the future to use it's pull-request mechanism.

Patch files
-----------

If you checked out the sources with::

  hg clone http://hg.code.sf.net/p/epics-sumo/mercurial epics-sumo

and have changed the working copy without committing changes, you can
create a patch file like this::

  hg diff > changes.patch

You can then send me this file by e-mail.

Mercurial patch bundle
----------------------

The general description for doing this with mercurial is found at
`Communicating Changes <https://www.mercurial-scm.org/wiki/CommunicatingChanges>`_ 
at "bundle/unbundle".

If you have committed changes in your working copy, you can create a patch bundle like this::

  hg bundle changes.hg http://hg.code.sf.net/p/epics-sumo/mercurial

The created file, "changes.hg" in this example, is in binary format and
contains your patches in compressed form.

You can then send me this file by e-mail.

