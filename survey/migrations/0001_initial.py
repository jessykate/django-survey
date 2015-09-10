# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('order', models.IntegerField()),
                ('required', models.BooleanField()),
                ('question_type', models.CharField(default=b'text', max_length=200, choices=[(b'text', 'text (multiple line)'), (b'short-text', 'short text (one line)'), (b'radio', 'radio'), (b'select', 'select'), (b'select-multiple', 'Select Multiple'), (b'select_image', 'Select Image'), (b'integer', 'integer')])),
                ('choices', models.TextField(help_text="if the question type is 'radio', 'select', or 'select multiple' provide a comma-separated list of options for this question .", null=True, blank=True)),
                ('category', models.ForeignKey(blank=True, to='survey.Category', null=True)),
            ],
            options={
                'ordering': ('survey', 'order'),
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('interview_uuid', models.CharField(max_length=36, verbose_name='Interview unique identifier')),
            ],
            options={
                'verbose_name': 'response',
                'verbose_name_plural': 'responses',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
                ('is_published', models.BooleanField()),
                ('need_logged_user', models.BooleanField()),
                ('display_by_question', models.BooleanField()),
            ],
            options={
                'verbose_name': 'survey',
                'verbose_name_plural': 'surveys',
            },
        ),
        migrations.CreateModel(
            name='AnswerInteger',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
                ('body', models.IntegerField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerRadio',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerSelect',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerSelectMultiple',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerText',
            fields=[
                ('answerbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.AnswerBase')),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='response',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='category',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='question',
            field=models.ForeignKey(to='survey.Question'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='response',
            field=models.ForeignKey(to='survey.Response'),
        ),
    ]
