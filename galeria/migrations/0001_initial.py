# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table('galeria_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['galeria.Album'])),
            ('cover', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cover', null=True, on_delete=models.SET_NULL, to=orm['galeria.Image'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('galeria', ['Album'])

        # Adding unique constraint on 'Album', fields ['slug', 'parent']
        db.create_unique('galeria_album', ['slug', 'parent_id'])

        # Adding model 'Image'
        db.create_table('galeria_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('album', self.gf('mptt.fields.TreeForeignKey')(to=orm['galeria.Album'])),
        ))
        db.send_create_signal('galeria', ['Image'])

        # Adding unique constraint on 'Image', fields ['slug', 'album']
        db.create_unique('galeria_image', ['slug', 'album_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'Image', fields ['slug', 'album']
        db.delete_unique('galeria_image', ['slug', 'album_id'])

        # Removing unique constraint on 'Album', fields ['slug', 'parent']
        db.delete_unique('galeria_album', ['slug', 'parent_id'])

        # Deleting model 'Album'
        db.delete_table('galeria_album')

        # Deleting model 'Image'
        db.delete_table('galeria_image')

    models = {
        'galeria.album': {
            'Meta': {'unique_together': "(('slug', 'parent'),)", 'object_name': 'Album'},
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['galeria.Image']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['galeria.Album']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'galeria.image': {
            'Meta': {'ordering': "['-date_added']", 'unique_together': "(('slug', 'album'),)", 'object_name': 'Image'},
            'album': ('mptt.fields.TreeForeignKey', [], {'to': "orm['galeria.Album']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['galeria']