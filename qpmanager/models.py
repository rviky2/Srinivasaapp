from django.db import models
from django.utils.text import slugify
import os

def question_paper_upload_path(instance, filename):
    # Upload question papers to department/subject directory
    return f'question_papers/{instance.subject.department.slug}/{instance.subject.slug}/{filename}'

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Departments'

class Subject(models.Model):
    SEMESTER_CHOICES = [
        (1, 'First Semester'),
        (2, 'Second Semester'),
        (3, 'Third Semester'),
        (4, 'Fourth Semester'),
        (5, 'Fifth Semester'),
        (6, 'Sixth Semester'),
        (7, 'Seventh Semester'),
        (8, 'Eighth Semester'),
    ]
    
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        code_display = f"[{self.subject_code}] " if self.subject_code else ""
        return f"{code_display}{self.name} - {self.department.name} (Semester {self.semester})"

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Subjects'
        unique_together = ['name', 'department']

class QuestionPaper(models.Model):
    MONTH_CHOICES = [
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('aug', 'August'),
        ('sep', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December'),
    ]
    
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='question_papers')
    subject_code = models.CharField(max_length=20, blank=True, help_text="Optional. If left blank, the subject's code will be used.")
    year = models.IntegerField()
    month = models.CharField(max_length=3, choices=MONTH_CHOICES, default='jan')
    file = models.FileField(upload_to=question_paper_upload_path)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Use the subject's code if no specific code is provided
        if not self.subject_code and self.subject and self.subject.subject_code:
            self.subject_code = self.subject.subject_code
        super().save(*args, **kwargs)
    
    def __str__(self):
        code_display = f"[{self.subject_code}] " if self.subject_code else ""
        return f"{code_display}{self.title} - {self.subject.name} ({self.get_month_display()} {self.year})"
    
    def filename(self):
        return os.path.basename(self.file.name)
    
    class Meta:
        ordering = ['-year', 'subject']
        verbose_name_plural = 'Question Papers'
