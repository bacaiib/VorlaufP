from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kunden/', views.kunden_uebersicht, name='kunden-uebersicht'),
    path('kunde/<int:kunden_nr>/', views.kunden_detail, name='kunden-detail'),
    path('kunde/neu/', views.kunde_neu, name='kunde-neu'),
    path('vermerk/erfassen/', views.vermerk_erfassen, name='vermerk-erfassen'),
    path('kunde/data/<int:kunden_nr>/', views.get_kunde_data, name='get-kunde-data'),
    path('vermerk/', views.vermerk_uebersicht, name='vermerk-uebersicht'),
    path('vermerk/<int:gespraechs_id>/', views.vermerk_detail, name='vermerk-detail'),
    path('kunde/<int:kunden_nr>/loeschen/', views.kunde_loeschen, name='kunde-loeschen'),
    path('vermerk/<int:gespraechs_id>/loeschen/', views.vermerk_loeschen, name='vermerk-loeschen')
]