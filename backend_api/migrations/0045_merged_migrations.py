import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0042_alter_acsparttimerstatus_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='HappinessIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happiness_score', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, unique_for_date='employee')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.user')),
            ],
            options={
                'db_table': 'happiness_index',
                'unique_together': {('employee', 'date')},
            },
        ),
        migrations.AddField(
            model_name='statusupdates',
            name='leave',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='acsparttimerstatus',
            name='date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2025, 4, 14))]),
        ),
    ]