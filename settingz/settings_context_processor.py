from .models import Settings

def get_settings(request):
    settings_data=Settings.objects.last()

    return{'settings_data':settings_data}