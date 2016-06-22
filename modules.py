"""Test file, seeing how well the Modules can be done."""
import os
import time
from selenium.webdriver import Chrome
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriverException
from modulescripts import LANGS, MODULES, SCRIPTS

DRIVER = Chrome()
DRIVER.implicitly_wait(30)
DRIVER.maximize_window()
MINIWAIT = 0.5
MOD_STEM = 'https://prod.aussiespecialist.com/content/asp/captivate/{0}_{1}/index.html'
SCREENSHOT_DIR = os.path.split(__file__)[0]
RESULTS_FILE = os.path.join(SCREENSHOT_DIR, 'module_results.txt')

def new_drag_drop(source: str, target: str):
	"""Like the ActionChains drag and drop,
	but updates the mouse position just after mousedown."""
	# Command.MOVE_TO, desite taking a css id string, does not actually perform a DOM lookup.
	def getid(lo):
		"""Interpret whether input is a locator or a series or alternate locators."""
		if isinstance(lo, str):
			return DRIVER.find_element_by_id(lo).id
		elif isinstance(lo, list):
			return pick_from_possibilities(lo).id
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

def full_languages_modules_run():
	"""Run all of the modules in all of the locales.
	Might take a while, might not even work."""
	# for mod in MODULES:
	mod = MODULES[11]
	for lang in LANGS:
	# lang = LANGS[12]
		froze = True	# Not really, but how else to get into the while?
		while froze:
			froze = False
			try:
				DRIVER.get(MOD_STEM.format(lang, mod))
				for elem in SCRIPTS[mod]:
					domo(elem)
				with open(RESULTS_FILE, mode='a') as log:
					log.write('{2}: Module {0} in locale {1} passed without issue.'\
						.format(mod, lang, time.asctime()))
			except WebDriverException as ex:
				# First, check if that was just the Loading Screen.
				checkload = '''x=function(){var n=window.$&&$("iframe[src^='/content/']")[0],
							t=n&&n.contentWindow&&n.contentWindow.$("#ScormContent")[0];
							return t&&t.contentWindow||n&&n.contentWindow||window}();
							return Number(x.cpInfoCurrentSlide) === Number(x.cpInfoSlideCount);'''
				if DRIVER.execute_script(checkload):
					DRIVER.refresh()
					froze = True
					continue	# Bit of a mess, but how else to 'redo' a For Iteration Step.
				with open(RESULTS_FILE, mode='a') as log:
					log.write('{3}: Module {0} in Locale {1} failed because "{2}".'\
						.format(mod, lang, ex.msg, time.asctime()))
				dirname = os.path.join(SCREENSHOT_DIR, mod)
				filename = dirname + r"\{}.png".format(lang.split('/')[0])
				os.makedirs(dirname, exist_ok=True)
				imgdata = DRIVER.get_screenshot_as_png()
				with open(filename, mode='wb') as fil:
					fil.write(imgdata)

full_languages_modules_run()
# DRIVER.get(MOD_STEM.format(LANGS[5], MODULES[11]))
# for el in SCRIPTS[MODULES[11]]:
# 	domo(el)

# Do remember to do this.
DRIVER.quit()

raise EOFError("Seems about right.")
