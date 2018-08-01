# Generated by Django 2.0.7 on 2018-08-01 08:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='ジャンル')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='顧客名')),
                ('sex', models.IntegerField(choices=[(1, '男性'), (2, '女性')], default=1, verbose_name='性別')),
                ('age', models.IntegerField(verbose_name='年齢')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='登録日')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('hours', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='時間')),
                ('charge', models.IntegerField(verbose_name='料金')),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='service.Curriculum', verbose_name='ジャンル')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='service.Customer', verbose_name='顧客')),
            ],
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['name'], name='service_cus_name_ca58fc_idx'),
        ),
    ]