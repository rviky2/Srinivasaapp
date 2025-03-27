from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import Department, Scheme, Semester, Subject, QuestionPaper
from .forms import BulkUploadForm
import os
import zipfile
import io
import json

def home(request):
    """Homepage view showing all departments"""
    departments = Department.objects.annotate(scheme_count=Count('schemes'))
    context = {
        'departments': departments,
        'title': 'SIT eLibrary Portal'
    }
    return render(request, 'qpmanager/home.html', context)

def department_detail(request, slug):
    """View showing schemes in a department"""
    department = get_object_or_404(Department, slug=slug)
    schemes = department.schemes.annotate(semester_count=Count('semesters'))
    
    context = {
        'department': department,
        'schemes': schemes,
        'title': f'{department.name} - Schemes'
    }
    return render(request, 'qpmanager/department_detail.html', context)

def scheme_detail(request, dept_slug, scheme_slug):
    """View showing semesters in a scheme"""
    department = get_object_or_404(Department, slug=dept_slug)
    scheme = get_object_or_404(Scheme, slug=scheme_slug, department=department)
    semesters = scheme.semesters.annotate(subject_count=Count('subjects'))
    
    context = {
        'department': department,
        'scheme': scheme,
        'semesters': semesters,
        'title': f'{scheme.year} Scheme - {department.name}'
    }
    return render(request, 'qpmanager/scheme_detail.html', context)

def semester_detail(request, dept_slug, scheme_slug, sem_slug):
    """View showing subjects in a semester"""
    department = get_object_or_404(Department, slug=dept_slug)
    scheme = get_object_or_404(Scheme, slug=scheme_slug, department=department)
    semester = get_object_or_404(Semester, slug=sem_slug, scheme=scheme)
    subjects = semester.subjects.annotate(paper_count=Count('question_papers'))
    
    context = {
        'department': department,
        'scheme': scheme,
        'semester': semester,
        'subjects': subjects,
        'title': f'{semester} - Subjects'
    }
    return render(request, 'qpmanager/semester_detail.html', context)

def subject_detail(request, dept_slug, scheme_slug, sem_slug, subj_slug):
    """View showing question papers for a subject"""
    department = get_object_or_404(Department, slug=dept_slug)
    scheme = get_object_or_404(Scheme, slug=scheme_slug, department=department)
    semester = get_object_or_404(Semester, slug=sem_slug, scheme=scheme)
    subject = get_object_or_404(Subject, slug=subj_slug, semester=semester)
    
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
        'scheme': scheme,
        'semester': semester,
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
    
    # Get the storage backend being used
    storage = question_paper.file.storage
    
    try:
        # Try to use the path approach (works for local file system)
        file_path = question_paper.file.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=question_paper.filename())
            return response
    except NotImplementedError:
        # For cloud storage like Azure Blob Storage that doesn't support path
        file_content = question_paper.file.read()
        response = HttpResponse(file_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{question_paper.filename()}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error accessing file: {str(e)}", status=500)
        
    return HttpResponse("File not found", status=404)

@login_required
def dashboard(request):
    """Admin dashboard for statistics"""
    department_count = Department.objects.count()
    scheme_count = Scheme.objects.count()
    semester_count = Semester.objects.count()
    subject_count = Subject.objects.count()
    question_paper_count = QuestionPaper.objects.count()
    
    context = {
        'department_count': department_count,
        'scheme_count': scheme_count,
        'semester_count': semester_count,
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
        'semesters': [],
        'schemes': [],
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
        
        # Search in semesters
        results['semesters'] = Semester.objects.filter(
            Q(scheme__year__icontains=query)
        ).distinct()
        
        # Search in schemes
        results['schemes'] = Scheme.objects.filter(
            Q(year__icontains=query) |
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

# API views for cascading dropdowns
def api_schemes(request):
    """API view to get schemes for a department"""
    department_id = request.GET.get('department')
    if department_id:
        schemes = Scheme.objects.filter(department_id=department_id).values('id', 'year')
        return JsonResponse(list(schemes), safe=False)
    return JsonResponse([], safe=False)

def api_semesters(request):
    """API view to get semesters for a scheme"""
    scheme_id = request.GET.get('scheme')
    if scheme_id:
        semesters = Semester.objects.filter(scheme_id=scheme_id).values('id', 'number')
        return JsonResponse(list(semesters), safe=False)
    return JsonResponse([], safe=False)

def api_subjects(request):
    """API view to get subjects for a semester"""
    semester_id = request.GET.get('semester')
    if semester_id:
        subjects = Subject.objects.filter(semester_id=semester_id).values('id', 'name')
        return JsonResponse(list(subjects), safe=False)
    return JsonResponse([], safe=False)

@login_required
def bulk_upload(request):
    """View for bulk uploading question papers"""
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            zip_file = form.cleaned_data['zip_file']
            
            # Track upload stats
            success_count = 0
            error_count = 0
            error_messages = []
            
            # Process the ZIP file
            with zipfile.ZipFile(zip_file) as z:
                for pdf_name in form.pdf_files:
                    try:
                        # Extract the file
                        pdf_content = z.read(pdf_name)
                        
                        # Create the question paper object
                        title = os.path.splitext(os.path.basename(pdf_name))[0]
                        
                        question_paper = QuestionPaper(
                            title=title,
                            subject=subject,
                            subject_code=subject.subject_code,
                            year=year,
                            month=month
                        )
                        
                        # Save the file content
                        file_name = f"{title}.pdf"
                        question_paper.file.save(file_name, ContentFile(pdf_content), save=False)
                        
                        # Save the question paper
                        question_paper.save()
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        error_messages.append(f"Error processing {pdf_name}: {str(e)}")
            
            # Show success message
            if success_count > 0:
                messages.success(
                    request, 
                    f"Successfully uploaded {success_count} question papers to {subject.name}"
                )
            
            # Show error message if any
            if error_count > 0:
                messages.error(
                    request,
                    f"Failed to upload {error_count} files. See details below."
                )
                for error in error_messages:
                    messages.error(request, error)
            
            # Redirect to subject detail page
            return redirect('qpmanager:subject_detail', 
                          dept_slug=subject.semester.scheme.department.slug, 
                          scheme_slug=subject.semester.scheme.slug,
                          sem_slug=subject.semester.slug,
                          subj_slug=subject.slug)
    else:
        form = BulkUploadForm()
    
    context = {
        'form': form,
        'title': 'Bulk Upload Question Papers'
    }
    return render(request, 'qpmanager/bulk_upload.html', context)
