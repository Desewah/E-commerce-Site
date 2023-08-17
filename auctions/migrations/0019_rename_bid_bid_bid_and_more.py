# Generated by Django 4.2.4 on 2023-08-08 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_auctionlisting_current_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='Bid',
            new_name='bid',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_price', to='auctions.bid'),
        ),
    ]
