from django.conf import settings
import json


def global_settings(request):
    app_settings = {
            'API_URL': settings.API_URL
        }

    return {
        'APP_SETTINGS': json.dumps(app_settings)
    }
