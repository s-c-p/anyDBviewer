import sys
import sqlite3
import subprocess

import utils

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

def getColNames(filePath, tableName):
	# bit.ly/2p53vG6
	# bit.ly/17NgHqj
	# bit.ly/2pwbDCP
	with sqlite3.connect(filePath) as conn:
		cur = conn.cursor()
		cur.execute("SELECT * FROM {} LIMIT 1;".format(tableName))
		# NOTE: sql injection vulnerablity, but using ? style instead
		# of {} gave sqlite3.OperationalError and webpage fails with
		# HTTP error 500
		col_names = [description_tuple[0] \
			for description_tuple in cur.description]
	return col_names

def _getSrNoField(filePath, tableName, fields):
	"""
		this function fails in case tableName="playlist_track"
		see its schema, it has 2 columns working togather as PRIMARY KEY
		now goto index page, point path to the famous "chinook.db"
		selet table "playlist_track" and chunkSize 10 and proceed
		DAYUMNN--- more than 10 results
		see-- bit.ly/2pI1Bge
		ANS-- use cur.execute, then ans = 
			[cur.fetchone for _ in range(chunkSize)]
		store the value of ans[0] & ans[-1] and use it as offset info for
		prev. and next fetch respectively
		UPDATE:
		I tried implementing the above linked page but it returns bad results
		if I pass all records (sans string/blob ones) as seen in getRows2()
		-- getting accurate pagination again comes down to knowing correct
		primary key
	"""
	# we need something like sr_no for using BETWEEN clause (which is required
	# for pagination), so we use schema's output and detect which field has
	# been declared as primary key
	# NOTE: fields = getColNames(filePath, tableName)
	schema = sqlCommandRunner(filePath, ".schema {}".format(tableName))
	schema = schema.replace(";", "\n").replace(",", "\n")                       # NOTE: in case schema is written in min form without any whitespaces
	schema = schema.splitlines()
	for aLine in schema:
		if "PRIMARY KEY" in aLine.upper():
			break
	for aField in fields:
		if aField in aLine:
			sr_no = aField
			return sr_no
	special_error_message = "Oops: a table without sr no kind of field \
		encountered i.e. no field was declared as PRIMARY KEY. This is okay,\
		see bit.ly/2pwjZdK and bit.ly/2qy3Frn"
	raise RuntimeError(special_error_message)

def getRows2(dbFile, tableName, col_names, frm, to):
	pk_field = _getSrNoField(dbFile, tableName, col_names)
	prev_record = utils.readPref("prev_record")
	SQL = "SELECT * FROM {} WHERE ".format(tableName)
	SQL+= "AND".join([col_names[i] + " > " + prev_record[i] for i in range(len(col_names))])
	SQL+= "ORDER BY " + pk_field
	SQL+= "LIMIT " + str(to-frm+1)
	with sqlite3.connect(dbFile) as conn:
		cur = conn.cursor()
		x = cur.execute("SELECT * FROM {} WHERE {} BETWEEN ? AND ?;".format(tableName, pk_field), [frm, to])
	utils.writePref(prev_record=prev_record)
	return answer

def getRows(dbFile, tableName, col_names, frm, to):
	pk_field = _getSrNoField(dbFile, tableName, col_names)
	with sqlite3.connect(dbFile) as conn:
		cur = conn.cursor()
		x = cur.execute("SELECT * FROM {} WHERE {} BETWEEN ? AND ?;".format(tableName, pk_field), [frm, to])
		data = x.fetchall()
	return data

if __name__ == '__main__':
	test()


# no reason why this should cause the highlighter to break
#
# a: lambda x=None: {key: val for key, val in (x if x is not None else [])}=42


"""
python is wrong in reporting PRIMARY KEY of "playlist_track"
properly parse the output of ".schema tableName"
	if CONSTRAIN and PRIMARY KEY occour in same line call special func
"""