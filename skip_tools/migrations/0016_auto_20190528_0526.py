# Generated by Django 2.2 on 2019-05-28 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skip_tools', '0015_auto_20190414_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refsource',
            old_name='name',
            new_name='name1',
        ),
    ]
