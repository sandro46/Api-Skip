from django.urls import path
from skip_tools.views import *

urlpatterns = [
    path('tasks', Tasks.as_view()),
    path('search-items', SearchItems.as_view()),
    path('template', Templates.as_view()),
    path('file-package', FilePackages.as_view()),
    path('capcha-recognize', Capcha.as_view()),
]