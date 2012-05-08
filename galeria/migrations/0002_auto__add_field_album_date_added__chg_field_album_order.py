# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Album.date_added'
        db.add_column('galeria_album', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 17, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Album.order'
        db.alter_column('galeria_album', 'order', self.gf('django.db.models.fields.CharField')(max_length=16))
    def backwards(self, orm):
        # Deleting field 'Album.date_added'
        db.delete_column('galeria_album', 'date_added')


        # Changing field 'Album.order'
        db.alter_column('galeria_album', 'order', self.gf('django.db.models.fields.CharField')(max_length=2))
    models = {
        'galeria.album': {
            'Meta': {'unique_together': "(('slug', 'parent'),)", 'object_name': 'Album'},
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['galeria.Image']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'default': "'-date_added'", 'max_length': '16'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['galeria.Album']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'galeria.image': {
            'Meta': {'ordering': "('-date_added',)", 'unique_together': "(('slug', 'album'),)", 'object_name': 'Image'},
            'album': ('mptt.fields.TreeForeignKey', [], {'related_name': "'images'", 'to': "orm['galeria.Album']"}),
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