=======
History
=======
2025.5.7: Bugfix: Error printing lists of values
   * Fixed a problem printing variables that were a list of floats.
     
2023.11.15: Improved handling of boolean options
   * Properly support using boolean options on the commandline as just a flag to
     indicate True.
     
2023.11.6: Bugfix for choices in control parameters
   * Ensuring compatibility of older flowcharts with improved handling of choices in the
     control parameters, necessitated by the Web GUI.
     
2023.10.21: Improved handling of choices
   * When editing the choices for a parameter, the entryfield now accepts the choices
     separated by spaces. If a choice has spaces or other special characters they can be
     protected with quotes or backslash in the normal fashion for shell arguments.

2023.7.10: Bugfix handling parameters with 0+ values

   * The default was not correctly handled for control parameters with 0+ arguments,
     where they need to be a list.
     
2023.1.23: Fixed issue with  parameters with '_'
------------------------------------------------

* Fixed issue with '-' and '_' in parameter/variable names

* Revamped documentation to the new MolSSI style and diátaxis layout.

* (internal) Moved from LGTM to GitHub CodeQL for code quality analysis

2022-6-6: Fixed bugs when editing parameters
--------------------------------------------

* Also added button to remove a parameter.

2022.2.9: Added 'files' to parameter types
------------------------------------------

* Added 'files' to parameter types. Needed for job submission

2021.10.13: Cleaned up the GUI
------------------------------

* Made the dialog larger

* Show all parameters

* Made appropriate comboboxes read only

2021.6.3: Update for internal change in argument parsing
--------------------------------------------------------

* Updated for the SEAMM argument parser moving to seamm_util

2021.2.9: Improved description for the installer
------------------------------------------------

* Added to the README text, and made it conform to the standard style

2020.12.4: First working release
--------------------------------

Adds functionality to SEAMM for specifying key control parameters, items such as the
structure, temperature, and pressure, and use them as command-line parameters. In the
future, we will also provide the ability to set them when submitting a flowchart from
the Python or web interfaces.

0.1 (2020-10-06)
------------------

* First release on PyPI.
