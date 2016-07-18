# selphi
Placeholder for Python Selenium scripts

## Installation
1. Install Python.
  * Version 3.5 (32bit) was used to write this, but the 64bit edition or any 3.x version should work as well.
  * Ensure that the Python variables are added to your PATH, there should be an option for that on the installer.
2. Using Command Prompt (Admin), use `pip` to install the Selenium Webdriver, Beautiful Soup, and TAP python libraries:
  * `pip install selenium`
  * `pip install tap.py`
  * `pip install beautifulsoup4`
3. Download the WebDriver application for the browser(s) you intend to use, and ensure the executable is located on your PATH.
  * For example, place it in the Scripts directory of your Python installation.
	* IE also requires that Protected Mode is set to the same value for every Security Level, set that in  the Security tab in IE's Internet Options dialog.
4. Clone or download this repository to some location in which you have file create/write access.

## Execution
Currently, the ASP Website test suite is under refurbishment.
The ASP Modules test suite is functionally complete, and has a rudimentary CLI:
* Opening the script from Windows Explorer will begin a test of all modules in all locales.
* To customise the suite of tests, run the script from the command line, (with `py modules.py`) using the `-l`/`--locales` and `-m`/`--modules` options.
* Use the `-h` option to get the list of possible values.
* By default, it will access the modules within the website, use the `-d`/`--direct` option to access the modules directly.
* Chrome is the default browser used, can be changed with the `-b`/`--browser` option.
	* Currently, Firefox is undergoing a transition to a new webdriver, and so FF47 is incompatible with selenium 2.5~something for now.

A dialog box with a series of buttons and/or checkboxes may follow.

## Results
After each module is completed (or failed), the execution status (and exception message) will be appended to `module_screenshots/module_results.csv` in the folder the repository was saved to (will be created if not already existing).

In the case of a failure, a screenshot will be taken and saved as a PNG image file named after the locale, in a folder named after the module, in the `module_screenshots` folder.

The selenium exceptions don't give a huge amount of information as to what went wrong, the screenshot should aid a manual investigation.

##Note
When the test is running, refrain from moving the mouse pointer around in the active window.

The Drag+Drop actions use mouse position, so moving the mouse around will interfere with that, likely breaking execution.
