# Generated by Django 4.1.1 on 2022-11-11 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='contac_address',
            new_name='contact_address',
        ),
    ]
