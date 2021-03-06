# Generated by Django 3.1.1 on 2020-12-27 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log5XXError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exception', models.CharField(blank=True, max_length=255, null=True)),
                ('exception_traceback', models.TextField(blank=True, null=True)),
                ('exception_class', models.CharField(blank=True, max_length=255, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('request_method', models.CharField(blank=True, max_length=15, null=True)),
                ('request_body', models.TextField(blank=True, null=True)),
                ('request_headers', models.TextField(blank=True, null=True)),
                ('request_is_ajax', models.BooleanField(blank=True, null=True)),
                ('request_is_secure', models.BooleanField(blank=True, null=True)),
                ('request_scheme', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(choices=[('0', 'Open'), ('1', 'Resolved')], default='0', max_length=5)),
            ],
        ),
    ]
