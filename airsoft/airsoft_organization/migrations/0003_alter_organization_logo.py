# Generated by Django 4.1.1 on 2022-12-07 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airsoft_organization", "0002_rename_members_member_orgrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="logo",
            field=models.ImageField(
                blank=True,
                default="airsoft/media/org_logo/nopic.jpeg",
                upload_to="org_logo",
            ),
        ),
    ]
