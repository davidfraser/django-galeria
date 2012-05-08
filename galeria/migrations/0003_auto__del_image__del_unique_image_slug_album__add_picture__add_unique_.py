# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Image', fields ['slug', 'album']
        db.delete_unique('galeria_image', ['slug', 'album_id'])

        # Deleting model 'Image'
        db.delete_table('galeria_image')

        # Adding model 'Picture'
        db.create_table('galeria_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('album', self.gf('mptt.fields.TreeForeignKey')(related_name='pictures', to=orm['galeria.Album'])),
        ))
        db.send_create_signal('galeria', ['Picture'])

        # Adding unique constraint on 'Picture', fields ['slug', 'album']
        db.create_unique('galeria_picture', ['slug', 'album_id'])


        # Changing field 'Album.cover'
        db.alter_column('galeria_album', 'cover_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['galeria.Picture']))
    def backwards(self, orm):
        # Removing unique constraint on 'Picture', fields ['slug', 'album']
        db.delete_unique('galeria_picture', ['slug', 'album_id'])

        # Adding model 'Image'
        db.create_table('galeria_image', (
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('mptt.fields.TreeForeignKey')(related_name='images', to=orm['galeria.Album'])),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
        ))
        db.send_create_signal('galeria', ['Image'])

        # Adding unique constraint on 'Image', fields ['slug', 'album']
        db.create_unique('galeria_image', ['slug', 'album_id'])

        # Deleting model 'Picture'
        db.delete_table('galeria_picture')


        # Changing field 'Album.cover'
        db.alter_column('galeria_album', 'cover_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['galeria.Image'], on_delete=models.SET_NULL))
    models = {
        'galeria.album': {
            'Meta': {'unique_together': "(('slug', 'parent'),)", 'object_name': 'Album'},
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['galeria.Picture']"}),
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
        'galeria.picture': {
            'Meta': {'ordering': "('-date_added',)", 'unique_together': "(('slug', 'album'),)", 'object_name': 'Picture'},
            'album': ('mptt.fields.TreeForeignKey', [], {'related_name': "'pictures'", 'to': "orm['galeria.Album']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['galeria']