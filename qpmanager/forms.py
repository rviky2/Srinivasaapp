from django import forms
from .models import Department, Scheme, Semester, Subject, QuestionPaper
import zipfile
import io
import os

class BulkUploadForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        help_text="Select the department"
    )
    scheme = forms.ModelChoiceField(
        queryset=Scheme.objects.none(),
        help_text="Select the scheme year"
    )
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.none(),
        help_text="Select the semester"
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        help_text="Select the subject for all question papers"
    )
    year = forms.IntegerField(
        help_text="Enter the year for all question papers (e.g., 2024)"
    )
    month = forms.ChoiceField(
        choices=QuestionPaper.MONTH_CHOICES,
        help_text="Select the month for all question papers"
    )
    zip_file = forms.FileField(
        help_text="Upload a ZIP file containing multiple PDF files"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If department is provided, filter schemes by department
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['scheme'].queryset = Scheme.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass
        
        # If scheme is provided, filter semesters by scheme
        if 'scheme' in self.data:
            try:
                scheme_id = int(self.data.get('scheme'))
                self.fields['semester'].queryset = Semester.objects.filter(scheme_id=scheme_id)
            except (ValueError, TypeError):
                pass
        
        # If semester is provided, filter subjects by semester
        if 'semester' in self.data:
            try:
                semester_id = int(self.data.get('semester'))
                self.fields['subject'].queryset = Subject.objects.filter(semester_id=semester_id)
            except (ValueError, TypeError):
                pass
    
    def clean_zip_file(self):
        zip_file = self.cleaned_data.get('zip_file')
        if zip_file:
            # Check if the file is a ZIP
            if not zip_file.name.endswith('.zip'):
                raise forms.ValidationError("File must be a ZIP archive.")
            
            # Check the contents of the ZIP file
            try:
                with zipfile.ZipFile(zip_file) as z:
                    # Get list of files in ZIP that are PDFs
                    pdf_files = [f for f in z.namelist() if f.lower().endswith('.pdf')]
                    
                    if not pdf_files:
                        raise forms.ValidationError("ZIP file does not contain any PDF files.")
                    
                    # Store the list of PDF files for later use
                    self.pdf_files = pdf_files
                    
                    return zip_file
            except zipfile.BadZipFile:
                raise forms.ValidationError("Invalid ZIP file.")
        return zip_file 