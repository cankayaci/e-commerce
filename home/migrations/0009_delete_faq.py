# Generated by Django 3.2 on 2022-05-24 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_faq_question'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FAQ',
        ),
    ]