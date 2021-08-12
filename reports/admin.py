from django.contrib import admin
from .models import Report


# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'TRIP_ID', 'device', 'driver', 'firm', 'vehicle', 'STARTEDT', 'STARTADDRESS', 'STARTODO', 'ENDEDT',
        'ENDADDRESS', 'ENDODO')
    search_fields = ['firm__company_name', 'driver__first_name', 'vehicle__make', 'TRIP_ID']
    list_filter = ('firm', 'driver', 'vehicle', 'device')


admin.site.register(Report, ReportAdmin)
