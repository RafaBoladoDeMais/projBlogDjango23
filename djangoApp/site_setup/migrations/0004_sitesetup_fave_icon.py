# Generated by Django 4.2.3 on 2023-07-18 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0003_menulink_site_setup'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetup',
            name='fave_icon',
            field=models.ImageField(blank=True, default='', upload_to='assets/faveicon/%Y/%m/'),
        ),
    ]