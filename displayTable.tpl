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
    <table>
	<thead>
    % for aField in table_head:
		<td>{{ aField }}</td>
	% end
	</thead>
	<tbody>
    for aRow in table_body:
        <tr>
        for _ in aRow:
            <td> {{ _ }} </td>
        end
		</tr
    end
			{{ table_body }}
		</pre>
	</codettbody>
    </table>
</body>
</html>
