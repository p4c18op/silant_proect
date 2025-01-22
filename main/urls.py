"""
URL configuration for silant_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarListView.as_view(), name="index"),
    path('user_index', views.AdminIndexListView.as_view(), name="user_index"),
    path('cars/new', views.CarCreateView.as_view(), name="car-create"),
    path('cars/<int:pk>', views.CarDetailView.as_view(), name="car-detail"),
    path('cars/edit/<int:pk>', views.CarUpdateView.as_view(), name="car-update"),
    path('cars/delete/<int:pk>', views.CarDeleteView.as_view(), name="car-delete"),

    path('lookups', views.lookups, name="lookups"),

    path('lookups/vehicle_models', views.VehicleModelListView.as_view(), name="vehicle-model-list"),
    path('lookups/vehicle_models/new', views.VehicleModelCreateView.as_view(), name="vehicle-model-create"),
    path('lookups/vehicle_models/edit/<int:pk>', views.VehicleModelUpdateView.as_view(), name="vehicle-model-update"),

    path('lookups/engine_models', views.EngineModelListView.as_view(), name="engine-model-list"),
    path('lookups/engine_models/new', views.EngineModelCreateView.as_view(), name="engine-model-create"),
    path('lookups/engine_models/edit/<int:pk>', views.EngineModelUpdateView.as_view(), name="engine-model-update"),

    path('lookups/transmission_models', views.TransmissionModelListView.as_view(), name="transmission-model-list"),
    path('lookups/transmission_models/new', views.TransmissionModelCreateView.as_view(), name="transmission-model-create"),
    path('lookups/transmission_models/edit/<int:pk>', views.TransmissionModelUpdateView.as_view(), name="transmission-model-update"),

    path('lookups/drive_axles', views.DriveAxleListView.as_view(), name="drive-axle-list"),
    path('lookups/drive_axles/new', views.DriveAxleCreateView.as_view(), name="drive-axle-create"),
    path('lookups/drive_axles/edit/<int:pk>', views.DriveAxleUpdateView.as_view(), name="drive-axle-update"),

    path('lookups/steering_axles', views.SteeringAxleListView.as_view(), name="steering-axle-list"),
    path('lookups/steering_axles/new', views.SteeringAxleCreateView.as_view(), name="steering-axle-create"),
    path('lookups/steering_axles/edit/<int:pk>', views.SteeringAxleUpdateView.as_view(), name="steering-axle-update"),

    path('lookups/service_companies', views.ServiceCompanyListView.as_view(), name="service-company-list"),
    path('lookups/service_companies/new', views.ServiceCompanyCreateView.as_view(), name="service-company-create"),
    path('lookups/service_companies/edit/<int:pk>', views.ServiceCompanyUpdateView.as_view(), name="service-company-update"),

    path('lookups/maintenance_types', views.MaintenanceTypeListView.as_view(), name="maintenance-type-company-list"),
    path('lookups/maintenance_types/new', views.MaintenanceTypeCreateView.as_view(), name="maintenance-type-create"),
    path('lookups/maintenance_types/edit/<int:pk>', views.MaintenanceTypeUpdateView.as_view(), name="maintenance-type-update"),

    path('lookups/denial_types', views.DenialTypeListView.as_view(), name="denial-type-company-list"),
    path('lookups/denial_types/new', views.DenialTypeCreateView.as_view(), name="denial-type-create"),
    path('lookups/denial_types/edit/<int:pk>', views.DenialTypeUpdateView.as_view(), name="denial-type-update"),

    path('lookups/recovery_methods', views.RecoveryMethodListView.as_view(), name="recovery-method-company-list"),
    path('lookups/recovery_methods/new', views.RecoveryMethodCreateView.as_view(), name="recovery-method-create"),
    path('lookups/recovery_methods/edit/<int:pk>', views.RecoveryMethodUpdateView.as_view(), name="recovery-method-update"),

    path('maintenance', views.MaintenanceListView.as_view(), name="maintenance-list"),
    path('maintenance/new', views.MaintenanceCreateView.as_view(), name="maintenance-create"),
    path('maintenance/<int:pk>', views.MaintenanceDetailView.as_view(), name="maintenance-detail"),
    path('maintenance/edit/<int:pk>', views.MaintenanceUpdateView.as_view(), name="maintenance-update"),
    path('maintenance/delete/<int:pk>', views.MaintenanceDeleteView.as_view(), name="maintenance-delete"),

    path('complaints', views.ComplaintListView.as_view(), name="complaint-list"),
    path('complaints/new', views.ComplaintCreateView.as_view(), name="complaint-create"),
    path('complaints/<int:pk>', views.ComplaintDetailView.as_view(), name="complaint-detail"),
    path('complaints/edit/<int:pk>', views.ComplaintUpdateView.as_view(), name="complaint-edit"),
    path('complaints/delete/<int:pk>', views.ComplaintDeleteView.as_view(), name="complaint-delete"),
]
