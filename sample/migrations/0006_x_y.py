# Generated by Django 2.2.5 on 2019-09-17 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0005_auto_20190910_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='X',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_var1', models.CharField(max_length=50)),
                ('x_var2', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Y',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('y_var1', models.CharField(max_length=50)),
                ('y_var2', models.CharField(max_length=50)),
                ('x_link', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sample.X')),
            ],
        ),
    ]
