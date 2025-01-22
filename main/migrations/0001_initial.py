
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DenialType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Характер отказа',
                'verbose_name_plural': 'Характеры отказов',
            },
        ),
        migrations.CreateModel(
            name='DriveAxleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель ведущего моста',
                'verbose_name_plural': 'Модели ведущего моста',
            },
        ),
        migrations.CreateModel(
            name='EngineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель двигателя',
                'verbose_name_plural': 'Модели двигателя',
            },
        ),
        migrations.CreateModel(
            name='FailureNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Узел отказа',
                'verbose_name_plural': 'Узлы отказа',
            },
        ),
        migrations.CreateModel(
            name='MaintenanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Вид ТО',
                'verbose_name_plural': 'Виды ТО',
            },
        ),
        migrations.CreateModel(
            name='RecoveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Способ восстановления',
                'verbose_name_plural': 'Способы восстановления',
            },
        ),
        migrations.CreateModel(
            name='SteeringAxleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель управляемого моста',
                'verbose_name_plural': 'Модели управляемого моста',
            },
        ),
        migrations.CreateModel(
            name='TransmissionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель трансмиссии',
                'verbose_name_plural': 'Модели трансмиссии',
            },
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель техники',
                'verbose_name_plural': 'Модели техники',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=255, verbose_name='Заводской номер машины')),
                ('engine_number', models.CharField(max_length=255, verbose_name='Заводской номер двигателя')),
                ('transmission_number', models.CharField(max_length=255, verbose_name='Заводской номер трансмиссии')),
                ('drive_axle_number', models.CharField(max_length=255, verbose_name='Заводской номер ведущего моста')),
                ('steering_axle_number', models.CharField(max_length=255, verbose_name='Заводской номер управляемого моста')),
                ('supply_agreement', models.TextField(verbose_name='Договор поставки, №, дата')),
                ('shipment_date', models.DateField(verbose_name='Дата отгрузки с завода')),
                ('consignee', models.TextField(verbose_name='Грузополучатель')),
                ('delivery_address', models.TextField(verbose_name='Адрес поставки (эксплуатации)')),
                ('equipment', models.TextField(verbose_name='Комплектация, доп. опции')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('drive_axle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.driveaxlemodel', verbose_name='Модель ведущего моста')),
                ('engine_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.enginemodel', verbose_name='Модель двигателя')),
            ],
            options={
                'verbose_name': 'Машина',
                'verbose_name_plural': 'Машины',
            },
        ),
        migrations.CreateModel(
            name='ServiceCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сервисная компания',
                'verbose_name_plural': 'Сервисные компании',
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_date', models.DateField(verbose_name='Дата проведения ТО')),
                ('operating_time', models.IntegerField(verbose_name='Наработка мото/часов')),
                ('order', models.CharField(max_length=50, verbose_name='Номер заказа наряда')),
                ('order_date', models.DateField(verbose_name='Дата заказа-наряда')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.car', verbose_name='Машина')),
                ('maintenance_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.maintenancetype', verbose_name='Вид ТО')),
                ('service_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.servicecompany', verbose_name='Сервисная компания')),
            ],
            options={
                'verbose_name': 'Техническое обслуживание (ТО)',
                'verbose_name_plural': 'Техническое обслуживание (ТО)',
                'ordering': ('maintenance_date',),
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_refusal', models.DateField(verbose_name='Дата отказа')),
                ('operating_time', models.IntegerField(verbose_name='Наработка м/час')),
                ('failure_node', models.TextField(verbose_name='Узел отказа')),
                ('used_details', models.TextField(blank=True, verbose_name='Используемые запасные части')),
                ('date_of_restoration', models.DateField(verbose_name='Дата восстановления')),
                ('equipment_downtime', models.TextField(verbose_name='Время простоя техники')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.car', verbose_name='Машина')),
                ('denial_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.denialtype', verbose_name='Характер отказа')),
                ('recovery_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.recoverymethod', verbose_name='Способ восстановления')),
                ('service_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.servicecompany', verbose_name='Сервисная компания')),
            ],
            options={
                'verbose_name': 'Рекламация',
                'verbose_name_plural': 'Рекламации',
                'ordering': ['date_of_refusal'],
            },
        ),
        migrations.AddField(
            model_name='car',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.servicecompany', verbose_name='Сервисная компания'),
        ),
        migrations.AddField(
            model_name='car',
            name='steering_axle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.steeringaxlemodel', verbose_name='Модель управляемого моста'),
        ),
        migrations.AddField(
            model_name='car',
            name='transmission_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.transmissionmodel', verbose_name='Модель трансмиссии'),
        ),
        migrations.AddField(
            model_name='car',
            name='vehicle_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vehiclemodel', verbose_name='Модель техники'),
        ),
    ]
