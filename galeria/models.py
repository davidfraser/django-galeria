import os

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpec
from imagekit.processors import Transpose
from imagekit.processors.resize import Crop, Fit
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from galeria import EXIF


DISPLAY_IMAGE_PROCESSORS = getattr(settings, 'GALERIA_DISPLAY_IMAGE_PROCESSORS', [
    Transpose(Transpose.AUTO), Fit(width=600, height=600)
])
THUMBNAIL_IMAGE_PROCESSORS = getattr(settings, 'GALERIA_THUMBNAIL_IMAGE_PROCESSORS', [
    Transpose(Transpose.AUTO), Crop(width=128, height=128, anchor=Crop.CENTER)
])
COVER_IMAGE_PROCESSORS = getattr(settings, 'GALERIA_COVER_IMAGE_PROCESSORS', [
    Transpose(Transpose.AUTO), Crop(width=128, height=128, anchor=Crop.CENTER)
])

ORDER_CHOICES = (
    ('-date_added', _('Descending by addition date')),
    ('date_added',  _('Ascending by addition date')),
    ('-date_taken', _('Descending by date taken')),
    ('date_daten',  _('Ascending by date taken')),
    ('-date_modified', _('Descending by modification date')),
    ('date_modified',  _('Ascending by modification date')),
)


class AlbumManager(models.Manager):
    use_for_related_fields = True

    def public(self):
        return super(AlbumManager, self).filter(is_public=True)


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
        elif self.parent:
            return self.parent.available_cover
        else:
            return None

    @property
    def ordered_pictures(self):
        return self.pictures.order_by(self.order)

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
        return super(PictureManager, self).filter(is_public=True)


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
    display_image = ImageSpec(
        DISPLAY_IMAGE_PROCESSORS,
        image_field='original_image',
        options={'quality': 90},
        pre_cache=True
    )
    thumbnail_image = ImageSpec(
        THUMBNAIL_IMAGE_PROCESSORS,
        image_field='original_image',
        format='JPEG',
        options={'quality': 75},
        pre_cache=True
    )
    cover_image = ImageSpec(
        COVER_IMAGE_PROCESSORS,
        image_field='original_image',
        format='JPEG',
        options={'quality': 75},
        autoconvert=False
    )
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
        unique_together = (('slug', 'album'),)

    @property
    def EXIF(self):
        image_file = open(self.original_image.path, 'rb')
        try:
            data = EXIF.process_file(image_file)
        except Exception, e:
            # TODO: log exception
            try:
                data = EXIF.process_file(image_file, details=False)
            except Exception, e:
                pass # TODO: log exception
        image_file.close()
        return data

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)
        if not self.date_taken:
            exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
            if exif_date:
                self.date_taken = datetime.strptime(str(exif_date), '%Y:%m:%d %H:%M:%S')
                super(Picture, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('galeria-picture', None, {
            'year' : str(self.date_added.year),
            'month': str(self.date_added.month).zfill(2),
            'day'  : str(self.date_added.day).zfill(2),
            'slug' : str(self.slug)
        })
