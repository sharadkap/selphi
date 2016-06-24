"""Test file, seeing how well the Modules can be done."""
import os
import time
import argparse
from selenium.webdriver import Chrome, Firefox, Ie, Safari, Opera, Edge
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriverException
from modulescripts import LANGS, LANGS_D, MODULES, MODULES_D, SCRIPTS

BROWSERS = {'chrome': Chrome, 'firefox': Firefox, 'ie': Ie, 'safari': Safari, \
'opera': Opera, 'edge': Edge}
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-m', '--modules', help='Which modules to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=MODULES.keys(), metavar='')
PARSER.add_argument('-l', '--locales', help='Which locales to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=LANGS.keys(), metavar='')
PARSER.add_argument('-b', '--browser', help='Which browser to use. One or more of [%(choices)s]. \
	Default is %(default)s', nargs=1, default='chrome', choices=BROWSERS.keys(), metavar='')
PARSER.add_argument('-d', '--direct', help=os.linesep+'Access the modules Directly.', action='store_true')
ARGS = PARSER.parse_args()

DRIVER = BROWSERS[ARGS.browser[0]]()
DRIVER.implicitly_wait(30)
DRIVER.maximize_window()
MINIWAIT = 0.5
MOD_STEM_D = 'https://prod.aussiespecialist.com/content/asp/captivate/{0}_{1}/index.html'
MOD_STEM = 'https://prod.aussiespecialist.com/{0}/secure/training/training-summary/{1}.html'
SCREENSHOT_DIR = os.path.join(os.path.split(__file__)[0], 'module_screenshots')
RESULTS_FILE = os.path.join(SCREENSHOT_DIR, 'module_results.txt')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
CHECK_LOADED = '''x=function(){var n=window.$&&$("iframe[src^='/content/']")[0],
				t=n&&n.contentWindow&&n.contentWindow.$("#ScormContent")[0];
				return t&&t.contentWindow||n&&n.contentWindow||window}();
				return Number(x.cpInfoCurrentSlide) === Number(x.cpInfoSlideCount);'''

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
	for mod in modfilter or mods.keys():
		for lang in langfilter or langs.keys():
			froze = True	# Not really, but how else to get into the while?
			while froze:
				froze = False
				try:
					DRIVER.get(stem.format(langs[lang], mods[mod]))
					for elem in SCRIPTS[mod]:
						domo(elem)
					with open(RESULTS_FILE, mode='a') as log:
						log.write('{2}: Module {0} in locale {1} passed without issue.\n'\
							.format(mod, lang, time.asctime()))
				except WebDriverException as ex:
					# First, check if that was just the Loading Screen.
					if DRIVER.execute_script(CHECK_LOADED):
						DRIVER.refresh()
						froze = True
						continue	# Bit of a mess, but how else to 'redo' a For Iteration Step.
					with open(RESULTS_FILE, mode='a') as log:
						log.write('\n{3}: Module {0} in Locale {1} failed because "{2}".\n'\
							.format(mod, lang, ex.msg, time.asctime()))
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
