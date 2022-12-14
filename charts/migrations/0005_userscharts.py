# Generated by Django 4.1.2 on 2022-11-24 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0004_accounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersCharts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('save_date', models.DateField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charts.accounts')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charts.chart')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charts.ticker')),
            ],
        ),
    ]
