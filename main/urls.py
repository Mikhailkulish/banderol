from django.urls import path

from .apps import MainConfig
from .views import MainView

app_name = MainConfig.name

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]
