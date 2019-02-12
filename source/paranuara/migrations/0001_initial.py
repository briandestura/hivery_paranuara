# Generated by Django 2.0.9 on 2019-02-11 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'friendship',
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('index', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('_id', models.CharField(blank=True, max_length=255, null=True)),
                ('guid', models.CharField(blank=True, max_length=255, null=True)),
                ('has_died', models.BooleanField(default=False)),
                ('balance', models.CharField(blank=True, max_length=255, null=True)),
                ('picture', models.URLField(blank=True, null=True)),
                ('age', models.PositiveIntegerField(default=0)),
                ('eyeColor', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('registered', models.DateTimeField(blank=True, null=True)),
                ('tags', models.TextField(blank=True, null=True)),
                ('greeting', models.TextField(blank=True, null=True)),
                ('favorite_fruits', models.TextField(blank=True, null=True)),
                ('favorite_vegetables', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, db_column='company_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='paranuara.Company')),
            ],
            options={
                'db_table': 'people',
            },
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='paranuara.People'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paranuara.People'),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together={('person', 'friend')},
        ),
    ]
