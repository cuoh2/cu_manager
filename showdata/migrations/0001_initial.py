# Generated by Django 2.2.6 on 2019-10-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CPUData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=128, verbose_name='CPU数据')),
                ('time', models.DateTimeField(verbose_name='监听时间')),
            ],
            options={
                'verbose_name': 'CPU数据表',
                'verbose_name_plural': 'CPU数据表',
            },
        ),
    ]
