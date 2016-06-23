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
4. Clone this repository to some location in which you have file create/write access.

## Execution
Currently, the ASP Website test suite is under refurbishment.
The ASP Modules test suite is functionally complete, but lacks any sort of GUI or even CLI. 
* Currently, to customize the suite, go to lines 71-74, and add comments and change indentation, or set the specific module/locale as needed.
* To run an individual module, go to lines 105-108 and invert comments.
* Changing the browser used will require altering lines 4 and 9.

Simple command line arguments likely to be done first, along with a short .cmd file.

A dialog box with a series of buttons and/or checkboxes may follow.

##Note
When the test is running, refrain from moving the mouse pointer around the active window.

The Drag+Drop actions use emulated mouse position, and a real mouse position *will* interfere, likely breaking execution.
