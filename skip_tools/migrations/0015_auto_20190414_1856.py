# Generated by Django 2.2 on 2019-04-14 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skip_tools', '0014_auto_20190414_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='source',
            field=models.ManyToManyField(related_name='template_source_rel', to='skip_tools.RefSource'),
        ),
    ]
