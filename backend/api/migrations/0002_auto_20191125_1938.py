# Generated by Django 2.2.1 on 2019-11-25 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='locked',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='UserPaymentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_code', models.TextField()),
                ('iban', models.TextField()),
                ('bank_number', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
