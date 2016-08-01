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
### Optional: For the HipTest Publisher
1. Install Ruby
  * Version 2.2.4 was used here.
2. Using the Command Prompt (Admin), install the publisher with 
  * `gem install hiptest-publisher`

## Execution
The test suite can be executed either by double-clicking the file or via the command line:
* Running the script from Windows Explorer will begin an End To End run with a new user in GB Production using Chrome.
* Currently, Firefox is undergoing a transition to a new web driver, and so FF47 is incompatible with selenium 2.5~something for now.
* To customise the test suite, run from the command line (the cmd.exe terminal) as `selene.py` with the `-l` and/or `-t` options.
* Run as `selene.py -h` to see the full set of options available.
The ASP Modules test suite can also be run at the Command-Line:
* Opening the script from Windows Explorer, or with no arguments, will begin a test of all modules in all locales, accessing the modules within the website, using Chrome.
* To customise the suite of tests, run from the command line, (with `modules.py`) using the `-l`/`--locales` and `-m`/`--modules` options.
* Use the `-h` option to get the list of possible values.

A dialog box with a series of buttons and/or checkboxes may follow.

## Results
### Website
When the entire test suite has finished, the results will be printed in the terminal, as well as written to `REGR.tap` in TAP format, which would be human readable, were it not for the exception stacktraces returned by webdriver.

This can then be formatted and uploaded to HipTest by running `hipub.bat`, and entering the Test Run ID when propted.

### Modules
After each module is completed (or failed), the execution status (and exception message) will be appended to `module_screenshots/module_results.csv` in the folder the repository was saved to (will be created if not already existing).

In the case of a failure, a screenshot will be taken and saved as a PNG image file named after the locale, in a folder named after the module, in the `module_screenshots` folder.

The selenium exceptions don't give a huge amount of information as to what went wrong, the screenshot should aid a manual investigation.

##Note
When any module-related tests are running, refrain from moving the mouse pointer around in the active window.

The Drag+Drop actions use mouse position, and moving the mouse around will interfere with that, likely breaking execution.

There is currently some issue wherein running either test suite unattended for a long time causes some kind of error with webdriver. It is yet unknown whether, but suspected that, this may also randomly cause some tests to be failed.
