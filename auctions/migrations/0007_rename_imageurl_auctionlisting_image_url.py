# Generated by Django 4.2.4 on 2023-08-06 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionlisting_imageurl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='imageUrl',
            new_name='image_url',
        ),
    ]
