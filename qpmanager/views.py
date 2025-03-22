from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Department, Subject, QuestionPaper
import os

def home(request):
    """Homepage view showing all departments"""
    departments = Department.objects.annotate(subject_count=Count('subjects'))
    context = {
        'departments': departments,
        'title': 'SIT eLibrary Portal'
    }
    return render(request, 'qpmanager/home.html', context)

def department_detail(request, slug):
    """View showing subjects in a department"""
    department = get_object_or_404(Department, slug=slug)
    subjects = department.subjects.annotate(paper_count=Count('question_papers'))
    
    # Filter by semester if provided
    semester = request.GET.get('semester')
    if semester:
        subjects = subjects.filter(semester=semester)
    
    context = {
        'department': department,
        'subjects': subjects,
        'selected_semester': semester,
        'semester_choices': Subject.SEMESTER_CHOICES,
        'title': f'{department.name} - Subjects'
    }
    return render(request, 'qpmanager/department_detail.html', context)

def subject_detail(request, dept_slug, subj_slug):
    """View showing question papers for a subject"""
    department = get_object_or_404(Department, slug=dept_slug)
    subject = get_object_or_404(Subject, slug=subj_slug, department=department)
    
    # Filter by year or month if provided
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    question_papers = subject.question_papers.all()
    
    if year:
        question_papers = question_papers.filter(year=year)
    if month:
        question_papers = question_papers.filter(month=month)
    
    # Get unique years for filter
    years = subject.question_papers.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'department': department,
        'subject': subject,
        'question_papers': question_papers,
        'years': years,
        'selected_year': year,
        'selected_month': month,
        'month_choices': QuestionPaper.MONTH_CHOICES,
        'title': f'{subject.name} - Question Papers'
    }
    return render(request, 'qpmanager/subject_detail.html', context)

def download_question_paper(request, pk):
    """View to download a question paper"""
    question_paper = get_object_or_404(QuestionPaper, pk=pk)
    file_path = question_paper.file.path
    
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=question_paper.filename())
        return response
    else:
        return HttpResponse("File not found", status=404)

@login_required
def dashboard(request):
    """Admin dashboard for statistics"""
    department_count = Department.objects.count()
    subject_count = Subject.objects.count()
    question_paper_count = QuestionPaper.objects.count()
    
    context = {
        'department_count': department_count,
        'subject_count': subject_count,
        'question_paper_count': question_paper_count,
        'recent_papers': QuestionPaper.objects.order_by('-upload_date')[:5],
        'title': 'Dashboard'
    }
    return render(request, 'qpmanager/dashboard.html', context)

def search(request):
    """Search view for finding question papers, subjects, and departments"""
    query = request.GET.get('q', '')
    results = {
        'question_papers': [],
        'subjects': [],
        'departments': [],
    }
    
    if query:
        # Search in question papers
        results['question_papers'] = QuestionPaper.objects.filter(
            Q(title__icontains=query) |
            Q(subject_code__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__name__icontains=query)
        ).distinct()
        
        # Search in subjects
        results['subjects'] = Subject.objects.filter(
            Q(name__icontains=query) |
            Q(subject_code__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
        
        # Search in departments
        results['departments'] = Department.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'results': results,
        'title': f'Search Results for "{query}"' if query else 'Search'
    }
    
    return render(request, 'qpmanager/search.html', context)
