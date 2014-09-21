# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Survey'
        db.create_table(u'survey_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')()),
            ('need_logged_user', self.gf('django.db.models.fields.BooleanField')()),
            ('display_by_question', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'survey', ['Survey'])

        # Adding model 'Category'
        db.create_table(u'survey_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
        ))
        db.send_create_signal(u'survey', ['Category'])

        # Adding model 'Question'
        db.create_table(u'survey_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('required', self.gf('django.db.models.fields.BooleanField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Category'], null=True, blank=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('question_type', self.gf('django.db.models.fields.CharField')(default='text', max_length=200)),
            ('choices', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['Question'])

        # Adding model 'Response'
        db.create_table(u'survey_response', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('interview_uuid', self.gf('django.db.models.fields.CharField')(max_length=36)),
        ))
        db.send_create_signal(u'survey', ['Response'])

        # Adding model 'AnswerBase'
        db.create_table(u'survey_answerbase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Response'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['AnswerBase'])

        # Adding model 'AnswerText'
        db.create_table(u'survey_answertext', (
            (u'answerbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['survey.AnswerBase'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['AnswerText'])

        # Adding model 'AnswerRadio'
        db.create_table(u'survey_answerradio', (
            (u'answerbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['survey.AnswerBase'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['AnswerRadio'])

        # Adding model 'AnswerSelect'
        db.create_table(u'survey_answerselect', (
            (u'answerbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['survey.AnswerBase'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['AnswerSelect'])

        # Adding model 'AnswerSelectMultiple'
        db.create_table(u'survey_answerselectmultiple', (
            (u'answerbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['survey.AnswerBase'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['AnswerSelectMultiple'])

        # Adding model 'AnswerInteger'
        db.create_table(u'survey_answerinteger', (
            (u'answerbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['survey.AnswerBase'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['AnswerInteger'])


    def backwards(self, orm):
        # Deleting model 'Survey'
        db.delete_table(u'survey_survey')

        # Deleting model 'Category'
        db.delete_table(u'survey_category')

        # Deleting model 'Question'
        db.delete_table(u'survey_question')

        # Deleting model 'Response'
        db.delete_table(u'survey_response')

        # Deleting model 'AnswerBase'
        db.delete_table(u'survey_answerbase')

        # Deleting model 'AnswerText'
        db.delete_table(u'survey_answertext')

        # Deleting model 'AnswerRadio'
        db.delete_table(u'survey_answerradio')

        # Deleting model 'AnswerSelect'
        db.delete_table(u'survey_answerselect')

        # Deleting model 'AnswerSelectMultiple'
        db.delete_table(u'survey_answerselectmultiple')

        # Deleting model 'AnswerInteger'
        db.delete_table(u'survey_answerinteger')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'survey.answerbase': {
            'Meta': {'object_name': 'AnswerBase'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Response']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'survey.answerinteger': {
            'Meta': {'object_name': 'AnswerInteger', '_ormbases': [u'survey.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'survey.answerradio': {
            'Meta': {'object_name': 'AnswerRadio', '_ormbases': [u'survey.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'survey.answerselect': {
            'Meta': {'object_name': 'AnswerSelect', '_ormbases': [u'survey.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'survey.answerselectmultiple': {
            'Meta': {'object_name': 'AnswerSelectMultiple', '_ormbases': [u'survey.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'survey.answertext': {
            'Meta': {'object_name': 'AnswerText', '_ormbases': [u'survey.AnswerBase']},
            u'answerbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.AnswerBase']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'survey.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"})
        },
        u'survey.question': {
            'Meta': {'ordering': "('survey', 'order')", 'object_name': 'Question'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Category']", 'null': 'True', 'blank': 'True'}),
            'choices': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '200'}),
            'required': ('django.db.models.fields.BooleanField', [], {}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'survey.response': {
            'Meta': {'object_name': 'Response'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview_uuid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.survey': {
            'Meta': {'object_name': 'Survey'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_by_question': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'need_logged_user': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['survey']