# Generated by Django 4.2.2 on 2023-07-23 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_rename_recipe_exercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='exercise_photos/'),
        ),
    ]
