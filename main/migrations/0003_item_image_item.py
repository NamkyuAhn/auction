# Generated by Django 4.0.4 on 2023-12-06 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_image',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.item'),
            preserve_default=False,
        ),
    ]
