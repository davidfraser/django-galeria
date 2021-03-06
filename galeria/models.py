# -*- coding: utf-8 -*-

import os

from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from galeria import EXIF

import pyexiv2
import collections

ORDER_CHOICES = (
    ('-date_added', _('Descending by addition date')),
    ('date_added',  _('Ascending by addition date')),
    ('-date_taken', _('Descending by date taken')),
    ('date_taken',  _('Ascending by date taken')),
    ('-date_modified', _('Descending by modification date')),
    ('date_modified',  _('Ascending by modification date')),
)


class AlbumManager(TreeManager):
    use_for_related_fields = True

    def public(self):
        return super(AlbumManager, self).filter(is_public=True)

    def public_root_nodes(self):
        return super(AlbumManager, self).root_nodes().filter(is_public=True)


class Album(MPTTModel):
    title = models.CharField(_('title'), max_length=256)
    slug = models.SlugField(
        _('slug'),
        max_length=256,
        help_text=_('Automatically built from the title. A slug is a short '
                    'label generally used in URLs.'),
    )
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(
        _('is public'),
        default=True,
        help_text=_('Only public albums will be displayed in the default views.')
    )
    order = models.CharField(
        _('order'),
        max_length=16,
        choices=ORDER_CHOICES,
        default='-date_added',
        help_text=_('The default order of pictures for this album.')
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name=_('parent album'),
        related_name='children'
    )
    cover = models.ForeignKey(
        'galeria.Picture',
        verbose_name=_('cover'),
        related_name='cover',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)

    objects = AlbumManager()

    class Meta:
        unique_together = (('slug', 'parent'),)
        verbose_name = _('album')
        verbose_name_plural = _('albums')

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('galeria-album', None, {
            'slug' : str(self.slug)
        })

    @property
    def available_cover(self):
        if self.cover:
            return self.cover
        elif getattr(self, '_cover', None):
            return self._cover
        try:
            self._cover = self.pictures.public().order_by('?')[0]
            return self._cover
        except IndexError:
            return None

    @property
    def ordered_pictures(self):
        return self.pictures.public().order_by(self.order)

    def get_album_tree(self):
        tree = [self.slug]
        if self.parent:
            tree = self.parent.get_album_tree() + tree
        return tree



def picture_imagefield_path(instance, filename):
    album_tree = '/'.join(instance.album.get_album_tree())
    return os.path.join('galeria', album_tree, filename)


class PictureManager(models.Manager):
    use_for_related_fields = True

    def public(self):
        return super(PictureManager, self).filter(is_public=True, album__is_public=True)


class Picture(models.Model):
    title = models.CharField(_('title'), max_length=256)
    slug = models.SlugField(
        _('slug'),
        max_length=256,
        help_text=_('Automatically built from the title. A slug is a short '
                    'label generally used in URLs.'),
    )
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    date_taken = models.DateTimeField(_('date taken'), null=True, editable=False)
    original_image = models.ImageField(_('image'), upload_to=picture_imagefield_path)
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(
        _('is public'),
        default=True,
        help_text=_('Public images will be displayed in the default views.')
    )
    album = TreeForeignKey(
        'galeria.Album',
        verbose_name=_('album'),
        related_name='pictures'
    )

    objects = PictureManager()

    class Meta:
        ordering = ('-date_added',)
        get_latest_by = 'date_added'
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')

    @property
    def EXIF(self):
        image_file = default_storage.open(self.original_image.name, 'rb')
        try:
            return EXIF.process_file(image_file)
        except Exception, e:
            # TODO: log exception
            try:
                return EXIF.process_file(image_file, details=False)
            except Exception, e:
                # TODO: log exception
                return {}
        finally:
            image_file.close()

    def get_metadata(self):
        if hasattr(self, "_metadata"):
            return self._metadata
        metadata = pyexiv2.ImageMetadata(default_storage.path(self.original_image.name))
        metadata.read()
        self._metadata = metadata
        return metadata

    @property
    def metadata(self):
        metadata = self.get_metadata()
        return collections.OrderedDict([(key, metadata[key].raw_value) for key in metadata.exif_keys + metadata.iptc_keys + metadata.xmp_keys])

    @property
    def metadata_description(self):
        metadata = self.get_metadata()
        if 'Iptc.Application2.Caption' in metadata.iptc_keys:
            return ' '.join(metadata['Iptc.Application2.Caption'].value)
        elif 'Exif.Photo.UserComment' in metadata.exif_keys:
            return ' '.join(metadata['Exif.Photo.UserComment'].value)
        return self.description or self.title

    @property
    def key_metadata(self):
        metadata = self.get_metadata()
        keys = metadata.exif_keys + metadata.iptc_keys
        filtered_metadata = []
        filtered_metadata.append(('Description', self.metadata_description))
        if 'Iptc.Application2.Keywords' in keys:
            tags = metadata['Iptc.Application2.Keywords'].value
            tags_str = " ".join([tag.strip() for tag in tags])
            filtered_metadata.append(('Tags', tags_str))
        if 'Exif.Image.DateTime' in keys:
            image_date = metadata['Exif.Image.DateTime'].value
            filtered_metadata.append(('Date', image_date))
        if 'Exif.Image.Make' in keys and 'Exif.Image.Model' in keys:
            camera_make = metadata['Exif.Image.Make'].value
            camera_model = metadata['Exif.Image.Model'].value
            filtered_metadata.append(('Camera', "%s %s" % (camera_make, camera_model)))
        return filtered_metadata

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)
        if not self.date_taken:
            exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
            if exif_date:
                try:
                    self.date_taken = datetime.strptime(str(exif_date), '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    # In case of bad formatted EXIF date...
                    pass
                super(Picture, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('galeria-picture', None, {
            'album_slug' : str(self.album.slug),
            'pk' : str(self.pk),
            'slug' : str(self.slug)
        })
