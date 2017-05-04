import os
import json

PREF_FILE = "temp/runtime-cli.json"

def readPref(key=None):
	if os.path.isfile(PREF_FILE):
		with open(PREF_FILE, mode="rt") as fp:
			dicn = json.load(fp)
	else:
		dicn = dict()
	if key:
		try:    ans = dicn[key]
		except KeyError:    raise RuntimeError("Requested key {} doesn't exist".format(key))
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

def test():
	writePref(a=1, b=2)
	print(readPref("b"))
	try:    readPref("c")
	except RuntimeError:    print("Appropriate error was raised")
	writePref(c=3, d=4)
	print(readPref())
	input("Undoing any changes")
	with open(PREF_FILE, mode="wt") as fp:
		fp.write("{}")
	return

if __name__ == '__main__':
	test()
