# Generated by Django 4.0.4 on 2023-12-06 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_item_image_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_image',
            name='image',
            field=models.FileField(upload_to='item_images'),
        ),
    ]