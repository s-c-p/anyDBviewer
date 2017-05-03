import sys
import sqlite3
import subprocess
from collections import namedtuple

class SQLError(Exception):
	def __init__(self, err=""):
		self.err = err
		return
	def __str__(self):
		ans = "\t"
		ans+= str(self.err, "CP437").replace("\r\n", "\t\r\n")
		return ans

def sqlCommandRunner(dbFile, command):
	cmnd_skel = r'sqlite -ascii "%s" "{}"' % dbFile
	x = subprocess.run\
		( cmnd_skel.format(command)
		, stdout=subprocess.PIPE
		, stderr=subprocess.PIPE)
	if x.stderr:
		print("Error in SQL dot command")
		raise SQLError(x.stderr)
	ans = str(x.stdout, "CP437")
	return ans

def test():
	dotCommandRunner("chinook.db", ".tables")
	try:	dotCommandRunner("chinook.db", ".tabul")
	except SQLError as e:
		if e:	print("Appropriate error was raised")
	return

def _getColNames(filePath, tableName):
	# bit.ly/2p53vG6
	# bit.ly/17NgHqj
	# bit.ly/2pwbDCP
	with sqlite3.connect(filePath) as conn:
		cur = conn.cursor()
		cur.execute("SELECT * FROM {} LIMIT 1;".format(tableName))				# NOTE: sql injection vulnerablity, but using ? style instead of {} gave sqlite3.OperationalError
		col_names = [description_tuple[0] \
			for description_tuple in cur.description]
	return col_names

def _getSrNoField(filePath, tableName, fields):
	# we need something like sr_no for using BETWEEN clause (which is required
	# for pagination. so we use schema's output and detect which field has
	# been declared as primary key
	# NOTE: fields = _getColNames(filePath, tableName)
	schema = sqlCommandRunner(filePath, ".schema {}".format(tableName))
	schema = schema.replace(";", "\n").replace(",", "\n")						# NOTE: in case schema is written in min form without any whitespaces
	schema = schema.splitlines()
	for aLine in schema:
		if "PRIMARY KEY" in aLine.upper():
			break
	for aField in fields:
		if aField in aLine:
			sr_no = aField
			return sr_no
	special_error_message = "Fucksi: a table without sr no kind of field \
		encountered i.e. no field was declared as PRIMARY KEY. This is okay,\
		see bit.ly/2pwjZdK and bit.ly/2qy3Frn"
	raise RuntimeError(special_error_message)

if __name__ == '__main__':
	test()


# no reason why this should cause the highlighter to break
#
# a: lambda x=None: {key: val for key, val in (x if x is not None else [])}=42