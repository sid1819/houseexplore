# Generated by Django 4.1.1 on 2022-11-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_housesold_id_alter_housesold_house_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='img1',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='house',
            name='img2',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='house',
            name='img3',
            field=models.ImageField(upload_to='images'),
        ),
    ]