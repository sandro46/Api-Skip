# Generated by Django 2.2 on 2019-04-10 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skip_tools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IvSkip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_type', models.TextField(max_length=50)),
                ('natural_person_id', models.IntegerField()),
                ('skip_date', models.DateTimeField(null=True)),
                ('prio', models.IntegerField(verbose_name='Приоритет поиска')),
                ('descr', models.TextField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Пачки, отправляемые на скип',
                'verbose_name_plural': 'Пачки, отправляемые на скип',
            },
        ),
        migrations.CreateModel(
            name='RefSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('description', models.TextField(max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Источники данных',
                'verbose_name_plural': 'Источники данных',
            },
        ),
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.AddField(
            model_name='ivskip',
            name='source_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='skip_tools.RefSource', verbose_name='Источник'),
        ),
    ]
