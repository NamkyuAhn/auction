# Generated by Django 4.0.4 on 2023-12-06 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_item_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.FileField(default=0, upload_to='item_images'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Item_Image',
        ),
    ]
