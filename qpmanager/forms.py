from django import forms
from .models import Subject, QuestionPaper
import zipfile
import io
import os

class BulkUploadForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
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