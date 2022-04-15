from django.contrib import admin
from .models import Institute

class InstituteAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_no', 'address')
    search_fields = ('name',)
    readonly_fields = ('id', 'slug', 'created_at')

    filter_horizontal = ()
    list_filter = ('name',)
    fieldsets = ()
    ordering = ('-created_at',)

    class Meta:
        model = Institute

admin.site.register(Institute, InstituteAdmin)
