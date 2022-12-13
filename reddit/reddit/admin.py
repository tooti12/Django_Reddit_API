from django.apps import apps
from django.contrib import admin

app = apps.get_containing_app_config(__name__)

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
