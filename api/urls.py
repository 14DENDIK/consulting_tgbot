from django.urls import path

from . import views

app_name = 'apis'

urlpatterns = [
    path('countries/', views.CountryListView.as_view(), name="country-list"),
    path('faqs/', views.FAQListView.as_view(), name="faq-list"),
    path('application/', views.ApplicationView.as_view(), name="application"),
]
