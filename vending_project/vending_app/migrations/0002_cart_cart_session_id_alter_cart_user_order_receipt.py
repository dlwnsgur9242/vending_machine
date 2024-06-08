# Generated by Django 5.0.6 on 2024-06-05 09:21

import django.db.models.deletion
import uuid
import vending_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vending_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_session_id',
            field=models.CharField(default=vending_app.models.generate_unique_session_id, max_length=32),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vending_app.user'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_qty', models.PositiveIntegerField()),
                ('order_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_datetime', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vending_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('receipt_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_type', models.CharField(choices=[('card', '카드'), ('cash', '현금')], max_length=10)),
                ('receipt_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receipt_datetime', models.DateTimeField(auto_now_add=True)),
                ('one_thousand', models.PositiveIntegerField(default=0)),
                ('five_thousand', models.PositiveIntegerField(default=0)),
                ('ten_thousand', models.PositiveIntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vending_app.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vending_app.user')),
            ],
        ),
    ]