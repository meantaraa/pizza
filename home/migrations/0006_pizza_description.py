# Generated by Django 5.0.7 on 2024-07-29 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_cart_updated_at_alter_cartitem_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]