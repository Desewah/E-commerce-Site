# Generated by Django 4.2.4 on 2023-08-08 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionlisting_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='auctions.auctionlisting')),
            ],
            options={
                'ordering': ['time_created'],
            },
        ),
    ]
