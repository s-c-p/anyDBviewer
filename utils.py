import os
import json

import pytest

PREF_FILE = "temp/runtime-cli.json"

def readPref(key=None):
	if os.path.isfile(PREF_FILE):
		with open(PREF_FILE, mode="rt") as fp:
			dicn = json.load(fp)
	else:
		dicn = dict()
	if key:
		try:
			ans = dicn[key]
		except KeyError:
			raise RuntimeError("Requested key {} doesn't exist".format(key))
	else:
		ans = dicn
	return ans

def writePref(**kwargs):
	data = readPref()
	for key, value in kwargs.items():
		data[key] = value
	with open(PREF_FILE, mode="wt") as fp:
		json.dump(data, fp)
	return 0

# ----------------------------------------------------------------------------

@pytest.fixture(scope="module")
def prefrencesFile():
	# the setup
	try:
		fp = open(PREF_FILE, mode="rt")
	except OSError:
		with open(PREF_FILE, mode="wb"):
			pass
		backup = dict()
	else:
		with fp:
			backup = json.load(fp)
		with open(PREF_FILE, mode="wt") as fp:
			fp.write(str(dict()))
	# ----------------------------------------------
	yield
	# ----------------------------------------------
	# now the tear-down
	# input("Undoing any changes")	NOTE: pytest doesn't like this
	with open(PREF_FILE, mode="wt") as fp:
		json.dump(backup, fp)
	return

def test(prefrencesFile):
	assert writePref(a=1, b=2) == 0
	assert readPref("b") == 2
	with pytest.raises(RuntimeError, message="Expecting RuntimeError for asking non-existatn key from dict"):
		readPref("c")
		# Appropriate error was raised
	assert writePref(c=3, d=4) == 0
	return
