<!DOCTYPE html>
<html>
<head>
	<title>DBViewer | Choose a table.</title>
</head>
<body>
	<form action="/displayTable">
		<select name="tableName">
		% for x in tableList:
			<option value="{{ x }}">{{ x }}</option>
		% end
		</select>
		<br>
		<select name="chunkSize">
			<option value="10">10</option>
			<option value="50">50</option>
			<option value="100">100</option>
		</select>
		<br>
		<input type="hidden" name="pageNum" value="1">
		<input type="submit">
	</form>
</body>
</html>
