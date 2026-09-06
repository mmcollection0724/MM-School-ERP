from .models import CLASSES, Teacher

def choices(request):
    return {"classes": CLASSES, "roles": Teacher.ROLE_CHOICES}
