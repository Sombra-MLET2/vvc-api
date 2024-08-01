import csv
import io

from starlette.responses import Response


def handle_csv_response(data, request, datasource_desc='embrapa') -> Response:

    if "text/csv" not in request.headers.get("Accept", ""):
        return data

    if not isinstance(data, list):
        data = [data]

    if not data:
        return Response(content=None, media_type="text/csv", status_code=204)

    output = io.StringIO()

    writer = csv.writer(output)
    writer.writerow(data[0].dict().keys())

    for item in data:
        row = []
        for value in item.dict().values():
            if isinstance(value, dict) and 'name' in value:
                row.append(value['name'])
            else:
                row.append(value)
        writer.writerow(row)

    csv_bytes = bytes(output.getvalue().encode("utf-8"))
    headers = {'Content-Disposition': f'inline; filename="{datasource_desc}.csv"'}

    return Response(csv_bytes, headers=headers, media_type='text/csv')
