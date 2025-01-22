import os
from django.core.management.base import BaseCommand
from ...models import DenialType, RecoveryMethod, Complaint, Maintenance, MaintenanceType, Car, VehicleModel, EngineModel, TransmissionModel, DriveAxleModel, SteeringAxleModel, ServiceCompany
from authentication.models import CustomUser

class Command(BaseCommand):
    help = 'Заполняет базу данных начальными данными из .txt файла'

    def handle(self, *args, **kwargs):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory + '/main/management/commands/', 'cars_lookups.txt')
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR('Файл не найден'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            line_index = 1
            for line in lines:
                parts = line.strip().split('**')

                if len(parts) != 16:
                    self.stdout.write(self.style.ERROR(f'Некорректное количество полей в строке: {line.strip()}'))
                    continue

                vehicle_model_name = parts[0]
                engine_model_name = parts[1]
                transmission_model_name = parts[2]
                drive_axle_model_name = parts[3]
                steering_axle_model_name = parts[4]
                service_company_name = parts[5]
                user_name = parts[6]

                vin = parts[7]
                engine_number = parts[8]
                transmission_number = parts[9]
                drive_axle_number = parts[10]
                steering_axle_number = parts[11]
                supply_agreement = 'test'
                shipment_date = parts[12]
                consignee = parts[13]
                delivery_address = parts[14]
                equipment = parts[15]

                vehicle_model, _ = VehicleModel.objects.get_or_create(name=vehicle_model_name, description='Описание из справочника')
                engine_model, _ = EngineModel.objects.get_or_create(name=engine_model_name, description='Описание из справочника')
                transmission_model, _ = TransmissionModel.objects.get_or_create(name=transmission_model_name, description='Описание из справочника')
                drive_axle_model, _ = DriveAxleModel.objects.get_or_create(name=drive_axle_model_name, description='Описание из справочника')
                steering_axle_model, _ = SteeringAxleModel.objects.get_or_create(name=steering_axle_model_name, description='Описание из справочника')

                user, _ = CustomUser.objects.get_or_create(
                    username='user%d'%line_index,
                    first_name=user_name,
                    last_name="",
                )

                service_company, _ = ServiceCompany.objects.get_or_create(name=service_company_name, description='Описание из справочника', user=user)

                car, _ = Car.objects.get_or_create(
                    vin=vin,
                    engine_number=engine_number,
                    transmission_number=transmission_number,
                    drive_axle_number=drive_axle_number,
                    steering_axle_number=steering_axle_number,
                    supply_agreement=supply_agreement,
                    shipment_date=shipment_date,
                    consignee=consignee,
                    delivery_address=delivery_address,
                    equipment=equipment,
                    user=user,
                    service_company=service_company,
                    vehicle_model=vehicle_model,
                    engine_model=engine_model,
                    transmission_model=transmission_model,
                    drive_axle=drive_axle_model,
                    steering_axle=steering_axle_model,
                )

                self.stdout.write(self.style.SUCCESS(f'Создана запись: {vehicle_model_name}, {engine_model_name}, {transmission_model_name}, {drive_axle_model_name}, {steering_axle_model_name}, {service_company_name}'))

                line_index += 1

        current_directory = os.getcwd()
        file_path = os.path.join(current_directory + '/main/management/commands/', 'maintenance.txt')
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR('Файл не найден'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            line_index = 1
            for line in lines:
                parts = line.strip().split('**')

                if len(parts) != 7:
                    self.stdout.write(self.style.ERROR(f'Некорректное количество полей в строке: {line.strip()}'))
                    continue

                vin = parts[0]
                maintenance_type = parts[1]
                maintenance_date = parts[2]
                operating_time = parts[3]
                order = parts[4]
                order_date = parts[5]
                service_company = parts[6]

                maintenance_type_object, _ = MaintenanceType.objects.get_or_create(
                    name=maintenance_type,
                    description="Описание из справочника",
                )

                service_company_object = ServiceCompany.objects.filter(name=service_company).first()
                if service_company_object == None:
                    service_company_object = ServiceCompany.objects.create(name=service_company, user=None)

                maintenance, _ = Maintenance.objects.get_or_create(
                    car=Car.objects.get(vin=vin),
                    maintenance_type=maintenance_type_object,
                    maintenance_date=maintenance_date,
                    operating_time=operating_time,
                    order=order,
                    order_date=order_date,
                    service_company=service_company_object,
                )

        current_directory = os.getcwd()
        file_path = os.path.join(current_directory + '/main/management/commands/', 'complaint.txt')
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR('Файл не найден'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            line_index = 1
            for line in lines:
                parts = line.strip().split('**')

                if len(parts) != 9:
                    self.stdout.write(self.style.ERROR(f'Некорректное количество полей в строке: {line.strip()}'))
                    continue

                vin = parts[0]
                date_of_refusal = parts[1]
                operating_time = parts[2]
                failure_node = parts[3]
                denial_type = parts[4]
                recovery_method = parts[5]
                used_details = parts[6]
                date_of_restoration = parts[7]
                equipment_downtime = parts[8]

                denial_type_object, _ = DenialType.objects.get_or_create(name=denial_type)
                recovery_method_object, _ = RecoveryMethod.objects.get_or_create(name=recovery_method)

                complaint, _ = Complaint.objects.get_or_create(
                    car=Car.objects.get(vin=vin),
                    date_of_refusal=date_of_refusal,
                    operating_time=operating_time,
                    failure_node=failure_node,
                    denial_type=denial_type_object,
                    recovery_method=recovery_method_object,
                    used_details=used_details,
                    date_of_restoration=date_of_restoration,
                    equipment_downtime=equipment_downtime,
                )


        self.stdout.write(self.style.SUCCESS('База данных заполнена данными из файла'))
