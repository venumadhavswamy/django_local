# Generated by Django 2.2.5 on 2019-09-17 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0007_auto_20190917_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='y',
            name='x_link',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sample.X'),
        ),
    ]
