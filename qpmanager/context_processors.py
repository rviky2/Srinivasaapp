from .models import Department

def global_context(request):
    """Add global context variables to all templates."""
    departments = Department.objects.all()
    
    return {
        'global_departments': departments,
    } 