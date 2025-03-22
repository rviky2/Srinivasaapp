from django.contrib import admin
from .models import Department, Subject, QuestionPaper

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_code', 'department', 'semester', 'created_at', 'updated_at')
    list_filter = ('department', 'semester')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'subject_code', 'department__name')

class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_code', 'subject', 'year', 'month', 'upload_date')
    list_filter = ('subject__department', 'subject__semester', 'subject', 'year', 'month')
    search_fields = ('title', 'subject_code', 'subject__name', 'subject__department__name')
    date_hierarchy = 'upload_date'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make subject_code field optional by setting required=False
        if 'subject_code' in form.base_fields:
            form.base_fields['subject_code'].required = False
        return form

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(QuestionPaper, QuestionPaperAdmin)
