from django.urls import path
from .import views


urlpatterns = [
#display
    path('', views.main),
    path('dashboard', views.dashboard),
    path('new', views.new),
    path('trips/<int:trip_id>', views.trip_info),
    path('trips/edit/<int:trip_id>', views.edit),



    #action
    path('register', views.register),
    path('login', views.login),
    path('trip/create', views.create),
    path('trips/destroy/<int:trip_id>', views.delete),
    path('trips/edit/<int:trip_id>/update', views.update),
    path('logout', views.logout),




    #wipe all data
    path('wipeDB', views.wipeDB),
]