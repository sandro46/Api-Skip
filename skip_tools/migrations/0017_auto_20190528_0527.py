# Generated by Django 2.2 on 2019-05-28 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skip_tools', '0016_auto_20190528_0526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refsource',
            old_name='name1',
            new_name='name',
        ),
    ]
