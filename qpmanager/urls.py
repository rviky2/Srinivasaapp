from django.urls import path
from . import views

app_name = 'qpmanager'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('download/<int:pk>/', views.download_question_paper, name='download_paper'),
    path('<slug:slug>/', views.department_detail, name='department_detail'),
    path('<slug:dept_slug>/<slug:subj_slug>/', views.subject_detail, name='subject_detail'),
] 