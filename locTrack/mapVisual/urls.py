from django.urls import path

from . import views

urlpatterns = [
    path('new-location/', views.new_location),
    path('all-locations/', views.all_locations),
    path('all-categories/', views.all_categories),
    path('child-categories/', views.child_categories),
    path('new-category/', views.new_category),
    path('remove-category/', views.remove_category),
    path('import-data-gpx/',views.import_data_gpx ),
    path('trackpoints/', views.trackpoints),
]
