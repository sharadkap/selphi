# selphi
Placeholder for Python Selenium scripts

## Installation
1. Install Python.
  * Version 3.5 (32bit) was used to write this, but the 64bit edition or any 3.x version should work as well.
  * Ensure that the Python variables/directories are added to your PATH, there should be an option for that on the installer.
2. Using Command Prompt (Admin), use `pip` to install the Selenium Webdriver, Beautiful Soup, and TAP python libraries:
  * `pip install selenium`
  * `pip install tap.py`
  * `pip install beautifulsoup4`
3. Download the WebDriver application for the browser(s) you intend to use, and ensure the executable is located on your PATH.
  * For example, place it in the Scripts directory of your Python installation.
	* IE also requires that Protected Mode is set to the same value for every Security Level, set that in the Security tab in IE's Internet Options dialog. This setting has a habit of turning itself off, so be sure to check each time.
4. Clone or download this repository to some location in which you have file create/write access.

## Execution
The test suite can be executed either by double-clicking the file or via the command line:
* Both methods will begin a test run with the settings as defined in the `test.properties` file, but running from the command line will give a small progress indicator.
* Recently, Firefox has discontinued support for the old firefox driver, requiring instead the new marrionette driver. However, this new driver, it doesn't actually work. You may have to experiment with older versions of firefox or selenium to find one that does. (FF 46, selenium 2.52.0 seems to be good.)
* To customise the test suite, edit the `test.properties` file, there should be examples and explanations already in there.
The ASP Modules test suite can also be run in either mode:
* The `modulescripts.py` file contains the customisable values, rather more involved, due to the complexity of module hosting. However, the modules to test, which locales to test in, and the browsers to use are currently still command line arguments.
* To customise the suite of tests, run from the command line, (with `modules.py`) using the `-l`/`--locales`, `-m`/`--modules`, and `-b`/`--browsers` options.
* Use the `-h` option to get the list of possible values.

A dialog box with a series of buttons and/or checkboxes may follow.

## Results
### Website
When the entire test suite has finished, the results will be printed in the terminal, as well as written to a `REGR_locale_site_browser_time.tap` file, in TAP format, named with the testing settings and the time of completion. Some knowledge of the structure of the test suite and the websites' CSS design may be required to decipher it directly.

This can then be uploaded to HipTest and viewed in a more readable format by:
1. Creating a new test run, selecting the Create As Empty For The Purpose Of Uploading Results option
2. Clicking the Push Results button in the new run to open the Push Results pane
3. Executing the following javascript (formatted as a bookmarklet for convenience): `javascript:!function(){var t=$("pre").text().match(/http.+?\/tap/)[0];$(".ember-view.modal-footer").append('<form method="post" enctype="multipart/form-data" action="'+t+'"><input type="file" name="file"><input type="submit"></form>')}();` to actually add the Upload File Form, just on the off chance that you don't already have cURL installed.
4. Selecting the file to upload and clicking Submit (this will show a machine representation of the results, hit back to show the test run proper.)

### Modules
After each module is completed (or failed), the execution status (and exception message) will be appended to `module_screenshots/module_results.csv` in the folder the repository was saved to (will be created if not already existing).

In the case of a failure, a screenshot will be taken and saved as a PNG image file named after the locale, in a folder named after the module, in the `module_screenshots` folder.

The selenium exceptions don't give a huge amount of information as to what went wrong, the screenshot should aid a manual investigation.

##Note
Be sure not to have the `module_results.csv` file open during the testing, as if the file is locked, no results can be recorded.

When any module-related tests are running, refrain from moving the mouse pointer around in the active window.

The module Drag+Drop actions use mouse position, and moving the mouse around will interfere with that, likely breaking execution.

There is currently some issue wherein running either test suite unattended for a long time causes some kind of error with webdriver. It is yet unknown whether, but suspected that, this may also randomly cause some tests to be failed.
