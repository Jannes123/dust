# Generated by Django 4.0.3 on 2023-02-24 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incoming', '0002_alter_codefunction_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codefunction',
            name='sponsor_number',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='codefunction',
            name='user_number',
            field=models.CharField(max_length=32),
        ),
    ]
