<!DOCTYPE html>
<html>
<head>
	<title>Choose a table</title>
</head>
<body>
	<form action="/displayTable?pageNum=1">
		<select name="tableName">
			<option value="{{ tableList[0] }}">{{ tableList[0] }}</option>
		% for x in tableList[1:]:
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
