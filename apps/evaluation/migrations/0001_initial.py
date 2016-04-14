# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChosenAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
            ],
            options={
                'verbose_name': 'respuesta',
                'verbose_name_plural': 'respuestas',
            },
        ),
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=200)),
                ('posX', models.FloatField(null=True, blank=True)),
                ('posY', models.FloatField(null=True, blank=True)),
                ('required_by', models.ManyToManyField(related_name='prerequisite', null=True, to='evaluation.Concept', blank=True)),
            ],
            options={
                'verbose_name': 'concepto',
                'verbose_name_plural': 'conceptos',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='nombre del curso')),
                ('code', models.CharField(max_length=100, verbose_name='clave del curso')),
                ('students', models.ManyToManyField(related_name='students', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('teacher', models.ForeignKey(related_name='profesor', verbose_name='profesor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'curso',
                'verbose_name_plural': 'cursos',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=60)),
                ('instructions', models.CharField(max_length=400, blank=True)),
                ('activated', models.BooleanField(default=False)),
                ('duration', models.TimeField(null=True)),
            ],
            options={
                'verbose_name': 'examen',
                'verbose_name_plural': 'ex\xe1menes',
            },
        ),
        migrations.CreateModel(
            name='PossibleAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('text', models.TextField(max_length=500)),
                ('correct', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'opci\xf3n',
                'verbose_name_plural': 'opciones',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('sentence', models.TextField()),
                ('points', models.PositiveSmallIntegerField()),
                ('concepts', models.ManyToManyField(related_name='related_concepts', null=True, to='evaluation.Concept', blank=True)),
                ('exam', models.ForeignKey(related_name='exam', to='evaluation.Exam', null=True)),
            ],
            options={
                'verbose_name': 'pregunta',
                'verbose_name_plural': 'preguntas',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=100, verbose_name='nombre de la unidad')),
                ('concepts', models.ManyToManyField(related_name='concept', verbose_name='conceptos relacioandos', to='evaluation.Concept')),
                ('course', models.ForeignKey(related_name='course', verbose_name='curso', to='evaluation.Course')),
            ],
            options={
                'verbose_name': 'unidad',
                'verbose_name_plural': 'unidades',
            },
        ),
        migrations.AddField(
            model_name='possibleanswer',
            name='question',
            field=models.ForeignKey(related_name='question', to='evaluation.Question', null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='unit',
            field=models.ForeignKey(related_name='unit', to='evaluation.Unit'),
        ),
        migrations.AddField(
            model_name='chosenanswer',
            name='answer',
            field=models.ForeignKey(related_name='chosen', to='evaluation.PossibleAnswer'),
        ),
        migrations.AddField(
            model_name='chosenanswer',
            name='question',
            field=models.ForeignKey(related_name='section', to='evaluation.Question', null=True),
        ),
        migrations.AddField(
            model_name='chosenanswer',
            name='student',
            field=models.ForeignKey(related_name='student', to=settings.AUTH_USER_MODEL),
        ),
    ]
