# Generated by Django 4.2.13 on 2024-05-25 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('website', models.URLField()),
                ('city', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('S', 'Science&Tech'), ('F', 'Fiction'), ('B', 'Biography'), ('T', 'Travel'), ('O', 'Other')], default='S', max_length=1)),
                ('num_pages', models.PositiveIntegerField(default=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='myapp.publisher')),
            ],
        ),
    ]
