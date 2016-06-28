"""Automated testing of the Modules"""
import os
import time
import argparse
from selenium.webdriver import Chrome, Firefox, Ie, Safari, Opera, Edge
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modulescripts import LANGS, LANGS_D, MODULES, MODULES_D, SCRIPTS, USERS

BROWSERS = {'chrome': Chrome, 'firefox': Firefox, 'ie': Ie, 'safari': Safari, \
'opera': Opera, 'edge': Edge}
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-m', '--modules', help='Which modules to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=MODULES.keys(), metavar='')
PARSER.add_argument('-l', '--locales', help='Which locales to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=LANGS.keys(), metavar='')
PARSER.add_argument('-b', '--browser', help='Which browser to use. One or more of [%(choices)s]. \
	Default is %(default)s', nargs=1, default='chrome', choices=BROWSERS.keys(), metavar='')
PARSER.add_argument('-d', '--direct', help=os.linesep+'Access the modules Directly.', \
	action='store_true')
PARSER.add_argument('-w', '--wait', help='Wait this many seconds before deciding \
	an element is missing. Default is %(default)s', default=15, type=int, nargs=1)
PARSER.add_argument('-tf', '--timeformat', help='The format to use for writing timestamps. \
	See https://docs.python.org/3/library/time.html#time.strftime for full formatting info. \
	Default is %(default)s', default='%Y/%m/%d %H:%M', nargs=1)
ARGS = PARSER.parse_args()

MINIWAIT = 0.5
IMPLICITLY_WAIT = ARGS.wait
TIME_FORMAT = ARGS.timeformat
DRIVER = BROWSERS[ARGS.browser]()
DRIVER.implicitly_wait(IMPLICITLY_WAIT)
DRIVER.maximize_window()
MOD_STEM_D = 'https://prod.aussiespecialist.com/content/asp/captivate/{0}_{1}/index.html'
MOD_STEM = 'https://prod.aussiespecialist.com/{0}/secure/training/training-summary/{1}.html'
SCREENSHOT_DIR = os.path.join(os.path.split(__file__)[0], 'module_screenshots')
RESULTS_FILE = os.path.join(SCREENSHOT_DIR, 'module_results.csv')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
RESET_MODULE = 'cpCmndGotoSlide=0'

def new_drag_drop(source: str, target: str):
	"""Like the ActionChains drag and drop,
	but updates the mouse position just after mousedown."""
	# Command.MOVE_TO, desite taking a css id string, does not actually perform a DOM lookup.
	def getid(loc):
		"""Interpret whether input is a locator or a series or alternate locators."""
		if isinstance(loc, str):
			return DRIVER.find_element_by_id(loc).id
		elif isinstance(loc, list):
			return pick_from_possibilities(loc).id
		else:
			raise TypeError('You broke it. String, or List only.')
	source,	target = getid(source), getid(target)
	DRIVER.execute(Command.MOVE_TO, {'element': source})
	DRIVER.execute(Command.MOUSE_DOWN, {})
	DRIVER.execute(Command.MOVE_TO, {'xoffset': int(1), 'yoffset': int(1)})
	DRIVER.execute(Command.MOVE_TO, {'element': target})
	DRIVER.execute(Command.MOUSE_UP, {})
	time.sleep(MINIWAIT)

def domo(locator):
	"""If locator is a string, clicks on the element with that as an id
	if locator is a tuple, drags the first element to the second one.
	if a list, looks for each of the elements listed, clicks the first one that exists."""
	if isinstance(locator, str):
		ele = DRIVER.find_element_by_id(locator)
		click_surely(ele)
	elif isinstance(locator, tuple):
		new_drag_drop(locator[0], locator[1])
	elif isinstance(locator, list):
		click_surely(pick_from_possibilities(locator))
	else:
		raise TypeError('You broke it. String, List, or Tuple only.')

def click_surely(ele):
	"""Click on an element. If that doesn't work, click it again.
	But off to the side a bit, in case there was a slight overlap."""
	try:
		ele.click()
	except WebDriverException as ex:
		del ex
		DRIVER.execute(Command.MOVE_TO, {'element': ele.id, \
			'xoffset': ele.size['width']/4, 'yoffset': ele.size['height']/4})
		DRIVER.execute(Command.CLICK)

def pick_from_possibilities(locator):
	"""Deal with alternate ids. Use a css selector to get any proposed elements."""
	eles = DRIVER.find_elements_by_css_selector("#" + ",#".join(locator))
	if len(eles) == 0:
		raise WebDriverException("Didn't find {0}".format(locator))
	return eles[0]

def full_languages_modules_run(langfilter=None, modfilter=None):
	"""Run the selected set of modules and locales, logging results,
	and saving a screenshot in case of failure.	By default, will run all of them."""
	if ARGS.direct:
		stem = MOD_STEM_D
		mods = MODULES_D
		langs = LANGS_D
	else:
		stem = MOD_STEM
		mods = MODULES
		langs = LANGS
	write_header_row(modfilter or mods)
	for lang in langfilter or langs.keys():
		# New line in the results.
		write_new_row(lang)
		# Logout between locales. Turns out, you can't delete PROD cookies while on WWW
		if not ARGS.direct:
			DRIVER.get(stem.split('{0}')[0])
			DRIVER.delete_all_cookies()
		for mod in modfilter or mods.keys():
			try:
				# Try to do the module
				DRIVER.get(stem.format(langs[lang], mods[mod]))
				log_in_first(lang)
				for elem in SCRIPTS[mod]:
					domo(elem)
				write_success()
			# Something goes wrong, document it and go to the next module.
			except WebDriverException as ex:
				write_failure(ex)
				draw_failure(lang, mod)
	write_footer_entry()

def log_in_first(lang):
	"""If testing with login, first, have to go and log in and everything.
	As it happens, restarting the module will also fix the Loading Forever bug."""
	if not ARGS.direct:
		DRIVER.implicitly_wait(MINIWAIT)
		if len(DRIVER.find_elements_by_id('link-logout')) == 0:
			DRIVER.find_element_by_css_selector('.link-signin-text').click()
			DRIVER.find_element_by_id('j_username').send_keys(USERS[lang])
			DRIVER.find_element_by_css_selector('[name="j_password"]').send_keys('Welcome1')
			DRIVER.find_element_by_id('usersignin').click()
		DRIVER.implicitly_wait(IMPLICITLY_WAIT)
		iframe = DRIVER.find_element_by_css_selector('iframe[src^="/content/"]')
		DRIVER.switch_to.frame(iframe)
	# Make sure the module is loaded first. Harder than it looks.
	# First, make sure that something is in the DOM,
	check = DRIVER.find_element_by_css_selector('[id^="Text_Caption_"]')
	# Then, wait until it is actually drawn to the screen.
	WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT)\
		.until(EC.visibility_of(check))
	# Then, wait until the loading overlay is gone.
	WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT)\
		.until_not(EC.visibility_of_element_located((By.ID, 'preloaderImage')))
	# THEN, you can run the script that compensates for the loading screen breaking.
	# Or a module being previously completed.
	DRIVER.execute_script(RESET_MODULE)

