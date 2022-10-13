import tempfile
from collections import defaultdict
from datetime import date
from wsgiref.util import FileWrapper
from zipfile import ZipFile

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from explorer.exporters import CSVExporter


def generate_report_action(description=_("Generate CSV file from SQL query"),):
    def generate_report(modeladmin, request, queryset):
        results = [report for report in queryset if report.passes_blacklist()[0]]
        queries = (len(results) > 0 and _package(results)) or defaultdict(int)
        response = HttpResponse(queries["data"], content_type=queries["content_type"])
        response["Content-Disposition"] = queries["filename"]
        response["Content-Length"] = queries["length"]
        return response

    generate_report.short_description = description
    return generate_report


def _package(queries):
    is_one = len(queries) == 1
    name_root = lambda n: f"attachment; filename={n}"  # noqa
    ret = {"content_type": "text/csv" if is_one else "application/zip", "filename": is_one and name_root(f'{queries[0].title.replace(",", "")}.csv') or name_root(f"Report_{date.today()}.zip")}

    ret["data"] = (is_one and CSVExporter(queries[0]).get_output()) or _build_zip(
        queries
    )

    ret["length"] = is_one and len(ret["data"]) or ret["data"].blksize
    return ret


def _build_zip(queries):
    temp = tempfile.TemporaryFile()
    zip_file = ZipFile(temp, "w")
    for r in queries:
        zip_file.writestr(f"{r.title}.csv", CSVExporter(r).get_output() or "Error!")
    zip_file.close()
    ret = FileWrapper(temp)
    temp.seek(0)
    return ret
