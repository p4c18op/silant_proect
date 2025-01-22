from django.contrib import admin
from . import models


admin.site.register(models.Car)
admin.site.register(models.Complaint)
admin.site.register(models.DriveAxleModel)
admin.site.register(models.EngineModel)
admin.site.register(models.FailureNode)
admin.site.register(models.Maintenance)
admin.site.register(models.MaintenanceType)
admin.site.register(models.RecoveryMethod)
admin.site.register(models.ServiceCompany)
admin.site.register(models.SteeringAxleModel)
admin.site.register(models.TransmissionModel)
admin.site.register(models.VehicleModel)
