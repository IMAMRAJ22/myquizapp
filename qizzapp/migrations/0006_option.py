# Generated by Django 5.0.7 on 2025-06-03 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qizzapp', '0005_quizz'),
    ]

    operations = [
        migrations.CreateModel(
            name='option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texts', models.CharField(max_length=100)),
                ('is_correct', models.BooleanField(default=False)),
                ('options', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qizzapp.quizz')),
            ],
        ),
    ]
