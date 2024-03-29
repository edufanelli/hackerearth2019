# Generated by Django 2.2.7 on 2019-12-01 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conveyor_belt', models.CharField(help_text='Conveyor_belt identification', max_length=5)),
                ('order', models.IntegerField(blank=True, help_text='order', null=True)),
                ('production_time', models.IntegerField(blank=True, help_text='production time', null=True)),
                ('delivery_time', models.IntegerField(blank=True, help_text='delivery time', null=True)),
                ('status', models.CharField(help_text='Status identification', max_length=50)),
            ],
            options={
                'verbose_name': 'Alocation',
                'verbose_name_plural': 'Alocation',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Client identification', max_length=50)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Conveyor_belt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conveyor_belt', models.CharField(help_text='Conveyor_belt identification', max_length=5)),
            ],
            options={
                'verbose_name': 'Conveyor belt',
                'verbose_name_plural': 'Conveyor belts',
            },
        ),
        migrations.CreateModel(
            name='Failure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor', models.IntegerField(blank=True, help_text='Sensor number', null=True)),
                ('timestamp', models.DateTimeField(editable=False)),
                ('conveyor_belt', models.CharField(help_text='Conveyor Belt identification', max_length=10)),
                ('machine', models.CharField(help_text='Machine Name', max_length=80)),
                ('unit', models.CharField(help_text='Unit Name', max_length=80)),
                ('group', models.CharField(help_text='Group Name', max_length=80)),
                ('component', models.CharField(help_text='Component Name', max_length=80)),
                ('failure_mode', models.CharField(help_text='Failure Mode Name', max_length=80)),
                ('discipline', models.CharField(help_text='Discipline Name', max_length=80)),
                ('comments', models.CharField(help_text='Comments', max_length=300)),
                ('delay_min', models.IntegerField(blank=True, help_text='Delay Min', null=True)),
                ('avg_repair_time', models.IntegerField(blank=True, help_text='Average repair time (hours)', null=True)),
                ('avg_repair_cost', models.IntegerField(blank=True, help_text='Average repair cost (USD)', null=True)),
                ('status', models.CharField(help_text='status', max_length=80)),
            ],
            options={
                'verbose_name': 'Failure',
                'verbose_name_plural': 'Failures',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(blank=True, help_text='order number', null=True)),
                ('client', models.CharField(help_text='Client identification', max_length=50)),
                ('product', models.CharField(help_text='Product identification', max_length=50)),
                ('quantity', models.IntegerField(blank=True, help_text='Quantity', null=True)),
                ('deadline', models.IntegerField(blank=True, help_text='Deadline (hrs)', null=True)),
                ('status', models.CharField(help_text='Status identification', max_length=50)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Product identification', max_length=50)),
                ('production_time', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
