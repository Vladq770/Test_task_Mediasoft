# Generated by Django 4.1 on 2023-07-05 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_auto_20230702_1457"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="authors",
            field=models.ManyToManyField(
                blank=True, related_name="blogs", to="core.user"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="posts", to="core.tag"
            ),
        ),
    ]
