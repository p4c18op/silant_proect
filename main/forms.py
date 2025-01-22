from django import forms
from . import models


class CarSearchForm(forms.Form):
    vin = forms.CharField(max_length=10)


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = '__all__'


class VehicleModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.VehicleModel
        fields = '__all__'


class EngineModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.EngineModel
        fields = '__all__'


class TransmissionModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.TransmissionModel
        fields = '__all__'


class DriveAxleModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.DriveAxleModel
        fields = '__all__'


class SteeringAxleModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.SteeringAxleModel
        fields = '__all__'


class ServiceCompanyCreateForm(forms.ModelForm):
    class Meta:
        model = models.ServiceCompany
        fields = '__all__'


class MaintenanceTypeCreateForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceType
        fields = '__all__'


class DenialTypeCreateForm(forms.ModelForm):
    class Meta:
        model = models.DenialType
        fields = '__all__'


class RecoveryMethodCreateForm(forms.ModelForm):
    class Meta:
        model = models.RecoveryMethod
        fields = '__all__'


class MaintenanceCreateForm(forms.ModelForm):
    class Meta:
        model = models.Maintenance
        fields = '__all__'
        widgets = {
            'order': forms.Textarea(attrs={'rows': 1}),
            'maintenance_date': forms.NumberInput(attrs={'type': 'date'}),
            'order_date': forms.NumberInput(attrs={'type': 'date'}),
            'car': forms.HiddenInput(),
            'service_company': forms.HiddenInput(),
        }


class ComplaintCreateForm(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = '__all__'
        widgets = {
            'date_of_refusal': forms.NumberInput(attrs={'type': 'date'}),
            'failure_node': forms.Textarea(attrs={'rows': 1}),
            'parts_used': forms.Textarea(attrs={'rows': 1}),
            'date_of_restoration': forms.NumberInput(attrs={'type': 'date'}),
            'equipment_downtime': forms.Textarea(attrs={'rows': 1}),
            'car': forms.HiddenInput(),
            'service_company': forms.HiddenInput(),
        }


class MaintenanceUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Maintenance
        fields = '__all__'
        widgets = {
            'order': forms.Textarea(attrs={'rows': 1}),
            'maintenance_date': forms.NumberInput(attrs={'type': 'date'}),
            'order_date': forms.NumberInput(attrs={'type': 'date'}),
            'car': forms.HiddenInput(),
            'service_company': forms.HiddenInput(),
        }
