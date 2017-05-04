import os

import bottle

import utils
import background as bg


@bottle.route("/")
@bottle.route("/index")
def index():
	return bottle.template("view/index")

@bottle.route("/chooseTable")
def chooseTable():
	args = bottle.request.query
	filePath = args.databaseFile
	if not os.path.isfile(filePath):
		return '<h2>File "{}" not accessible.</h2>'.format(filePath)	# TODO: redirect after 5sec to index
	utils.writePref(databaseFile=filePath)
	tables = bg.sqlCommandRunner(filePath, ".tables")
	tables = tables.split()
	return bottle.template("chooseTable"
		, tableList=tables)

@bottle.route("/displayTable")
def displayTable():
	args = bottle.request.query
	pageNum = int(args.pageNum)
	tableName = args.tableName
	chunkSize = int(args.chunkSize)
	filePath = utils.readPref("databaseFile")

	col_names = bg.getColNames(filePath, tableName)

	to = chunkSize*pageNum
	frm = to - (chunkSize-1)
	data = bg.getRows(filePath, tableName, col_names, frm, to)
	isThisLastPage = True if len(data) < to-frm+1 else False
	isThisFirstPage = True if pageNum == 1 else False

	return bottle.template("displayTable"
		, tableName=tableName
		, chunkSize=chunkSize
		, pageNum=pageNum
		, table_head=col_names
		, table_body=data
		, isThisLastPage=isThisLastPage
		, isThisFirstPage=isThisFirstPage)

if __name__ == '__main__':
	bottle.run(debug=True, reloader=True)
