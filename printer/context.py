from .models import Settings


def add_to_context(request):
    settings = Settings.objects.get(id=1)
    return { 'app_title': settings.app_title }