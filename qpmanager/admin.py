from django.contrib import admin
from .models import Department, Scheme, Semester, Subject, QuestionPaper

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class SchemeAdmin(admin.ModelAdmin):
    list_display = ('year', 'department', 'created_at', 'updated_at')
    list_filter = ('department',)
    prepopulated_fields = {'slug': ('year',)}
    search_fields = ('year', 'department__name')

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'number', 'scheme', 'created_at', 'updated_at')
    list_filter = ('scheme__department', 'scheme', 'number')
    prepopulated_fields = {'slug': ('number',)}
    search_fields = ('number', 'scheme__year', 'scheme__department__name')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_code', 'get_department', 'get_scheme', 'get_semester', 'created_at', 'updated_at')
    list_filter = ('semester__scheme__department', 'semester__scheme', 'semester')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'subject_code', 'semester__scheme__department__name')
    
    def get_department(self, obj):
        return obj.semester.scheme.department
    get_department.short_description = 'Department'
    get_department.admin_order_field = 'semester__scheme__department'
    
    def get_scheme(self, obj):
        return obj.semester.scheme
    get_scheme.short_description = 'Scheme'
    get_scheme.admin_order_field = 'semester__scheme'
    
    def get_semester(self, obj):
        return obj.semester
    get_semester.short_description = 'Semester'
    get_semester.admin_order_field = 'semester'

class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_code', 'subject', 'get_department', 'get_scheme', 'get_semester', 'year', 'month', 'upload_date')
    list_filter = ('subject__semester__scheme__department', 'subject__semester__scheme', 'subject__semester', 'subject', 'year', 'month')
    search_fields = ('title', 'subject_code', 'subject__name', 'subject__semester__scheme__department__name')
    date_hierarchy = 'upload_date'
    
    def get_department(self, obj):
        return obj.subject.semester.scheme.department
    get_department.short_description = 'Department'
    get_department.admin_order_field = 'subject__semester__scheme__department'
    
    def get_scheme(self, obj):
        return obj.subject.semester.scheme
    get_scheme.short_description = 'Scheme'
    get_scheme.admin_order_field = 'subject__semester__scheme'
    
    def get_semester(self, obj):
        return obj.subject.semester
    get_semester.short_description = 'Semester'
    get_semester.admin_order_field = 'subject__semester'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make subject_code field optional by setting required=False
        if 'subject_code' in form.base_fields:
            form.base_fields['subject_code'].required = False
        return form

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Scheme, SchemeAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(QuestionPaper, QuestionPaperAdmin)
