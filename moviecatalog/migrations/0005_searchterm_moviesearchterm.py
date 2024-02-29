# Generated by Django 5.0 on 2024-02-13 19:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviecatalog', '0004_alter_movie_actors'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_term', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MovieSearchTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviecatalog.movie')),
                ('search_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviecatalog.searchterm')),
            ],
            options={
                'unique_together': {('movie', 'search_term')},
            },
        ),
    ]
