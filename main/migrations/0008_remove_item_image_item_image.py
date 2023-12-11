# Generated by Django 4.0.4 on 2023-12-06 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_item_image_delete_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.CreateModel(
            name='Item_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='item_images')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_image', to='main.item')),
            ],
            options={
                'db_table': 'item_images',
            },
        ),
    ]