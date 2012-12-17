VERSION = (0, 4, 12)


def get_version():
    """Returns the version as a human-format string.
    """
    return '.'.join([str(i) for i in VERSION])


__author__ = 'See the file AUTHORS'
__license__ = 'BSD License'
__url__ = 'https://bitbucket.org/semente/django-gallery'
__version__ = get_version()
