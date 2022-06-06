from django.contrib import admin
from .models import Document 

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'FILES' , 'upload_time' , 'Reviewer')
    list_filter = ('FILES',)
    search_fields = ('FILES' , 'upload_time')
    date_hierarchy = 'upload_time'