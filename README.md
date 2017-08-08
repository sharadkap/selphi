# selphi
Placeholder for Python Selenium scripts

## Installation
1. Install Python.
  * Version 3.5 (32bit) was used to write this, but the 64bit edition or any 3.x version should work as well.
  * Ensure that the Python variables/directories are added to your PATH, there should be an option for that on the installer.
  * It may also be convenient to set up the application handler, set the default Open With action for `.py` files to be Python, rather than Notepad/IDLE.
2. Using Command Prompt (Admin), use `pip` to install the Selenium Webdriver, Beautiful Soup, and TAP python libraries:
  * `pip install selenium`
  * `pip install tap.py`
  * `pip install beautifulsoup4`
3. Download the WebDriver application for the browser(s) you intend to use, and ensure the executable is located on your PATH.
  * For example, place it in the Scripts directory of your Python installation.
  * IE also requires that Protected Mode is set to the same value for every Security Level, set that in the Security tab in IE's Internet Options dialog. This setting has a habit of turning itself off, so be sure to check each time.
4. Clone or download this repository to some location in which you have file create/write access.

## Execution
The test suite can be executed in two main ways: by running the `fenester.py` file, or by running the `selene.py` file.
* The latter method will begin a test run with the settings as defined in the `test.properties` file.
  * To customise the test suite, edit the `test.properties` file, there should be examples and explanations already in there.
* The former method will open up a dialog prepopulated with the `test.properties` settings, which can then be further modified in a more(maybe) user-friendly manner.
  * Changes made in this window will not be saved to the properties file, you will still have to edit that to set the default values.

The ASP Modules test suite can currently only be run via the `modules.py` file, and even then, via the command line:
* The `modulescripts.py` file contains the customisable values, rather more involved, due to the complexity of module hosting. However, the modules to test, which locales to test in, and the browsers to use are currently still command line arguments.
* To customise the suite of tests, run from the command line, (with `modules.py`) using the `-l`/`--locales`, `-m`/`--modules`, and `-b`/`--browsers` options.
* Use the `-h` option to get the list of possible values.

## Results
### Website
When the entire test suite has finished, the results will be written to a `REGR_locale_site_browser_time.txt` file, named with the testing settings and the time of completion. Some knowledge of the structure of the test suite and the websites' CSS design may be required to decipher it directly.
Additionally, if the testing was run via the dialog window, the results will be displayed in a collapsing-tree-view panel to the right of the test options.

### Modules
After each module is completed (or failed), the execution status (and exception message) will be appended to `module_screenshots/module_results.csv` in the folder the repository was saved to (will be created if not already existing).

In the case of a failure, a screenshot will be taken and saved as a PNG image file named after the locale, in a folder named after the module, in the `module_screenshots` folder.

The selenium exceptions don't give a huge amount of information as to what went wrong, the screenshot should aid a manual investigation.

##Note
Be sure not to have the `module_results.csv` file open during the testing; if the file is locked, no results can be recorded.

When any module-related tests are running, refrain from moving the mouse pointer around in the active window.

The module Drag+Drop actions use mouse position, and moving the mouse around will interfere with that, likely breaking execution.
