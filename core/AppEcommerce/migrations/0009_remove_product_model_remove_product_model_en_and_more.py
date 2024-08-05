# Generated by Django 5.0.3 on 2024-05-11 20:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AppEcommerce", "0008_alter_brand_options_remove_brand_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="model",
        ),
        migrations.RemoveField(
            model_name="product",
            name="model_en",
        ),
        migrations.RemoveField(
            model_name="product",
            name="model_tr",
        ),
        migrations.AddField(
            model_name="product",
            name="asansor",
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="durum",
            field=models.CharField(
                choices=[("kiralık", "kiralık"), ("satılık", "satılık")],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="güvenlik",
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="kat_sayısı",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="otopark",
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="room_number",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="title",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="title_en",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="title_tr",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.FloatField(null=True),
        ),
    ]