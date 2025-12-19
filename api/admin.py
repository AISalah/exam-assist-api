from django.contrib import admin
from .models import Profile, ExamRequest, Application

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'academic_level', 'institution')
    list_filter = ('role', 'academic_level')
    search_fields = ('user__username', 'institution')

@admin.register(ExamRequest)
class ExamRequestAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'requester', 'university', 'exam_date', 'status')
    list_filter = ('status', 'university', 'exam_date')
    search_fields = ('module_name', 'requester__username')
    ordering = ('-exam_date',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('scribe', 'exam_request', 'status', 'created_at')
    list_filter = ('status',)