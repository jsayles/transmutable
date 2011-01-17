# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Namespace'
        db.create_table('peach_namespace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1000)),
        ))
        db.send_create_signal('peach', ['Namespace'])

        # Adding model 'WikiPage'
        db.create_table('peach_wikipage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('namespace', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['peach.Namespace'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
            ('rendered', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('peach', ['WikiPage'])

        # Adding model 'WikiPageLog'
        db.create_table('peach_wikipagelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['peach.WikiPage'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('peach', ['WikiPageLog'])

        # Adding model 'WikiConstant'
        db.create_table('peach_wikiconstant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('constant', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('peach', ['WikiConstant'])

        # Adding model 'WikiFile'
        db.create_table('peach_wikifile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['peach.WikiPage'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('peach', ['WikiFile'])

        # Adding model 'WikiPhoto'
        db.create_table('peach_wikiphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['peach.WikiPage'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('peach', ['WikiPhoto'])


    def backwards(self, orm):
        
        # Deleting model 'Namespace'
        db.delete_table('peach_namespace')

        # Deleting model 'WikiPage'
        db.delete_table('peach_wikipage')

        # Deleting model 'WikiPageLog'
        db.delete_table('peach_wikipagelog')

        # Deleting model 'WikiConstant'
        db.delete_table('peach_wikiconstant')

        # Deleting model 'WikiFile'
        db.delete_table('peach_wikifile')

        # Deleting model 'WikiPhoto'
        db.delete_table('peach_wikiphoto')


    models = {
        'peach.namespace': {
            'Meta': {'object_name': 'Namespace'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000'})
        },
        'peach.wikiconstant': {
            'Meta': {'object_name': 'WikiConstant'},
            'constant': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'peach.wikifile': {
            'Meta': {'ordering': "['-created']", 'object_name': 'WikiFile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['peach.WikiPage']"})
        },
        'peach.wikipage': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WikiPage'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'namespace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['peach.Namespace']"}),
            'rendered': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'peach.wikipagelog': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'WikiPageLog'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['peach.WikiPage']"})
        },
        'peach.wikiphoto': {
            'Meta': {'ordering': "['-created']", 'object_name': 'WikiPhoto'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['peach.WikiPage']"})
        }
    }

    complete_apps = ['peach']
