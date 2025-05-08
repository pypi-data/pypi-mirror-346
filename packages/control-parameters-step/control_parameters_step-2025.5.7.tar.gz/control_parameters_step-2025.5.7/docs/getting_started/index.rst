***************
Getting Started
***************

Installation
============
The Control Parameters step is probably already installed in your SEAMM environment, but
if not or if you wish to check, follow the directions for the `SEAMM Installer`_. The
graphical installer is the easiest to use. In the SEAMM conda environment, simply type::

  seamm-installer

or use the shortcut if you installed one. Switch to the second tab, `Components`, and
check for `control-parameters-step`. If it is not installed, or can be updated, check the box
next to it and click `Install selected` or `Update selected` as appropriate.

The non-graphical installer is also straightforward::

  seamm-installer install --update control-parameters-step

will ensure both that it is installed and up-to-date.

.. _SEAMM Installer: https://molssi-seamm.github.io/installation/index.html

Example
=======
If you need required or optional parameters for you flowchart, add a `Control
Parameters` step, typically as the first step in the flowchart:

.. figure:: flowchart.png
   :width: 250px
   :align: center
   :alt: Flowchart with Control Parameters step

   Flowchart with Control Parameters step

Editing the step brings up a dialog like this, which is defining four parameters:

.. figure:: dialog.png
   :width: 800px
   :align: center
   :alt: Editing the parameters

   Creating and editing the parameters

Finally, when you run from SEAMM you have an opportunity to give different values as you
submit the job:

.. figure:: run.png
   :width: 800px
   :align: center
   :alt: Run dialog with parameters at bottom

   Run dialog with parameters at bottom

Note that the first parameters, `files`, has a type of `file`. This prompts SEAMM to add
a button to the Run dialog, which brings up a typical dialog for opening
files. The files are then automatically shipped to the JobServer when you submit the
job.

That should be enough to get started. For more detail about the functionality in this
plug-in, see the :ref:`User Guide <user-guide>`. 
