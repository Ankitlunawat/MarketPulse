from django.urls import path
from tracker import views
urlpatterns = [
    path("api/products/", views.products),
    path("api/products/<int:pk>/history/", views.history),
    path("api/summary/", views.summary),
    path("api/export/", views.export),
]
