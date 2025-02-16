from django.urls import include, path
from . import views

urlpatterns = []

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]

urlpatterns = [
    path('', views.index, name='index'),
]