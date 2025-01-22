from django.db import models
from authentication import models as auth_models

"""Модель техники"""


class VehicleModel(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"


"""Модель двигателя"""


class EngineModel(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Модель двигателя"
        verbose_name_plural = "Модели двигателя"


"""Модель трансмиссии"""


class TransmissionModel(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Модель трансмиссии"
        verbose_name_plural = "Модели трансмиссии"


"""Модель ведущего моста"""


class DriveAxleModel(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Модель ведущего моста"
        verbose_name_plural = "Модели ведущего моста"


"""Модель управляемого моста"""


class SteeringAxleModel(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Модель управляемого моста"
        verbose_name_plural = "Модели управляемого моста"


"""Сервисная компания"""


class ServiceCompany(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    user = models.OneToOneField(auth_models.CustomUser, on_delete=models.SET_NULL, verbose_name='Пользователь',
                                null=True)

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Сервисная компания"
        verbose_name_plural = "Сервисные компании"


"""Узел отказа"""


class FailureNode(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Узел отказа"
        verbose_name_plural = "Узлы отказа"


"""Способ восстановления"""


class RecoveryMethod(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Способ восстановления"
        verbose_name_plural = "Способы восстановления"


"""Вид ТО"""


class MaintenanceType(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Вид ТО"
        verbose_name_plural = "Виды ТО"


"""Машина"""


class Car(models.Model):
    vin = models.CharField("Заводской номер машины", max_length=255)

    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name="Модель техники")

    engine_model = models.ForeignKey(EngineModel, on_delete=models.CASCADE, verbose_name="Модель двигателя")

    engine_number = models.CharField("Заводской номер двигателя", max_length=255)

    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.CASCADE,
                                           verbose_name="Модель трансмиссии")

    transmission_number = models.CharField("Заводской номер трансмиссии", max_length=255)

    drive_axle = models.ForeignKey(DriveAxleModel, on_delete=models.CASCADE, verbose_name="Модель ведущего моста")

    drive_axle_number = models.CharField("Заводской номер ведущего моста", max_length=255)

    steering_axle = models.ForeignKey(SteeringAxleModel, on_delete=models.CASCADE,
                                      verbose_name="Модель управляемого моста")

    steering_axle_number = models.CharField("Заводской номер управляемого моста", max_length=255)

    supply_agreement = models.TextField("Договор поставки, №, дата")

    shipment_date = models.DateField("Дата отгрузки с завода")

    consignee = models.TextField("Грузополучатель")

    delivery_address = models.TextField("Адрес поставки (эксплуатации)")

    equipment = models.TextField("Комплектация, доп. опции")

    user = models.ForeignKey(auth_models.CustomUser, on_delete=models.CASCADE, verbose_name="Клиент")

    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name="Сервисная компания")

    def __str__(self):
        return self.vin

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"


"""ТО"""


class Maintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')

    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name='Вид ТО')

    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')

    operating_time = models.IntegerField(verbose_name='Наработка мото/часов')

    order = models.CharField(max_length=50, verbose_name='Номер заказа наряда')

    order_date = models.DateField(verbose_name='Дата заказа-наряда')

    def __str__(self):
        return self.car.vin + ' / ' + self.maintenance_type.name

    class Meta:
        verbose_name = 'Техническое обслуживание (ТО)'
        verbose_name_plural = 'Техническое обслуживание (ТО)'
        ordering = ('maintenance_date',)


"""Характер отказа"""


class DenialType(models.Model):
    name = models.CharField("Название", max_length=255)

    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характер отказа'
        verbose_name_plural = 'Характеры отказов'


"""Рекламация"""


class Complaint(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')

    service_company = models.ForeignKey(ServiceCompany, on_delete=models.SET_NULL, verbose_name='Сервисная компания',
                                        null=True)

    date_of_refusal = models.DateField(verbose_name='Дата отказа')

    operating_time = models.IntegerField(verbose_name='Наработка м/час')

    failure_node = models.TextField(verbose_name='Узел отказа')

    denial_type = models.ForeignKey(DenialType, on_delete=models.CASCADE, verbose_name='Характер отказа')

    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.CASCADE, verbose_name='Способ восстановления')

    used_details = models.TextField(blank=True, verbose_name='Используемые запасные части')

    date_of_restoration = models.DateField(verbose_name='Дата восстановления')

    equipment_downtime = models.TextField(verbose_name='Время простоя техники')

    def __str__(self):
        return self.car.vin + ' / ' + self.failure_node

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'
        ordering = ['date_of_refusal']
