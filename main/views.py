from typing import Any
from django.shortcuts import render
from . import models, forms
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from authentication import models as auth_models


def index(request):
    return render(request, 'main/index.html')


class CarListView(FormMixin, ListView):
    model = models.Car
    template_name = 'main/index.html'
    context_object_name = 'cars'
    form_class = forms.CarSearchForm
    success_url = 'index'

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            self.object_list = models.Car.objects.filter(vin__startswith=form.cleaned_data['vin'])
        else:
            self.object_list = []

        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))


class CarCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_car'
    model = models.Car
    template_name = 'main/car/new.html'
    form_class = forms.CarCreateForm
    success_url = '/user_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vehicle_models'] = models.VehicleModel.objects.all()
        context['engine_models'] = models.EngineModel.objects.all()
        context['transmission_models'] = models.TransmissionModel.objects.all()
        context['drive_axles'] = models.DriveAxleModel.objects.all()
        context['steering_axles'] = models.SteeringAxleModel.objects.all()
        context['users'] = auth_models.CustomUser.objects.all()
        context['service_companies'] = models.ServiceCompany.objects.all()

        return context


class AdminIndexListView(PermissionRequiredMixin, ListView):
    model = models.Car
    permission_required = 'main.view_car'
    template_name = 'main/user_index.html'
    context_object_name = 'cars'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        order_by = self.request.GET.get('order_by', 'shipment_date')

        if order_by in ['vehicle_model', 'engine_model', 'transmission_model', 'drive_axle_model',
                        'steerable_axle_model', 'service_company']:
            order_by = order_by + "__name"
        if order_by in ['customer']:
            order_by = "user__username"

        context['vm'] = self.request.GET.get('vm', '---')
        context['em'] = self.request.GET.get('em', '---')
        context['tr'] = self.request.GET.get('tr', '---')
        context['dam'] = self.request.GET.get('dam', '---')
        context['sam'] = self.request.GET.get('sam', '---')

        qs = qs_filter = models.Car.objects.all()
        if context['vm'] != "---":
            filter = models.VehicleModel.objects.get(name=context['vm']).pk
            qs = qs.filter(vehicle_model=filter)
        if context['em'] != "---":
            filter = models.EngineModel.objects.get(name=context['em']).pk
            qs = qs.filter(engine_model=filter)
        if context['tr'] != "---":
            filter = models.TransmissionModel.objects.get(name=context['tr']).pk
            qs = qs.filter(transmission_model=filter)
        if context['dam'] != "---":
            filter = models.DriveAxleModel.objects.get(name=context['dam']).pk
            qs = qs.filter(drive_axle=filter)
        if context['sam'] != "---":
            filter = models.SteeringAxleModel.objects.get(name=context['sam']).pk
            qs = qs.filter(steering_axle=filter)

        filter_list = ['vehicle_model', 'engine_model', 'transmission_model', 'drive_axle', 'steering_axle']

        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(
                name='manager').exists():
            context['cars'] = qs.order_by(order_by)
            for filter in filter_list:
                context[filter] = set(qs_filter.values_list(filter + '__name', flat=True))
        elif self.request.user.groups.filter(name='service').exists():
            context['cars'] = qs.filter(service_company__user=self.request.user.pk).order_by(order_by)
            for filter in filter_list:
                context[filter] = set(
                    qs_filter.filter(service_company__user=self.request.user.pk).values_list(filter + '__name',
                                                                                             flat=True))
        elif self.request.user.groups.filter(name='customer').exists():
            context['cars'] = qs.filter(user=self.request.user.id).order_by(order_by)
            for filter in filter_list:
                context[filter] = set(
                    qs_filter.filter(user=self.request.user.id).values_list(filter + '__name', flat=True))
        else:
            context['cars'] = []

        return context


class CarDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'main.view_car'
    model = models.Car
    queryset = models.Car.objects.all()
    template_name = 'main/car/index.html'


class CarUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_car'
    model = models.Car
    queryset = models.Car.objects.all()
    form_class = forms.CarCreateForm
    template_name = 'main/car/edit.html'
    success_url = '/user_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vehicle_models'] = models.VehicleModel.objects.all()
        context['engine_models'] = models.EngineModel.objects.all()
        context['transmission_models'] = models.TransmissionModel.objects.all()
        context['drive_axles'] = models.DriveAxleModel.objects.all()
        context['steering_axles'] = models.SteeringAxleModel.objects.all()
        context['users'] = auth_models.CustomUser.objects.all()
        context['service_companies'] = models.ServiceCompany.objects.all()

        return context


class CarDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'main.delete_car'
    model = models.Car
    template_name = 'main/car/delete.html'
    success_url = '/user_index'


def lookups(request):
    return render(request, 'main/lookups/list.html')


class VehicleModelListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_vehicle_model'
    model = models.VehicleModel
    queryset = models.VehicleModel.objects.all()
    template_name = 'main/lookups/vehicle_models/list.html'
    context_object_name = 'vehicle_models'


class VehicleModelCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_vehicle_model'
    model = models.VehicleModel
    form_class = forms.VehicleModelCreateForm
    template_name = 'main/lookups/vehicle_models/new.html'
    success_url = '/lookups/vehicle_models'


class VehicleModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_vehicle_model'
    model = models.VehicleModel
    queryset = models.VehicleModel.objects.all()
    form_class = forms.VehicleModelCreateForm
    template_name = 'main/lookups/vehicle_models/edit.html'
    success_url = '/lookups/vehicle_models'
    context_object_name = 'vehicle_model'


class EngineModelListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_maintenance'
    model = models.EngineModel
    queryset = models.EngineModel.objects.all()
    template_name = 'main/lookups/engine_models/list.html'
    context_object_name = 'engine_models'


class EngineModelCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_engine_model'
    model = models.EngineModel
    form_class = forms.EngineModelCreateForm
    template_name = 'main/lookups/engine_models/new.html'
    success_url = '/lookups/engine_models'


class EngineModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_engine_model'
    model = models.EngineModel
    queryset = models.EngineModel.objects.all()
    form_class = forms.EngineModelCreateForm
    template_name = 'main/lookups/engine_models/edit.html'
    success_url = '/lookups/engine_models'
    context_object_name = 'engine_model'


class TransmissionModelListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_transmission_model'
    model = models.TransmissionModel
    queryset = models.TransmissionModel.objects.all()
    template_name = 'main/lookups/transmission_models/list.html'
    context_object_name = 'transmission_models'


class TransmissionModelCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_transmission_model'
    model = models.TransmissionModel
    form_class = forms.TransmissionModelCreateForm
    template_name = 'main/lookups/transmission_models/new.html'
    success_url = '/lookups/transmission_models'


class TransmissionModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_transmission_model'
    model = models.TransmissionModel
    queryset = models.TransmissionModel.objects.all()
    form_class = forms.TransmissionModelCreateForm
    template_name = 'main/lookups/transmission_models/edit.html'
    success_url = '/lookups/transmission_models'
    context_object_name = 'transmission_model'


class DriveAxleListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_drive_axle_model'
    model = models.DriveAxleModel
    queryset = models.DriveAxleModel.objects.all()
    template_name = 'main/lookups/drive_axles/list.html'
    context_object_name = 'drive_axles'


class DriveAxleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_drive_axle_model'
    model = models.DriveAxleModel
    form_class = forms.DriveAxleModelCreateForm
    template_name = 'main/lookups/drive_axles/new.html'
    success_url = '/lookups/drive_axles'


class DriveAxleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_drive_axle_model'
    model = models.DriveAxleModel
    queryset = models.DriveAxleModel.objects.all()
    form_class = forms.DriveAxleModelCreateForm
    template_name = 'main/lookups/drive_axles/edit.html'
    success_url = '/lookups/drive_axles'
    context_object_name = 'drive_axle'


class SteeringAxleListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_steering_axle_model'
    model = models.SteeringAxleModel
    queryset = models.SteeringAxleModel.objects.all()
    template_name = 'main/lookups/steering_axles/list.html'
    context_object_name = 'steering_axles'


class SteeringAxleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_steering_axle_model'
    model = models.SteeringAxleModel
    form_class = forms.SteeringAxleModelCreateForm
    template_name = 'main/lookups/steering_axles/new.html'
    success_url = '/lookups/steering_axles'


class SteeringAxleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_steering_axle_model'
    model = models.SteeringAxleModel
    queryset = models.SteeringAxleModel.objects.all()
    form_class = forms.SteeringAxleModelCreateForm
    template_name = 'main/lookups/steering_axles/edit.html'
    success_url = '/lookups/steering_axles'
    context_object_name = 'steering_axle'


class ServiceCompanyListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_service_company'
    model = models.ServiceCompany
    queryset = models.ServiceCompany.objects.all()
    template_name = 'main/lookups/service_companies/list.html'
    context_object_name = 'service_companies'


class ServiceCompanyCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_service_company'
    model = models.ServiceCompany
    form_class = forms.ServiceCompanyCreateForm
    template_name = 'main/lookups/service_companies/new.html'
    success_url = '/lookups/service_companies'


class ServiceCompanyUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_service_company'
    model = models.ServiceCompany
    queryset = models.ServiceCompany.objects.all()
    form_class = forms.ServiceCompanyCreateForm
    template_name = 'main/lookups/service_companies/edit.html'
    success_url = '/lookups/service_companies'
    context_object_name = 'service_company'


class MaintenanceTypeListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_maintenance_type'
    model = models.MaintenanceType
    queryset = models.MaintenanceType.objects.all()
    template_name = 'main/lookups/maintenance_types/list.html'
    context_object_name = 'maintenance_types'


class MaintenanceTypeCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_maintenance_type'
    model = models.MaintenanceType
    form_class = forms.MaintenanceTypeCreateForm
    template_name = 'main/lookups/maintenance_types/new.html'
    success_url = '/lookups/maintenance_types'


class MaintenanceTypeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_maintenance_type'
    model = models.MaintenanceType
    queryset = models.MaintenanceType.objects.all()
    form_class = forms.MaintenanceTypeCreateForm
    template_name = 'main/lookups/maintenance_types/edit.html'
    success_url = '/lookups/maintenance_types'
    context_object_name = 'maintenance_type'


class DenialTypeListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_denial_type'
    model = models.DenialType
    queryset = models.DenialType.objects.all()
    template_name = 'main/lookups/denial_types/list.html'
    context_object_name = 'denial_types'


class DenialTypeCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_denial_type'
    model = models.DenialType
    form_class = forms.DenialTypeCreateForm
    template_name = 'main/lookups/denial_types/new.html'
    success_url = '/lookups/denial_types'


class DenialTypeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_denial_type'
    model = models.DenialType
    queryset = models.DenialType.objects.all()
    form_class = forms.DenialTypeCreateForm
    template_name = 'main/lookups/denial_types/edit.html'
    success_url = '/lookups/denial_types'
    context_object_name = 'denial_type'


class RecoveryMethodListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_recovery_method'
    model = models.RecoveryMethod
    queryset = models.RecoveryMethod.objects.all()
    template_name = 'main/lookups/recovery_methods/list.html'
    context_object_name = 'recovery_methods'


class RecoveryMethodCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_recovery_method'
    model = models.RecoveryMethod
    form_class = forms.RecoveryMethodCreateForm
    template_name = 'main/lookups/recovery_methods/new.html'
    success_url = '/lookups/recovery_methods'


class RecoveryMethodUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_recovery_method'
    model = models.RecoveryMethod
    queryset = models.RecoveryMethod.objects.all()
    form_class = forms.RecoveryMethodCreateForm
    template_name = 'main/lookups/recovery_methods/edit.html'
    success_url = '/lookups/recovery_methods'
    context_object_name = 'recovery_method'


class MaintenanceListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_maintenance'
    model = models.Maintenance
    queryset = models.Maintenance.objects.all()
    template_name = 'main/maintenance/list.html'
    context_object_name = 'maintenance_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.request.GET.get('clear'):
            self.request.session.pop('order_by2', None)
            self.request.session.pop('mt', None)
            self.request.session.pop('cr', None)
            self.request.session.pop('sc', None)

        if self.request.GET.get('order_by'):
            self.request.session['order_by2'] = self.request.GET.get('order_by')

        if not 'order_by2' in self.request.session:
            self.request.session['order_by2'] = 'maintenance_date'

        order_by = self.request.session['order_by2']

        if order_by in ['maintenance_type', 'car', 'service_company']:
            order_by = order_by + "__name"

        if self.request.GET.get('mt'):
            self.request.session['mt'] = self.request.GET.get('mt')

        context['mt'] = self.request.session['mt'] if "tm" in self.request.session else '---'

        if self.request.GET.get('cr'):
            self.request.session['cr'] = self.request.GET.get('cr')

        context['cr'] = self.request.session['cr'] if "cr" in self.request.session else '---'

        if self.request.GET.get('sc'):
            self.request.session['sc'] = self.request.GET.get('sc')

        context['sc'] = self.request.session['sc'] if "sc" in self.request.session else '---'

        qs = qs_filter = models.Maintenance.objects.all()

        if "mt" in self.request.session:
            filter = models.MaintenanceType.objects.get(name=self.request.session['mt']).id
            qs = qs.filter(maintenance_type=filter)

        if "cr" in self.request.session:
            filter = models.Car.objects.get(vin=self.request.session['cr'])
            qs = qs.filter(car=filter)

        if "sc" in self.request.session:
            filter = models.ServiceCompany.objects.filter(name=self.request.session['sc'])
            if filter.exists():
                qs = qs.filter(service_company=filter.first().id)
            else:
                context['sc'] = '---'

        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(
                name='manager').exists():
            context['maintenance_type'] = set(qs_filter.values_list('maintenance_type__name', flat=True))
            context['car'] = set(qs_filter.values_list('car__vin', flat=True))
            context['service_company'] = set(qs_filter.values_list('service_company__name', flat=True))
            context['maintenance_list'] = qs.order_by(order_by)
        elif self.request.user.groups.filter(name='service').exists():
            context['maintenance_type'] = set(
                qs_filter.filter(service_company__user=self.request.user).values_list('maintenance_type__name',
                                                                                      flat=True))
            context['car'] = set(
                qs_filter.filter(service_company__user=self.request.user).values_list('car__vin', flat=True))
            context['service_company'] = set(
                qs_filter.filter(service_company__user=self.request.user).values_list('service_company__name',
                                                                                      flat=True))
            context['maintenance_list'] = qs.filter(service_company__user=self.request.user).order_by(order_by)
        elif self.request.user.groups.filter(name='customer').exists():
            context['maintenance_type'] = set(
                qs_filter.filter(car__user=self.request.user).values_list('maintenance_type__name', flat=True))
            context['car'] = set(qs_filter.filter(car__user=self.request.user).values_list('car__vin', flat=True))
            context['service_company'] = set(
                qs_filter.filter(car__user=self.request.user).values_list('service_company__name', flat=True))
            context['maintenance_list'] = qs.filter(car__user=self.request.user).order_by(order_by)
        else:
            context['maintenance_list'] = []

        return context


class MaintenanceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_maintenance'
    model = models.Maintenance
    form_class = forms.MaintenanceCreateForm
    template_name = 'main/maintenance/new.html'
    success_url = '/maintenance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_car'] = "Выберите машину"
        else:
            context['select_car'] = models.Car.objects.get(id=id)

        context['cars'] = models.Car.objects.all()
        context['maintenance_types'] = models.MaintenanceType.objects.all()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')

        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = models.Car.objects.get(id=id).service_company.pk
            kwargs['initial'] = {'service_company': service_company, 'car': id}
        return kwargs


class MaintenanceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'main.view_maintenance'
    model = models.Maintenance
    template_name = 'main/maintenance/index.html'
    context_object_name = 'maintenance'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['maintenance_type'] = models.MaintenanceType.objects.all()
        context['service_company'] = models.ServiceCompany.objects.all()

        return context


class ComplaintListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_complaint'
    model = models.Complaint
    queryset = models.Complaint.objects.all()
    template_name = 'main/complaints/list.html'
    context_object_name = 'complaints'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.request.GET.get('clear'):
            self.request.session.pop('order_by3', None)
            self.request.session.pop('fn', None)
            self.request.session.pop('rm', None)
            self.request.session.pop('sc', None)

        if self.request.GET.get('order_by'):
            self.request.session['order_by3'] = self.request.GET.get('order_by')

        if not 'order_by3' in self.request.session:
            self.request.session['order_by3'] = 'date_of_refusal'

        order_by = self.request.session['order_by3']
        if order_by in ['recovery_method', 'service_company']:
            order_by = order_by + "__name"

        if self.request.GET.get('fn'): self.request.session['fn'] = self.request.GET.get('fn')

        context['fn'] = self.request.session['fn'] if "fn" in self.request.session else '---'

        if self.request.GET.get('rm'):
            self.request.session['rm'] = self.request.GET.get('rm')

        context['rm'] = self.request.session['rm'] if "rm" in self.request.session else '---'

        if self.request.GET.get('sc'):
            self.request.session['sc'] = self.request.GET.get('sc')

        context['sc'] = self.request.session['sc'] if "sc3" in self.request.session else '---'

        qs = qs_filter = models.Complaint.objects.all()

        if "fn" in self.request.session:
            qs = qs.filter(failure_node=self.request.session['fn'])

        if "rm" in self.request.session:
            filter = models.RecoveryMethod.objects.get(name=self.request.session['rm'])
            qs = qs.filter(recovery_method=filter)

        if "sc" in self.request.session:
            # filter = models.ServiceCompany.objects.get(name=self.request.session['sc']).id
            # qs = qs.filter(service_company=filter)
            filter = models.ServiceCompany.objects.filter(name=self.request.session['sc'])
            if filter.exists():
                qs = qs.filter(service_company=filter.first().id)
            else:
                context['sc'] = '---'

        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(
                name='manager').exists():
            context['failure_node'] = set(qs_filter.values_list('failure_node', flat=True))
            context['recovery_method'] = set(qs_filter.values_list('recovery_method__name', flat=True))
            context['service_company'] = set(qs_filter.values_list('service_company__name', flat=True))
            context['complaints'] = qs.order_by(order_by)
        elif self.request.user.groups.filter(name='service').exists():
            context['failure_node'] = set(
                qs_filter.filter(service_company__user=self.request.user).values_list('failure_node', flat=True))
            context['recovery_method'] = set(
                qs_filter.filter(service_company__user=self.request.user).values_list('recovery_method__name',
                                                                                      flat=True))
            context['service_company'] = set(qs_filter.values_list('service_company__name', flat=True))
            context['complaints'] = qs.filter(service_company__user=self.request.user).order_by(order_by)
        elif self.request.user.groups.filter(name='customer').exists():
            context['failure_node'] = set(
                qs_filter.filter(car__user=self.request.user).values_list('failure_node', flat=True))
            context['recovery_method'] = set(
                qs_filter.filter(car__user=self.request.user).values_list('recovery_method__name', flat=True))
            context['service_company'] = set(qs_filter.values_list('service_company__name', flat=True))
            context['complaints'] = qs.filter(car__user=self.request.user.id).order_by(order_by)
        else:
            context['complaints'] = []

        return context


class ComplaintCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_complaint'
    model = models.Complaint
    form_class = forms.ComplaintCreateForm
    template_name = 'main/complaints/new.html'
    success_url = '/complaints'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_car'] = "Выберите машину"
        else:
            context['select_car'] = models.Car.objects.get(id=id)

        context['denial_types'] = models.DenialType.objects.all()
        context['recovery_methods'] = models.RecoveryMethod.objects.all()
        context['cars'] = models.Car.objects.all()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')
        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = models.Car.objects.get(id=id).service_company.pk
            kwargs['initial'] = {'service_company': service_company, 'car': id}
        return kwargs


class MaintenanceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_maintenance'
    model = models.Maintenance
    form_class = forms.MaintenanceCreateForm
    template_name = 'main/maintenance/edit.html'
    success_url = '/maintenance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_car'] = "Выберите машину"
        else:
            context['select_car'] = models.Car.objects.get(id=id)

        context['cars'] = models.Car.objects.all()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')

        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = models.Car.objects.get(id=id).service_company.pk
            kwargs['initial'] = {'service_company': service_company, 'car': id}
        return kwargs


class MaintenanceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'main.delete_maintenance'
    model = models.Maintenance
    template_name = 'main/maintenance/delete.html'
    success_url = '/maintenance'


class ComplaintUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_complaint'
    model = models.Complaint
    form_class = forms.ComplaintCreateForm
    template_name = 'main/complaints/edit.html'
    success_url = '/complaints'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_car'] = "Выберите машину"
        else:
            context['select_car'] = models.Car.objects.get(id=id)

        context['cars'] = models.Car.objects.all()
        context['denial_types'] = models.DenialType.objects.all()
        context['recovery_methods'] = models.RecoveryMethod.objects.all()

        return context


class ComplaintDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'main.view_complaint'
    model = models.Complaint
    template_name = 'main/complaints/index.html'
    context_object_name = 'complaint'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['service_company'] = models.ServiceCompany.objects.all()

        return context


class ComplaintDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'main.delete_complaint'
    model = models.Complaint
    template_name = 'main/complaints/delete.html'
    success_url = '/complaints'
