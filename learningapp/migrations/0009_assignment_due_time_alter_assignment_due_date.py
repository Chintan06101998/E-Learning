# Generated by Django 4.2.2 on 2023-07-18 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learningapp', '0008_remove_assignment_material_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(null=True),
        ),
    ]
