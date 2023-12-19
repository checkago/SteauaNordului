# Generated by Django 3.2.8 on 2022-11-01 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории меню',
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=4, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Ед. изм.',
                'verbose_name_plural': 'Единицы имз.',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование млд.')),
                ('name_ru', models.CharField(blank=True, max_length=100, verbose_name='Наименование рус.')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним')),
                ('composition', models.CharField(blank=True, max_length=100, verbose_name='Состав млд.')),
                ('composition_ru', models.CharField(blank=True, max_length=100, verbose_name='Состав рус.')),
                ('volume_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Объем/Вес')),
                ('price_1', models.FloatField(verbose_name='Цена')),
                ('volume_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Объем/Вес')),
                ('price_2', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('image', models.ImageField(upload_to='media/images', verbose_name='Фото')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.category', verbose_name='Категория')),
                ('volume_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.volume', verbose_name='Ед. изм')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
    ]
