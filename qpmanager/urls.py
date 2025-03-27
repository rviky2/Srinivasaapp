from django.urls import path
from . import views

app_name = 'qpmanager'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('download/<int:pk>/', views.download_question_paper, name='download_paper'),
    path('bulk-upload/', views.bulk_upload, name='bulk_upload'),
    
    # API endpoints for cascading dropdowns
    path('api/schemes/', views.api_schemes, name='api_schemes'),
    path('api/semesters/', views.api_semesters, name='api_semesters'),
    path('api/subjects/', views.api_subjects, name='api_subjects'),
    
    # Main navigation URLs
    path('<slug:slug>/', views.department_detail, name='department_detail'),
    path('<slug:dept_slug>/<slug:scheme_slug>/', views.scheme_detail, name='scheme_detail'),
    path('<slug:dept_slug>/<slug:scheme_slug>/<slug:sem_slug>/', views.semester_detail, name='semester_detail'),
    path('<slug:dept_slug>/<slug:scheme_slug>/<slug:sem_slug>/<slug:subj_slug>/', views.subject_detail, name='subject_detail'),
] 