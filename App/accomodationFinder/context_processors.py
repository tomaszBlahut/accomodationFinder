from django.conf import settings
import json


def global_settings(request):
    app_settings = {
            'API_URL': settings.API_URL,
            'initialLatLng': {
                'lat': 50.049683,
                'lng': 19.944544
            },
            'initialRadius': 10000,
            'initialMeshDensity': 50,
            'resultCheckInterval': 5 * 1000
        }

    return {
        'APP_SETTINGS': json.dumps(app_settings)
    }
