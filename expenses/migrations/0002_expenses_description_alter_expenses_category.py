# Generated by Django 4.2.5 on 2024-06-22 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expenses',
            name='category',
            field=models.CharField(choices=[('RENT', 'RENT'), ('OTHERS', 'OTHERS'), ('TRAVEL', 'TRAVEL'), ('FOOD', 'FOOD'), ('OPERATING EXPENSE', 'operating expense')], max_length=255),
        ),
    ]
