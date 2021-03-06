# Generated by Django 2.0.5 on 2018-06-02 19:35

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casting_time', models.CharField(blank=True, max_length=128, null=True)),
                ('classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=24), default=list, size=24)),
                ('components', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('description', models.CharField(blank=True, max_length=10240, null=True)),
                ('higher_levels', models.CharField(blank=True, max_length=1024, null=True)),
                ('duration', models.CharField(blank=True, max_length=128, null=True)),
                ('level', models.SmallIntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('spell_range', models.CharField(blank=True, max_length=128, null=True)),
                ('ritual', models.BooleanField(default=False)),
                ('school', models.CharField(blank=True, max_length=128, null=True)),
                ('spell_type', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Spellbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Generic Spellbook', max_length=64)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=24), default=list, size=24)),
                ('spells', models.ManyToManyField(related_name='spellbooks', to='spells.Spell')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
