<!DOCTYPE html>
<html>
<head>
	<title>DBViewer | Viewing page #{{ pageNum }} of {{ tableName }}</title>
</head>
<body>
	<p>Viewing data of table: <em>{{ tableName }}</em></p>
	% if not isThisFirstPage:
		<a href="?tableName={{ tableName }}&chunkSize={{ chunkSize }}&pageNum={{ pageNum-1 }}">Previous</a>
	% end
	% if not isThisLastPage:
		<a href="?tableName={{ tableName }}&chunkSize={{ chunkSize }}&pageNum={{ pageNum+1 }}">Next</a>
	% end
	<ul>
		% for _ in table_head:
			<li>{{ _ }}</li>
		% end
	</ul>
	<code>
		<pre>
			{{ table_body }}
		</pre>
	</code>
</body>
</html>
