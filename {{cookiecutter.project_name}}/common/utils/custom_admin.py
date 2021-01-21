


import csv
import datetime

from django.http import HttpResponse
from rangefilter.filter import DateRangeFilter

from common.consts import DATE


def export_to_csv(modeladmin, request, queryset):
    """
    export a table from the admin to
    """
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' f"filename={opts.verbose_name}s.csv"
    writer = csv.writer(response)
    fields = [field for field in opts._get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response


export_to_csv.short_description = 'Export to CSV'  # short description

ADMIN_DATE_FILTER = (DATE, DateRangeFilter)