def get_time():
	"""Get the time, and formatted as well."""
	return time.strftime(TIME_FORMAT)

def write_header_row(mods):
	"""Adds the header row to the output file. Columns are for mods."""
	with open(RESULTS_FILE, mode='a') as log:
		log.write('"START: {0}",'.format(get_time()))	# Header corner.
		log.write(','.join(mods).upper())

def write_new_row(lang):
	"""Adds a new line to the csv output file. Lines are for langs."""
	with open(RESULTS_FILE, mode='a') as log:
		log.write('\n' + lang.upper())

def write_success():
	"""Writes a successful outcome to the results."""
	with open(RESULTS_FILE, mode='a') as log:
		log.write(',"{0}: PASS"'.format(get_time()))

def write_failure(ex):
	"""Writes a failed outcome to the results."""
	with open(RESULTS_FILE, mode='a') as log:
		log.write(',"{0}: FAIL: {1}"'.format(get_time(), ex.msg.replace('"', '""')))

def write_footer_entry():
	"""Adds a bunch of newlines to the end of the file. Easier to read multiple runs."""
	with open(RESULTS_FILE, mode='a') as log:
		log.write('\n"FINISH: {0}"\n\n'.format(get_time()))

def draw_failure(lang, mod):
	"""Take a screenshot, save it to the screenshot folder."""
	dirname = os.path.join(SCREENSHOT_DIR, mod)
	filename = dirname + r"\{}.png".format(lang.split('/')[0])
	os.makedirs(dirname, exist_ok=True)
	imgdata = DRIVER.get_screenshot_as_png()
	with open(filename, mode='wb') as fil:
		fil.write(imgdata)

full_languages_modules_run(modfilter=ARGS.modules, langfilter=ARGS.locales)

# Do remember to do this.
DRIVER.quit()

raise EOFError("This is the end of the file.")
