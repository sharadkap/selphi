# selphi
Placeholder for Python Selenium scripts

## Installation
1. Install Python.
  * Version 3.5 (32bit) was used to write this, but the 64bit edition or any 3.x version should work as well.
  * Ensure that the Python variables are added to your PATH, there should be an option for that on the installer.
2. Using Command Prompt (Admin), use `pip` to install the Selenium Webdriver and TAP python libraries:
  * `pip install selenium`
  * `pip install tap.py`
3. Download the WebDriver application for the browser(s) you intend to use, and ensure the executable is located on your PATH.
  * For example, place it in the Scripts directory of your Python installation.
	* IE also requires that Protected Mode is set to the same value for every Security Level, set that in  the Security tab in IE's Internet Options dialog.
4. Clone or download this repository to some location in which you have file create/write access.

## Execution
Currently, the ASP Website test suite is under refurbishment.
The ASP Modules test suite is functionally complete, and has a rudimentary CLI:
* Opening the script from Windows Explorer will begin a test of all modules in all locales.
* To customise the suite of tests to run, run the script from the command line, using the `-l`/`--locales` and `-m`/`--modules` options, use the `-h` option to get specific values.
* By default, will access the modules within the website, use the `-d`/`--direct` option to access the modules directly.
* Chrome is the default browser used, can be changed with the `-b`/`--browser` option.
	* Currently, Firefox is undergoing a transition to a new webdriver, and so FF47 is incompatible with selenium 2.5~something for now.

A dialog box with a series of buttons and/or checkboxes may follow.

##Note
When the test is running, refrain from moving the mouse pointer around in the active window.

The Drag+Drop actions use mouse position, so moving the mouse around will interfere with that, likely breaking execution.

Don't mind that EOFError, it's a workaround for the debugger.
