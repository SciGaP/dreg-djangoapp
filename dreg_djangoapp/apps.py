from django.apps import AppConfig


class DregDjangoappConfig(AppConfig):
    name = 'dreg_djangoapp'
    label = 'dreg_djangoapp'
    url_prefix = "dreg"
    
    def enabled(self, request):
        # Exclude from menus
        return False
