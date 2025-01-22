
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_servicecompany_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='service_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.servicecompany', verbose_name='Сервисная компания'),
        ),
    ]
