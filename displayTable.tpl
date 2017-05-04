<!DOCTYPE html>
<html>
<head>
	<title>DBViewer | Page #{{ pageNum }} of {{ tableName }} table.</title>
	<style type="text/css">
table, th, td {
    border: 1px solid black;
}
thead {
	font-weight: bolder;
	text-align: center;
}
	</style>
</head>
<body>
	<p>Viewing data of table: <em>{{ tableName }}</em></p>
	% if not isThisFirstPage:
		<a href="?tableName={{ tableName }}&chunkSize={{ chunkSize }}&pageNum={{ pageNum-1 }}">Previous</a>
	% end
	% if not isThisLastPage:
		<a href="?tableName={{ tableName }}&chunkSize={{ chunkSize }}&pageNum={{ pageNum+1 }}">Next</a>
	% end
	<table>
	<thead>
	% for aField in table_head:
		<td>{{ aField }}</td>
	% end
	</thead>
	<tbody>
	% for aRow in table_body:
		<tr>
		% for _ in aRow:
			<td> {{ _ }} </td>
		% end
		</tr>
	% end
	</tbody>
	</table>
</body>
</html>
