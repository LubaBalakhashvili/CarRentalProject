# Generated by Django 5.0.6 on 2024-06-20 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_starredcar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image1',
            field=models.ImageField(blank=True, default='media/images/default.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='car',
            name='image2',
            field=models.ImageField(blank=True, default='media/images/default.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='car',
            name='image3',
            field=models.ImageField(blank=True, default='media/images/default.jpg', upload_to='images/'),
        ),
    ]
